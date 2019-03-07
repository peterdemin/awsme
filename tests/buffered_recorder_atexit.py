from __future__ import print_function

import datetime

from awsme.metric import Metric
from awsme.buffered_recorder import BufferedRecorder
from typing import List, Dict, Any  # noqa

class StdoutRecorder:

    def put_metric_data(self, metric_data: List[Dict[str, Any]]) -> None:
        print(metric_data)

recorder = BufferedRecorder(recorder=StdoutRecorder())
recorder.put_metric(
    Metric(
        event_time=datetime.datetime.min,
        name="1",
        dimensions={},
    )
)
print("Exiting")
