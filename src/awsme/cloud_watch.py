import datetime
import logging
from typing import Dict, Callable

import boto3

from .metric import Metric


logger = logging.getLogger(__name__)


class CloudWatch:
    """CloudWatch client, provides method log, that records metric
    using recorder_class instance.
    """

    def __init__(self,
                 namespace: str,
                 default_dimensions: Dict[str, str],
                 recorder_class: Callable,
                 **kwargs) -> None:
        client = boto3.client(
            'cloudwatch',
            **kwargs
        )
        self.default_dimensions = default_dimensions
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
