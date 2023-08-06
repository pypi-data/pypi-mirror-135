import argparse
import collections
import json
import re
import subprocess

from . import Exporter, Metric

from prometheus_client import Gauge

from typing import Any, Iterator, List


class OpenstackExporter(Exporter):
    def fetch_data(self) -> None:
        """
        Fetch a openstack data from server. ``self.data`` would become an object with following attributes:

        * ``limits: [{'Name': 'nameOfData', 'Value': 1024}, ...]``
        * ``instances: [{"Status": ..., "Name": ..., "Image": ..., "ID": ..., "Flavor": ..., "Networks": ...}, ...]``
        """

        self.data = argparse.Namespace()

        try:
            output = subprocess.Popen(
                self._get_command_openstack() + [
                    'limits',
                    'show',
                    '-f', 'json',
                    '--absolute',
                    '--reserved'
                ], stdout=subprocess.PIPE
            )

            self.data.limits = json.loads(output.communicate()[0])

            output = subprocess.Popen(
                self._get_command_openstack() + [
                    'server',
                    'list',
                    '-f', 'json'
                ], stdout=subprocess.PIPE
            )

            self.data.instances = json.loads(output.communicate()[0])

            output = subprocess.Popen(
                self._get_command_openstack() + [
                    'network',
                    'list',
                    '-f', 'json'
                ], stdout=subprocess.PIPE
            )

            networks = json.loads(output.communicate()[0])

            self.data.networks = {}

            for network in networks:
                if re.match(self.config['networks'], network['Name']) is None:
                    continue

                output = subprocess.Popen(
                    self._get_command_openstack() + [
                        'ip',
                        'availability',
                        'show',
                        '-f', 'json',
                        network['Name']
                    ], stdout=subprocess.PIPE
                )

                network_info = json.loads(output.communicate()[0])

                for subnet_info in network_info['subnet_ip_availability']:

                    if subnet_info['ip_version'] != '4':
                        continue

                    self.data.networks[network['Name']] = {
                        'total': float(subnet_info['total_ips']),
                        'used': float(subnet_info['used_ips'])
                    }

        except Exception:
            # Do not log Exception details, becuase it contains secret informations like a Openstack password!
            self.logger.error(
                "Phoebe Openstack: Can not fetch Openstack data."
            )
            raise

    def _get_command_openstack(self) -> List[str]:
        """
        It uses credentials from settings to create an Openstack client command-line.

        :returns: Shell command to login to Openstack
        """
        return [
            'openstack',
            f'--os-auth-url={self.config["client"]["os_auth_url"]}',
            f'--os-identity-api-version={self.config["client"]["os_identity_api_version"]}',
            f'--os-user-domain-name={self.config["client"]["os_user_domain_name"]}',
            f'--os-project-domain-name={self.config["client"]["os_project_domain_name"]}',
            f'--os-project-name={self.config["client"]["os_project_name"]}',
            f'--os-username={self.config["client"]["os_username"]}',
            f'--os-password={self.config["client"]["os_password"]}'
        ]

    def _extract_value(self, name: str) -> Any:
        """
        It extract value from a Openstack statistical data.

        :param name str: A name of specific value
        :returns: A value of a given name
        """
        return list(filter(lambda d: d['Name'] == name, self.data.limits))[0]['Value']

    def create_metric(self) -> Iterator[Metric]:
        """
        Generate Prometheus data for metrics. Definition of each metric is read from the configuration
        and yielded to the caller.
        """

        # Tenant usage metrics
        for metric_spes in self.config['metrics']:
            metric = Gauge(
                metric_spes['name'], metric_spes['help'], ['type'],
            )

            for metric_label in metric_spes['labels']:
                if self.data_fetch_failed:
                    value = float('NaN')

                else:
                    value = self._extract_value(metric_label['os-property'])
                    value *= float(metric_label.get('scale', 1))

                metric.labels(type=metric_label['type']).set(value)

            yield metric

        # Instance states metric
        state_counts = collections.Counter([
            instance['Status'].lower() for instance in self.data.instances
        ])

        metric = Gauge(
            'instance_states',
            'Number of instances in given state',
            ['state']
        )

        for state in self.config.get('expected-states', []):
            metric.labels(state=state.lower()).set(0.0)

        for state, count in state_counts.items():
            metric.labels(state=state).set(float(count))

        yield metric

        metric = Gauge(
            'network_ips',
            'Number of IP addresses in given network and state',
            ['network', 'type']
        )

        for network_name, network_info in self.data.networks.items():
            metric.labels(network=network_name.lower(), type='total').set(network_info['total'])
            metric.labels(network=network_name.lower(), type='used').set(network_info['used'])

        yield metric


def main() -> None:
    """
    Fetches metrics from Openstack and exports them to Prometheus format.
    """

    OpenstackExporter().run()


if __name__ == "__main__":
    main()
