import datetime

from awsme.metric import Metric


def test_sample_metric_formatting():
    metric = Metric(
        event_time=datetime.datetime(2014, 4, 14, 14, 4, 14),
        name='app-start',
        dimensions={
            'app': 'makar',
            'config': 'alpha-bch-x8-taker',
        },
    )
    data = metric.to_metric_data()
    assert data == [
        {
            'Dimensions': [
                {'Name': 'app', 'Value': 'makar'},
            ],
            'MetricName': 'app-start',
            'StorageResolution': 60,
            'Timestamp': '2014-04-14 14:04:14.000000 UTC',
            'Unit': 'Count',
            'Value': 1.0
        },
        {
            'Dimensions': [
                {'Name': 'config', 'Value': 'alpha-bch-x8-taker'},
            ],
            'MetricName': 'app-start',
            'StorageResolution': 60,
            'Timestamp': '2014-04-14 14:04:14.000000 UTC',
            'Unit': 'Count',
            'Value': 1.0
        },
        {
            'Dimensions': [
                {'Name': 'app', 'Value': 'makar'},
                {'Name': 'config', 'Value': 'alpha-bch-x8-taker'},
            ],
            'MetricName': 'app-start',
            'StorageResolution': 60,
            'Timestamp': '2014-04-14 14:04:14.000000 UTC',
            'Unit': 'Count',
            'Value': 1.0
        }
    ]
