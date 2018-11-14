"""Metrics client factory"""

from typing import Dict, Optional

from .cloud_watch import CloudWatch
from .dummy import DummyCloudWatch
from .immediate_recorder import ImmediateRecorder
from .buffered_recorder import BufferedRecorder


def create_cloud_watch(namespace: str,
                       buffered: Optional[bool] = True,
                       dummy: Optional[bool] = False,
                       dimensions: Optional[Dict[str, str]] = None,
                       **kwargs
                       ) -> CloudWatch:
    """Create CloudWatch client using passed arguments"""
    if dummy:
        recorder_class = DummyCloudWatch
    else:
        recorder_class = (
            BufferedRecorder
            if buffered
            else ImmediateRecorder
        )
    return CloudWatch(
        namespace,
        dimensions or {},
        recorder_class,
        **kwargs
    )
