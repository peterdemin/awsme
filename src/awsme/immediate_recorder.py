import logging
from typing import List, Dict, Any

from .metric import Metric


logger = logging.getLogger(__name__)


class ImmediateRecorder:
    """Simple metric recorder that sends metric data immediately"""

    def __init__(self, namespace: str, client: Any) -> None:
        self._namespace = namespace
        self._client = client

    def put_metric(self, metric: Metric) -> None:
        """Convert Metric instance to AWS format and send."""
        self.put_metric_data(metric.to_metric_data())

    def flush(self, complete: bool = True) -> None:
        """Does nothing, as recording is immediate"""
        pass

    def put_metric_data(self, metric_data: List[Dict[str, Any]]) -> None:
        """Send metric data to boto3 client."""
        logger.debug('put metric data: %r', metric_data)
        self._client.put_metric_data(
            Namespace=self._namespace,
            MetricData=metric_data,
        )
