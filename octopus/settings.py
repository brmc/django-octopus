#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

START_TAG = getattr(settings, "OCTOPUS_START_TAG", "<<<OCTOPUSDESTROYER!!!>>>")
END_TAG = getattr(settings, "OCTOPUS_END_TAG", START_TAG)

# Allows manual paths and potentially external URLS
ALLOW_MANUAL = getattr(settings, "OCTOPUS_ALLOW_MANUAL", True)

# Currently not being used
FAIL_SILENTLY = getattr(settings, "OCTOPUS_FAIL_SILENTLY", True)

__all__ = (ALLOW_MANUAL,)
