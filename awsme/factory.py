import os
import sys
import argparse
from typing import Dict, Optional

from .cloud_watch import CloudWatch
from .dummy import DummyCloudWatch
from .buffered_recorder import BufferedRecorder


def create_cloud_watch(namespace: str,
                       buffered: Optional[bool] = True,
                       dimensions: Optional[Dict[str, str]] = None,
                      ) -> CloudWatch:
    return CloudWatch(namespace, task_name, BufferedRecorder)


def get_task_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', help='a path to configuration file')
    args = parser.parse_args()
    file_path = args.config
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    return base_name.lstrip('config_')
