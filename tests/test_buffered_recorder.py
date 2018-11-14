import datetime
import logging
from unittest import mock

from awsme.immediate_recorder import ImmediateRecorder
from awsme.metric import Metric
from awsme.buffered_recorder import (
    BufferedRecorder,
    PAGE_SIZE,
    MAX_BATCH_SIZE,
    MAX_BUFFER_SIZE,
)


def test_buffered_recorder_buffers_incomplete_page():
    _, fake_recorder = make_recorder(10)
    assert fake_recorder.called == 0


def test_buffered_recorder_flushes_full_page():
    _, fake_recorder = make_recorder(25)
    fake_recorder.put_metric_data.assert_called_once()
    assert len(fake_recorder.put_metric_data.call_args[0][0]) == PAGE_SIZE


def test_buffered_recorder_rate_control(caplog):
    with caplog.at_level(logging.WARNING):
        _, fake_recorder = make_recorder(MAX_BUFFER_SIZE)
    assert len(caplog.records) == 1
    assert fake_recorder.put_metric_data.call_count == MAX_BATCH_SIZE


def test_buffered_recorder_complete_flush_keeps_nothing():
    recorder, fake_recorder = make_recorder(MAX_BUFFER_SIZE)
    recorder.flush()
    assert fake_recorder.put_metric_data.call_count == MAX_BUFFER_SIZE // PAGE_SIZE


def make_recorder(dimensions_count):
    fake_recorder = mock.Mock(spec=ImmediateRecorder)
    recorder = BufferedRecorder(recorder=fake_recorder)
    recorder.put_metric(Metric(
        datetime.datetime.utcnow(),
        'test',
        {str(number): str(number)
         for number in range(dimensions_count)},
    ))
    return recorder, fake_recorder
