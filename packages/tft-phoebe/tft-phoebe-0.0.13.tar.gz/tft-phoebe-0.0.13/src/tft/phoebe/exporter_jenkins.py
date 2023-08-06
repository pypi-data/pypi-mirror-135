import argparse
import collections
import dataclasses
import re

import bs4
import requests
from prometheus_client import Gauge

from . import Exporter, Metric

from typing import cast, Any, DefaultDict, Dict, Iterator, List

JSONType = Dict[str, Any]


@dataclasses.dataclass
class JenkinsConnection:
    url: str
    username: str
    password: str


@dataclasses.dataclass
class NodeInfo:
    api: Dict[str, Any]
    config: bs4.Tag


@dataclasses.dataclass
class NodesInfo:
    api: List[Dict[str, Any]]
    nodes: Dict[str, NodeInfo]


class JenkinsExporter(Exporter):
    def parse_args(self) -> argparse.Namespace:
        options = super(JenkinsExporter, self).parse_args()

        self.jenkins = JenkinsConnection(
            url=self.config['jenkins']['master_url'],
            username=self.config['jenkins']['username'],
            password=self.config['jenkins']['password']
        )

        return options

    def _fetch_json(self, url: str) -> JSONType:
        return cast(
            JSONType,
            requests.get(
                f'{self.jenkins.url}/{url}',
                auth=(self.jenkins.username, self.jenkins.password)
            ).json()
        )

    def _fetch_xml(self, url: str) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(
            requests.get(
                f'{self.jenkins.url}/{url}',
                auth=(self.jenkins.username, self.jenkins.password)
            ).content,
            'xml'
        )

    def fetch_data(self) -> None:
        self.data_nodes = NodesInfo(
            api=[],
            nodes={}
        )

        # Fetch summary data we can get for all nodes via JSON API.
        self.data_nodes.api = cast(
            List[Dict[str, Any]],
            self._fetch_json('/computer/api/json?depth=1')['computer']
        )

        # For each node, fetch its configuration, and extract its JSON API data from the global structure.
        for node_info in self.data_nodes.api:
            display_name = node_info['displayName']

            if display_name == 'master':
                continue

            self.data_nodes.nodes[display_name] = NodeInfo(
                api=node_info,
                config=self._fetch_xml(f'/computer/{display_name}/config.xml')
            )

        self.data_queue = self._fetch_json('/queue/api/json')

    def _create_label_count_metric(self) -> Metric:
        # We initialize values for `expected-labels` to zero, but we also want to add
        # entries for *unexpected* labels, which is easier with defaultdict.
        labels: DefaultDict[str, float] = collections.defaultdict(float)

        if self.data_fetch_failed:
            # When data fetch failed, set all metrics to NaN.
            for label in self.config['expected-labels']:
                labels[label] = float('nan')

        else:
            # Make sure to set default value for all labels.
            for label in self.config['expected-labels']:
                labels[label] = 0

            for display_name, node in self.data_nodes.nodes.items():
                node_labels_el = node.config.find('label')
                if node_labels_el is None:
                    self.logger.error(
                        f'Node {display_name} has no "label" configuration'
                    )
                    continue

                for label in node_labels_el.text.split(' '):
                    labels[label] += 1

        metric = Gauge(
            'node_labels',
            'Number of executors having a given label',
            ['label']
        )

        for node_label, count in labels.items():
            metric.labels(
                label=node_label
            ).set(count)

        return metric

    def _create_build_count_metric(self) -> Metric:
        # We initialize values for `expected-jobs` to zero, but we also want to add
        # entries for *unexpected* job, which is easier with defaultdict.
        running_jobs: DefaultDict[str, float] = collections.defaultdict(float)
        buildable_jobs: DefaultDict[str, float] = collections.defaultdict(float)
        blocked_jobs: DefaultDict[str, float] = collections.defaultdict(float)

        if self.data_fetch_failed:
            # When data fetch failed, set all metrics to NaN.
            for job in self.config['expected-jobs']:
                running_jobs[job] = float('nan')
                buildable_jobs[job] = float('nan')
                blocked_jobs[job] = float('nan')

        else:
            # Make sure to set default value for all jobs.
            for job in self.config['expected-jobs']:
                running_jobs[job] = 0
                buildable_jobs[job] = 0
                blocked_jobs[job] = 0

            # Running builds first
            for display_name, node in self.data_nodes.nodes.items():
                for executor in node.api['executors']:
                    if executor['currentExecutable'] is None:
                        continue

                    if 'url' not in executor['currentExecutable']:
                        self.logger.error(
                            f'Executor {display_name}:{executor["number"]} has no build URL'
                        )
                        continue

                    match = re.match(
                        fr'{self.jenkins.url}/job/(.+?)/\d+/',
                        executor['currentExecutable']['url']
                    )

                    if match:
                        running_jobs[match.group(1)] += 1

            # Queued builds next
            for queue_item in self.data_queue['items']:
                item_task = queue_item['task']
                item_class = item_task['_class']

                # These are known for not having project name
                if item_class == 'org.jenkinsci.plugins.workflow.support.steps.ExecutorStepExecution$PlaceholderTask':
                    self.logger.warn(
                        'task of type "ExecutorStepExecution$PlaceholderTask" does not specify project name'
                    )

                    continue

                # Let's make sure we get nice error when the project name's missing in queue items that should
                # specify it, at least as far as we can.
                if 'name' not in item_task:
                    raise Exception(f'task of type "{item_class}" does not specify project name')

                item_task_name = item_task['name']

                if item_class == 'hudson.model.Queue$BuildableItem':
                    buildable_jobs[item_task_name] += 1

                elif item_class == 'hudson.model.FreeStyleProject':
                    buildable_jobs[item_task_name] += 1

                elif item_class == 'hudson.model.Queue$BlockedItem':
                    blocked_jobs[item_task_name] += 1

                else:
                    self.logger.warn(
                        f'task of type "{item_class}" (task name {item_task_name}) was not recognized'
                    )

        metric = Gauge(
            'build_count',
            'Number of builds of a given job',
            # Simple "job" would be nicer, but that would collide with Prometheus' "job" label.
            ['jenkins_job', 'state']
        )

        for job_name, count in running_jobs.items():
            metric.labels(
                jenkins_job=job_name,
                state='running'
            ).set(count)

        for job_name, count in buildable_jobs.items():
            metric.labels(
                jenkins_job=job_name,
                state='buildable'
            ).set(count)

        for job_name, count in blocked_jobs.items():
            metric.labels(
                jenkins_job=job_name,
                state='blocked'
            ).set(count)

        for job_name in buildable_jobs.keys():
            metric.labels(
                jenkins_job=job_name,
                state='queued'
            ).set(buildable_jobs[job_name] + blocked_jobs[job_name])

        return metric

    def create_metric(self) -> Iterator[Metric]:
        yield self._create_label_count_metric()
        yield self._create_build_count_metric()


def main() -> None:
    """
    Fetches metrics from Jenkins and exports them to Prometheus format.
    """

    JenkinsExporter().run()


if __name__ == "__main__":
    main()
