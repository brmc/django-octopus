#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2014 Brian McClure
#
#  django-octopus is free software under terms of the MIT License.
#

from setuptools import setup, find_packages

description = """"""

setup(
    name='django-octopus',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 2.7)', 'python (>= 3.3)', 'django (>= 1.6)'],
    description='A simple AJAX pull framework for django, now with full' \
                'featured demo',
    author='Brian McClure',
    author_email='brian@mcclure.pw',
    url='https://github.com/brmc/django-octopus',
    download_url='https://github.com/brmc/django-octopus.git',
    license='MIT License',
    keywords='django, ajax, front-end, pull',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
