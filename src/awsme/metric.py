import datetime
from typing import List, Dict, Any

import attr


@attr.s(auto_attribs=True)
class Metric:
    """Metric data-class"""

    event_time: datetime.datetime
    name: str
    dimensions: Dict[str, str]
    value: float = 1
    unit: str = 'Count'
    storage_resolution: int = 60

    def to_metric_data(self) -> List[Dict[str, Any]]:
        """Return list of metrics in AWS CloudWatch format"""
        data = [
            self._format_single_metric({key: value})
            for key, value in self.dimensions.items()
        ]
        data.append(self._format_single_metric(self.dimensions))
        return data

    def _format_single_metric(self, dimensions: Dict[str, str]) -> Dict[str, Any]:
        timestamp = self.event_time.strftime(
            '%Y-%m-%d %H:%M:%S.%f UTC'
        )
        value = float(self.value)
        cw_dimensions = [
            {'Name': key, 'Value': value}
            for key, value in dimensions.items()
        ]
        return {
            'MetricName': self.name,
            'Dimensions': cw_dimensions,
            'Timestamp': timestamp,
            'Value': value,
            'Unit': self.unit,
            'StorageResolution': self.storage_resolution,
        }
