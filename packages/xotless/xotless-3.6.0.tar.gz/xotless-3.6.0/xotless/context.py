#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import contextlib

from xotl.tools.context import context


def ReentrantContext(context_identifier):
    """Return a reentrant context manager.

    Entering a reentrant context the first time setups a dictionary that is
    shared with all nested entries to the same context.

    Examples:

       >>> CONTEXT1 = ReentrantContext(object())
       >>> with CONTEXT1() as d1:
       ...    with CONTEXT1() as d2:
       ...        assert d1 is d2

    However, non-nested entries to the context share no common dictionary:

       >>> CONTEXT1 = ReentrantContext(object())
       >>> with CONTEXT1() as d1:
       ...     pass

       >>> with CONTEXT1() as d2:
       ...     pass

       >>> assert d1 is not d2

    """

    @contextlib.contextmanager
    def reentrant_context():
        ctx = context[context_identifier]
        if ctx:
            yield ctx["memory"]
        else:
            with context(context_identifier, memory={}) as ctx:
                yield ctx["memory"]

    return reentrant_context
