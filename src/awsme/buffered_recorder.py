"""Buffering recorder"""

import atexit
from itertools import count
import logging
from typing import List, Dict, Any  # noqa

from .immediate_recorder import ImmediateRecorder
from .metric import Metric


logger = logging.getLogger(__name__)
PAGE_SIZE = 20
MAX_BATCH_SIZE = 5
MAX_BUFFER_SIZE = PAGE_SIZE * MAX_BATCH_SIZE * 10


class BufferedRecorder:
    """Accumulate metrics in buffer and send them in pages"""

    def __init__(self, *args, recorder=None, **kwargs) -> None:
        self._recorder = recorder or ImmediateRecorder(*args, **kwargs)
        self._buffer = []  # type: List[Dict[str, Any]]
        atexit.register(self.flush) # ensure that we flush before we depart this earth

    def put_metric(self, metric: Metric) -> None:
        """Add metric_data to buffer. Send full pages"""
        metric_data = metric.to_metric_data()
        space_left = MAX_BUFFER_SIZE - len(self._buffer)
        if len(metric_data) > space_left:
            logger.warning(
                "Dropping %d metrics, that don't fit into buffer",
                space_left - len(metric_data),
            )
            metric_data = metric_data[:space_left]
        self._buffer += metric_data
        self.flush(complete=False)

    def flush(self, complete: bool = True) -> None:
        '''Sends as much data as possible to CloudWatch.

        If complete is set to False, this only sends at most MAX_BATCH_SIZE full pages.
        Otherwise it sends all buffered pages, even last incomplete page.
        This way, it minimizes the API usage at the cost of delaying data.
        '''
        batches = (
            count()
            if complete
            else range(MAX_BATCH_SIZE)
        )
        for _ in batches:
            page = self._pop_batch(partial=complete)
            if page:
                self._recorder.put_metric_data(page)
            else:
                break

    def _pop_batch(self, partial: bool = True):
        """Pop first page from buffer.

        If there are no pages available, return empty list.
        if partial is True, return even incomplete page.
        """
        if partial or len(self._buffer) >= PAGE_SIZE:
            page = self._buffer[:PAGE_SIZE]
            self._buffer = self._buffer[PAGE_SIZE:]
            return page
        return []
