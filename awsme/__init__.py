"""CloudWatch metrics recorder

Usage:

    from awsme.factory import create_cloud_watch
    cloud_watch = create_cloud_watch()
    cloud_watch.log('name', dimensions={'key': 'dim'}, value=123)
"""
