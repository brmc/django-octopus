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
    name     = 'django-octopus',
    version  = '0.2',
    packages = find_packages(),
    include_package_data=True,
    requires = ['python (2.7, 3.3, 3.4)', 'django (>= 1.5)'],
    description  = 'A simple AJAX pull framework for django',
    author       = 'Brian McClure',
    author_email = 'brian.mcclr@gmail.com',
    url          = 'https://github.com/brmc/django-octopus',
    download_url = 'https://github.com/brmc/django-octopus.git',
    license      = 'MIT License',
    keywords     = 'django, ajax, front-end, pull',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
