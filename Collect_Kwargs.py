#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Collect_Kwargs.py
#   Written by Karl Debiec on 14-10-25, last updated by Karl Debiec on 15-01-03
"""
Decorator class to manage the selection of which keyword arguments to
pass to wrapped function

.. todo:
    - Check
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
import six
################################### CLASSES ####################################
class Collect_Kwargs(object):
    """
    Note: This is a decorator class with arguments. These use a
        different syntax from decorator classes without arguments. When
        the wrapped function is declared, __init__ and __call__ from
        the decorator are called sequentially. __init__ receives the
        arguments, while __call__ receives the function. __init__
        should (presumably) store the values of the arguments, while
        __call__ should prepare and return a wrapped function using
        their values.

    .. todo:
        - Does this actually need to accept arguments at declaration
          time? This seemed really useful initially but does not any
          longer.
    """
    def __init__(self, defaults = {}, default_pool_sources = []):
        """
        Stores defaults for wrapped function

        **Arguments:**
            :*defaults*: Default arguments to function
        """

        if isinstance(defaults, dict):
            self.defaults = defaults
        elif isinstance(defaults, six.string_types):
            import yaml

            if os.path.isfile(defaults):
                with file(defaults, "r") as infile:
                    self.defaults = yaml.load(defaults)
            else:
                self.defaults = yaml.load(defaults)

        self.default_pool_sources = default_pool_sources

    def __call__(self, function):
        """
        Wraps function

        **Arguments:**
            :*function*: function to wrap
        """

        def wrapped_function(kwarg_pool = {}, kwarg_pool_sources = None,
            *args_to_pass, **kwargs_from_call):
            """
            """
            if kwarg_pool_sources is None:
                kwarg_pool_sources = self.default_pool_sources

            kwargs_to_pass = self.defaults.copy()

            # Parse kwarg_pool
            if isinstance(kwarg_pool, dict):
                pass
            elif isinstance(kwarg_pool, six.string_types):
                import yaml

                if os.path.isfile(kwarg_pool):
                    with file(kwarg_pool, "r") as infile:
                        kwarg_pool = yaml.load(infile)
                else:
                    kwarg_pool = yaml.load(kwarg_pool)

            # Update kwargs from sources in kwarg_pool
            for source in kwarg_pool_sources:
                group = kwarg_pool
                for i, key in enumerate(source, -1 * len(source) + 1):
                    if str(key) in map(str, group.keys()) and i == 0:
                        try:
                            kwargs_from_source = group[key]
                        except KeyError:
                            try:
                                kwargs_from_source = group[str(key)]
                            except KeyError:
                                pass
                        break
                    elif str(key) in map(str, group.keys()):
                        try:
                            group = group[key]
                        except KeyError:
                            try:
                                group = group[str(key)]
                            except KeyError:
                                break
                    else:
                        kwargs_from_source = {}
                        break
                kwargs_to_pass.update(kwargs_from_source)

            kwargs_to_pass.update(kwargs_from_call)
            kwargs_to_pass["kwarg_pool"]         = kwarg_pool
            kwargs_to_pass["kwarg_pool_sources"] = kwarg_pool_sources

            return function(*args_to_pass, **kwargs_to_pass)

        return wrapped_function

