import os
import argparse
import json
import subprocess

from . import Exporter, Metric

from prometheus_client import Gauge

from typing import Iterator, List


class AWSExporter(Exporter):
    def fetch_data(self) -> None:
        """
        Fetch an AWS data from server through aws cli.
        """

        self.data = argparse.Namespace()

        # aws cli has no argumetns for providing credential
        # to workaround this we can provide them as command line envvars
        self.env = os.environ.copy()
        self.env["AWS_ACCESS_KEY_ID"] = f'{self.config["client"]["aws_access_key"]}'
        self.env["AWS_SECRET_ACCESS_KEY"] = f'{self.config["client"]["aws_secret_key"]}'

        try:
            output = subprocess.Popen(
                self._get_command_aws() + [
                    'describe-subnets'
                ], stdout=subprocess.PIPE, env=self.env
            )

            subnets = json.loads(output.communicate()[0])

            self.data.networks = {}

            for subnet in subnets["Subnets"]:
                if subnet["SubnetId"] == f'{self.config["client"]["aws_subnet_id"]}':
                    self.data.networks[f'{self.config["client"]["aws_subnet_id"]}'] = {
                        'available': float(subnet["AvailableIpAddressCount"])
                    }

            output = subprocess.Popen(
                self._get_command_aws() + [
                    'describe-instances'
                ], stdout=subprocess.PIPE, env=self.env
            )

            instances = json.loads(output.communicate()[0])
            self.data.instances = {
                'using': len(instances["Reservations"])
            }

        except Exception:
            # Do not log Exception details, becuase it contains secret informations like a Openstack password!
            self.logger.error(
                "Phoebe AWS: Can not fetch AWS data."
            )
            raise

    def _get_command_aws(self) -> List[str]:
        """
        It uses credentials from settings to create an AWS client command-line.

        :returns: Shell command to login to AWS
        """
        return [
            'aws',
            '--no-paginate',
            '--output=json',
            f'--region={self.config["client"]["aws_region"]}',
            'ec2'
        ]

    def create_metric(self) -> Iterator[Metric]:
        """
        Generate Prometheus data for metrics. Definition of each metric is read from the configuration
        and yielded to the caller.
        """

        metric = Gauge(
            'instances',
            'Number of instances',
            ['type']
        )
        metric.labels(type='using').set(self.data.instances['using'])

        yield metric

        metric = Gauge(
            'network_ips',
            'Number of IP addresses in given network and state',
            ['network', 'type']
        )

        for network_name, network_info in self.data.networks.items():
            metric.labels(network=network_name.lower(), type='available').set(network_info['available'])

        yield metric


def main() -> None:
    """
    Fetches metrics from AWS and exports them to Prometheus format.
    """

    AWSExporter().run()


if __name__ == "__main__":
    main()
