#!/usr/bin/env python
# -*- coding: utf-8 -*-

from octopus.templatetags.tentacles import *

raise DeprecationWarning("{% load a %} is deprecated.  Please use " \
    "{% load tentacles %} instead")