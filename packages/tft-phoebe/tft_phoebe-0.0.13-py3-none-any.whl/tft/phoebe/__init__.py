import argparse
import sys
import logging
import time

from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.metrics import MetricWrapperBase as Metric
from prometheus_client.metrics import Gauge
import ruamel.yaml
import stackprinter

from typing import Any, Dict, Iterator, List

SettingsType = Dict[str, Any]


class Exporter:
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.data_fetch_failed = False

        now = time.time()

        self._start = now
        self._data_fetch_start = now
        self._data_fetch_end = now
        self._end = now

    def create_args_parser(self, require_config: bool = True) -> argparse.ArgumentParser:
        """
        Create and return a parser for command-line options. The parser is already set to accept
        common, shared options ``--config``, ``--export``, ``--log-file`` and ``--verbose``.
        """

        args_parser = argparse.ArgumentParser()

        args_parser.add_argument(
            "--config", "-c",
            required=require_config,
            metavar="FILE",
            help="Path to plugin's YAML config file."
        )

        args_parser.add_argument(
            "--export", "-e",
            required=True,
            metavar="FILE",
            help="Path to the output file. Use '-' for standard output instead of a file."
        )

        args_parser.add_argument(
            "--log-file", "-l",
            default="-",
            required=False,
            metavar="FILE",
            help="Path to the log file. Default value '-' is stderr."
        )

        args_parser.add_argument(
            "--verbose", "-v",
            required=False,
            action="store_true",
            help="Increase verbosity"
        )

        args_parser.add_argument(
            '--include-batch-metrics', '-B',
            action='store_true',
            required=False,
            help='If set, Phoebe will add metrics for timestamps marking exporter stages.'
        )

        args_parser.add_argument(
            '--batch-metric-started',
            required=False,
            default='phoebe_start_time_seconds',
            help='Name of the metric providing timestamp of exporter start.'
        )

        args_parser.add_argument(
            '--batch-metric-finished',
            required=False,
            default='phoebe_end_time_seconds',
            help='Name of the metric providing timestamp of exporter exit.'
        )

        args_parser.add_argument(
            '--batch-metric-fetch-started',
            required=False,
            default='phoebe_start_fetch_time_seconds',
            help='Name of the metric providing timestamp of data fetch start.'
        )

        args_parser.add_argument(
            '--batch-metric-fetch-finished',
            required=False,
            default='phoebe_end_fetch_time_seconds',
            help='Name of the metric providing timestamp of data fetch exit.'
        )

        return args_parser

    def parse_args(self) -> argparse.Namespace:
        """
        Parse command-line arguments.

        Common options ``--config``, ``--export``, ``--log-file`` and ``--verbose`` are consumed immediately.
        """

        parser = self.create_args_parser()

        self.options = options = parser.parse_args()

        self.config_filepath = options.config
        self.export_filepath = options.export

        # Setup up logging errors to file or on stderr. Default error output is printed on stderr.
        if options.log_file == '-':
            log_handler = logging.StreamHandler()
        else:
            log_handler = logging.FileHandler(options.log_file, encoding="utf-8")
        log_handler.setFormatter(
            logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S"
            )
        )
        self.logger.addHandler(log_handler)
        self.logger_verbose = options.verbose

        if self.options.config:
            try:
                with open(options.config) as f:
                    self.config = ruamel.yaml.YAML().load(f)
            except Exception as exc:
                self.logger.critical(f"Can not open phoebe config file '{options.config}' \n\t\t{exc}")

                sys.exit(1)

        else:
            self.config = {}

        return options

    def fetch_data(self) -> None:
        """
        This method is responsible for acquiring data the exporter needs to emit metrics.

        If this method raises an exception, ``data_fetch_failed`` property of the instance is set to ``True``.
        """

        pass

    def create_metric(self) -> Iterator[Metric]:
        """
        This method is expected to yield one metric every time is called, or return when exporter
        runs out of metrics to export.
        """

        # This method is supposed to be a generator, overriden by child classes. We want to provide a default
        # behavior, which would be an "empty" iterator - when called, this method should yield no entries,
        # iteration over it should end immediately. This is achieved by doing nothing and calling `return`
        # right away.
        #
        # But `return` alone is not enough - this function must be a generator, and generator must have `yield`.
        # So, adding `yield` - and the order is important, `return` must go first. Othwerwise, `yield` would
        # actually yielded an item, `None`, but as said above, this generator is supposed to be empty.
        #
        # So, `return` to quit the generator, and `yield` to "trick" Python to treating this method as
        # a generator. The `yield` is never used, all calls end with `return`, but it's present.
        return
        yield

    def _create_source_reachable_metric(self, value: int) -> Gauge:
        metric = Gauge(
            'phoebe_source_reachable',
            'Whether or not the data were fetched successfully'
        )

        metric.set(value)

        return metric

    def _create_batch_metrics(self) -> List[Gauge]:
        if not self.options.include_batch_metrics:
            return []

        metrics_info = [
            (self.options.batch_metric_started, 'Timestamp of the exporter start', self._start),
            (self.options.batch_metric_finished, 'Timestamp of the exporter exit', self._end),
            (self.options.batch_metric_fetch_started, 'Timestamp of the data fetch start', self._data_fetch_start),
            (self.options.batch_metric_fetch_finished, 'Timestamp of the exporter exit', self._data_fetch_end)
        ]

        metrics = [
            Gauge(name, help_string) for name, help_string, _ in metrics_info
        ]

        for metric, (_, _, value) in zip(metrics, metrics_info):
            metric.set(value)

        return metrics

    def collect_metrics(self) -> CollectorRegistry:
        """
        Main workhorse: calls ``create_metric`` as long as necessary, adds gained metrics to a registry,
        and returns the registry.
        """

        registry = CollectorRegistry()

        for metric in self.create_metric():
            registry.register(metric)

        registry.register(self._create_source_reachable_metric(0 if self.data_fetch_failed else 1))

        self._end = time.time()

        for metric in self._create_batch_metrics():
            registry.register(metric)

        return registry

    def export_metrics(self, registry: CollectorRegistry) -> None:
        exported = generate_latest(registry)

        if self.export_filepath == '-':
            sys.stdout.write(exported.decode('utf-8'))

        else:
            with open(self.export_filepath, 'w') as f:
                f.write(exported.decode('utf-8'))

    def run(self) -> None:
        self.parse_args()

        self._data_fetch_start = time.time()

        try:
            self.fetch_data()

        except Exception as exc:
            self.data_fetch_failed = True

            self.logger.error(f'Failed to fetch data: {exc}')
            if self.logger_verbose:
                self.logger.error(stackprinter.format_current_exception())

        finally:
            self._data_fetch_end = time.time()

        try:
            registry = self.collect_metrics()

        except Exception as exc:
            self.logger.critical(f'Failed to collect metrics: {exc}')
            if self.logger_verbose:
                self.logger.critical(stackprinter.format_current_exception())

            sys.exit(1)

        try:
            self.export_metrics(registry)

        except Exception as exc:
            self.logger.critical(f'Failed to export metrics: {exc}')
            if self.logger_verbose:
                self.logger.critical(stackprinter.format_current_exception())

            sys.exit(1)
