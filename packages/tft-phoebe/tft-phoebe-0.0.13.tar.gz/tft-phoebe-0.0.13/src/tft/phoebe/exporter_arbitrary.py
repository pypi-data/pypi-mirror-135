import argparse
import dataclasses

from . import Exporter, Metric

from prometheus_client import Gauge

from typing import Dict, Iterator


@dataclasses.dataclass
class MetricSandbox:
    labels: Dict[str, str]
    value: float


class ArbitraryExporter(Exporter):
    def create_args_parser(self, require_config: bool = True) -> argparse.ArgumentParser:
        parser = super(ArbitraryExporter, self).create_args_parser(require_config=False)

        parser.add_argument(
            '--gauge',
            required=False,
            metavar='NAME:LABEL1_NAME=LABEL1_VALUE,LABEL2_NAME=LABEL2_VALUE,...:VALUE',
            default=[],
            action='append',
            help='Add a gauge metric. Repeat LABEL_NAME[LABEL_VALUE]=VALUE to add metrics for each label and its values'
        )

        return parser

    def create_metric(self) -> Iterator[Metric]:
        for gauge_info in self.options.gauge:
            name, *values = gauge_info.split(':')

            sandboxes = []

            for value in values:
                sandbox = MetricSandbox(
                    labels={},
                    value=float('NaN')
                )

                sandboxes.append(sandbox)

                for label_info in value.split(','):
                    if '=' in label_info:
                        label_name, label_value = label_info.split('=', 1)

                        sandbox.labels[label_name.strip()] = label_value.strip()

                    else:
                        sandbox.value = float(label_info)

            label_names = list(set(sum(
                [list(sandbox.labels.keys()) for sandbox in sandboxes],
                []
            )))

            metric = Gauge(
                name.strip(), 'no help', label_names,
            )

            for sandbox in sandboxes:
                metric.labels(**sandbox.labels).set(sandbox.value)

            yield metric


def main() -> None:
    """
    Emit given arbitrary metrics.
    """

    ArbitraryExporter().run()


if __name__ == "__main__":
    main()
