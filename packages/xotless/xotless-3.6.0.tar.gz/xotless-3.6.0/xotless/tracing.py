#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import contextlib
from functools import partial

try:
    from sentry_sdk import Hub

    def sentry_span(module, description, **tags):
        hub = Hub.current
        span = hub.start_span(op=module, description=description)
        for tag, value in tags.items():
            span.set_tag(tag, value)
        return span


except ImportError:

    @contextlib.contextmanager
    def sentry_span(module, description, **tags):
        yield


def get_module_sentry_spanner(module):
    """Return a function to create Sentry spans for `module`.

    Usage:

       >>> sentry_span = get_module_sentry_spanner(__name__)       # doctest: +SKIP
       >>> with sentry_span("function_name_or_whatever", **tags):  # doctest: +SKIP
       ...    pass

    """
    return partial(sentry_span, module)
