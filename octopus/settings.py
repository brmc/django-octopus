#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

# Allows manual paths and potentially external URLS
ALLOW_MANUAL = getattr(settings, "OCTOPUS_ALLOW_MANUAL", True)

__all__ = (ALLOW_MANUAL,)
