===============================================
Amazon Web Services Cloud Watch Metrics Library
===============================================


.. image:: https://img.shields.io/pypi/v/awsme.svg
        :target: https://pypi.python.org/pypi/awsme

.. image:: https://img.shields.io/travis/peterdemin/awsme.svg
        :target: https://travis-ci.org/peterdemin/awsme

.. image:: https://pyup.io/repos/github/peterdemin/awsme/shield.svg
     :target: https://pyup.io/repos/github/peterdemin/awsme/
     :alt: Updates

Configurable client library, that supports asynchronous and buffered sending of
AWS cloud watch metrics.

Installation
------------

By default awsme is installed without ``boto3`` dependency to make it deploy
faster in AWS Lambda environment (See `#3 <https://github.com/peterdemin/awsme/issues/3>` for details).

If you run awsme outside of Lambda, use following command to activate ``boto3`` dependency::

    pip install awsme[boto3]

Usage
-----

.. code-block:: python
    
    from awsme import create_cloud_watch
    cloud_watch = create_cloud_watch(
        namespace='Application',
        dimensions={'version': '1.0.0'},
    )
    cloud_watch.log('metric', dimensions={'key': 'dim'}, value=123)

Create Options
--------------

``create_cloud_watch`` accepts following arguments:

* asynchronous (optional bool): if True (default), send metrics from a separate thread.
* buffered (optional bool): if True (default), metrics will be accumulated in a buffer and sent in batches.
* dummy (optional bool): if True, ignore two previous options and create dummy recorder. False by default.
* dimensions: (optional Dict[str, str]): dictionary of default dimensions, that will be attached to all metrics.
* All other kwargs will be bypassed to ``boto3.client('cloudwatch', **kwargs)``

Log Options
-----------

CloudWatch, returned by ``create_cloud_watch`` has two public methods. The primary method is ``log``.
It's arguments:

* name (required str): name of the metric.
* dimensions (optional Dict[str, str]): additional dimensions,
  that will be added to default dimension from factory.
* value (optional float): metric's value, 1 by default.
* unit (optional str): metric unit, e.g. Count, Seconds, Bytes,
  see `AWS docs`_ for a complete list of valid values.
* storage_resolution (optional int): metric storage resolution in seconds, 60 by default.

Flushing
--------

If ``create_cloud_watch`` was called with ``buffered=True`` (default) then you may want to forcefully 
flush the internal metrics buffer. 
In a standard application this will likely not be necessary, as the buffer will auto-flush ``atexit``.
However, if your application is running as an AWS Lambda function, the execution of the Lambda function
will be "frozen" when the function completes, preventing exiting and thus flushing. In this use case, 
you will need to forcibly flush the buffer by calling ``flush``.
It's argument:

* complete (optional bool): if True (default), perform a complete flush.

AWS configuration
-----------------

Awsme uses boto3 library, that takes configuration from `environment variables`_
and configuration files.
To check, that you have everything configured properly to send metrics, use included command-line tool:

.. code-block::

    $ awsme-test
    ...
    Successfully sent metric "awsme-test" to "Test Namespace"


Credits
-------

This package was created with Cookiecutter_ and the `elgertam/cookiecutter-pipenv`_ project template, based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elgertam/cookiecutter-pipenv`: https://github.com/elgertam/cookiecutter-pipenv
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`AWS docs`: https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html
.. _`environment variables`: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variables
