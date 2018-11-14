"""Console script for awsme."""

import sys
import click
import logging
from .factory import create_cloud_watch


@click.command()
def main():
    """Send test metric to AWS CloudWatch"""
    logging.basicConfig(level=logging.DEBUG)
    cloud_watch = create_cloud_watch(
        'Test Namespace',
        buffered=False,
        dummy=False,
        dimensions={'By intent': 'Test'},
    )
    cloud_watch.log('awsme-test', {'By source': 'awsme'})
    print('Successfully sent metric "awsme-test" to "Test Namespace"')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
