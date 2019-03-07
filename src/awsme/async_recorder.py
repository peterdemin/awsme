from queue import Queue, Full, Empty
from threading import Thread
from typing import Optional  # noqa

from .metric import Metric


class AsyncRecorder:
    """Offload actual sending to a thread"""

    def __init__(self, recorder) -> None:
        self._recorder = recorder
        self._queue = Queue(maxsize=1000)  # type: Queue
        self._thread = None  # type: Optional[Thread]
        self._start()

    def put_metric(self, metric: Metric) -> None:
        """Enqueue metric for sending in the background."""
        try:
            self._queue.put(metric, block=False)
        except Full:
            # ignore metric if queue is full:
            pass

    def flush(self, complete: bool = True) -> None:
        """Flushes the contained recorder"""
        self._recorder.flush(complete=complete)

    def _start(self):
        """Start sending thread"""
        if self._thread is not None:
            raise RuntimeError("Attempted to start AsyncRecorder twice")
        self._thread = Thread(target=self._background_send)
        self._thread.daemon = True
        self._thread.start()

    def _background_send(self):
        """Send metrics through actual recorder."""
        for metric in self._pending_metrics():
            self._recorder.put_metric(metric)

    def _pending_metrics(self):
        """Infinite metrics generator."""
        while True:
            try:
                metric = self._queue.get(block=True)
            except Empty:
                return
            try:
                yield metric
            finally:
                self._queue.task_done()
