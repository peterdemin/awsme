"""Metrics client factory"""

from typing import Dict, Optional

from .cloud_watch import CloudWatch
from .dummy import DummyCloudWatch
from .immediate_recorder import ImmediateRecorder
from .buffered_recorder import BufferedRecorder
from .async_recorder import AsyncRecorder


def create_cloud_watch(namespace: str,
                       asynchronous: Optional[bool] = True,
                       buffered: Optional[bool] = True,
                       dummy: Optional[bool] = False,
                       dimensions: Optional[Dict[str, str]] = None,
                       **kwargs
                       ) -> CloudWatch:
    """Create CloudWatch client using passed arguments"""
    return CloudWatch(
        namespace,
        dimensions or {},
        recorder_factory(asynchronous, buffered, dummy),
        **kwargs
    )


def recorder_factory(asynchronous: Optional[bool] = True,
                     buffered: Optional[bool] = True,
                     dummy: Optional[bool] = False):
    def create_recorder(namespace, client):
        if dummy:
            return DummyCloudWatch()
        recorder = ImmediateRecorder(
            namespace=namespace,
            client=client,
        )
        if buffered:
            recorder = BufferedRecorder(recorder=recorder)
        if asynchronous:
            recorder = AsyncRecorder(recorder)
        return recorder
    return create_recorder
