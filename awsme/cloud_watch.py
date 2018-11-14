import datetime
import logging

import boto3

from .metric import Metric


logger = logging.getLogger(__name__)


class CloudWatch:
    """CloudWatch client, provides method log, that records metric
    using recorder_class instance.
    """

    def __init__(self, namespace, task_name, recorder_class) -> None:
        client = boto3.client(
            'cloudwatch',
            region_name='ap-northeast-1',
        )
        self.default_dimensions = {'task': task_name}
        self._recorder = recorder_class(namespace, client)

    def log(self, name, dimensions=None, value=1, **kwargs) -> None:
        """Record metric.

        ``dimensions`` are merged with default_dimensions.
        Keyword arguments are passed to Metric constructor.
        """
        complete_dimensions = self.default_dimensions.copy()
        complete_dimensions.update(dimensions or {})
        self._record_metric(Metric(
            event_time=datetime.datetime.utcnow(),
            name=name,
            value=value,
            dimensions=complete_dimensions,
            **kwargs,
        ))

    def _record_metric(self, metric: Metric) -> None:
        logger.debug('log: %r', metric)
        self._recorder.put_metric(metric)
