#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


TRUE_SETTINGS = [
    'ALLOW_MANUAL',     # Allows manual paths and potentially external URLS
    'FAIL_SILENTLY',    # Currently not being used
]

# FALSE_SETTINGS = []

START_TAG = getattr(settings, "OCTOPUS_START_TAG", "<<<OCTOPUSDESTROYER!!!>>>")
END_TAG = getattr(settings, "OCTOPUS_END_TAG", START_TAG)

for setting in TRUE_SETTINGS:
    locals()[setting] = getattr(settings, "OCTOPUS_%s" % setting, True)


__all__ = TRUE_SETTINGS