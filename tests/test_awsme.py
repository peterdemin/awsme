#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `awsme` package."""

import pytest

from click.testing import CliRunner

from awsme import awsme
from awsme import cli



def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'awsme.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
