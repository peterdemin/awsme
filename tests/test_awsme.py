#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `awsme` package."""

from click.testing import CliRunner
from moto import mock_cloudwatch

from awsme.cli import main
from awsme import create_cloud_watch


@mock_cloudwatch
def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert 'Successfully sent metric' in result.output
    help_result = runner.invoke(main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


@mock_cloudwatch
def test_put_metric():
    cloud_watch = create_cloud_watch(
        'Test Namespace',
        buffered=False,
        dummy=False,
        dimensions={'By intent': 'Test'},
    )
    cloud_watch.log('awsme-test', {'By source': 'awsme'})
