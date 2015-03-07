#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


TRUE_SETTINGS = [
    'ALLOW_MANUAL',     # Allows manual paths and potentially external URLS
    'FAIL_SILENTLY',    # Currently not being used
]

# FALSE_SETTINGS = []

for setting in TRUE_SETTINGS:
    locals()[setting] = getattr(settings, "OCTOPUS_%s" % setting, True)
