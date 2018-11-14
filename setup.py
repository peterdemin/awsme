#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    README = readme_file.read()


with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()


with open(os.path.join('requirements', 'base.in')) as fp:
    REQUIREMENTS = list(fp)


setup(
    author="Peter Demin",
    author_email='peterdemin@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    description="AWS CloudWatch client library to send "
                "metrics conviniently and efficiently",
    entry_points={
        'console_scripts': [
            'awsme-test=awsme.cli:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords='awsme',
    name='awsme',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/peterdemin/awsme',
    version='0.1.3',
    zip_safe=False,
)
