# -*- coding: utf-8 -*-
#   myplotspec.manage_defaults_presets.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Decorator to manage the passage of defaults and available presets to a
method.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class manage_defaults_presets(object):
    """
    Decorator to manage the passage of defaults and available presets to
    a method.

    This decorator is a partner to
    :class:`~.manage_kwargs.manage_kwargs`, desiged to allows its use
    for methods of objects containg central ``defaults`` and
    ``available_presets`` attributes. It obtains available defaults and
    presets for the wrapped method from their central location in the
    host object, and passes on those applicable to the wrapped method.
    :class:`~.manage_kwargs.manage_kwargs` then selects arguments to
    pass from among the provided defaults, available and selected
    presets, YAML file, and arguments provided at call time.

    Defaults are accessed from the host object's instance (or class)
    variable ``self.defaults``, and may be a dict, a path to a YAML
    file, or a YAML string. Outer level (of indentation or keys)
    provides function names, and inner level provides default arguments
    to each function::

        defaults = \"\"\"
            method_1:
                method_1_arg_1: 1000
                method_1_arg_2: abcd
            method_2
                method_2_arg_1: 2000
                method_2_arg_2: efgh
            ...
        \"\"\"

    Presets are accessed from the host objects's instance (or class)
    variable ``self.available_presets``, in the same formats as
    ``self.defaults``. Presets contain an outer level of keys providing
    the names of available presets::

        available_presets = \"\"\"
            preset_1:
                method_1:
                    method_1_arg_1: 1001
                    method_1_arg_2: abcde
                method_2
                    method_2_arg_1: 2001
                    method_2_arg_2: efghi
            preset_2:
                method_1:
                    method_1_arg_1: 1002
                    method_1_arg_2: abcdef
                method_2
                    method_2_arg_1: 2002
                method_2_arg_2: efghij
        \"\"\"

    When this decorator is used to wrap a method of a class, it adds to
    the arguments being passed ``defaults``, containing the defaults
    specified for the method, and ``available_presets``, containing only
    the presets applicable to the method::

        @manage_defaults_presets()
        def method_1(*args, **kwargs):
            print(kwargs)
            ...

        {
            'defaults': {
                'method_1_argument_1': 1000,
                'method_1_argument_2': 'asdf'
            },
            'presets': {
                'preset_1': {
                    'method_1_argument_1': 1001,
                    'method_1_argument_2': 'asde'
                },
                'preset_1': {
                    'method_1_argument_1': 1002,
                    'method_1_argument_2': 'asdef'
                }
            },
            ...
        }

    Attributes:
      verbose (int): Level of verbose output
      debug (int): Level of debug output
    """

    def __init__(self, verbose=1, debug=0):
        """
        Stores arguments provided at decoration.

        Arguments:
          verbose (int): Level of verbose output
          debug (int): Level of debug output
        """
        self.verbose = verbose
        self.debug = debug

    def __call__(self, method):
        """
        Wraps method.

        Arguments:
          method (method): method to wrap

        Returns:
          (method): Wrapped method
        """
        from functools import wraps

        decorator = self
        self.method = method

        @wraps(method)
        def wrapped_method(self, *in_args, **in_kwargs):
            """
            Wrapped version of method

            Arguments:
              in_args (tuple): Arguments passed to function
              in_kwargs (dict): Keyword arguments passed to function

            Returns:
              Return value of wrapped function
            """
            from copy import copy
            from . import get_yaml
            from .debug import db_s

            db = max(in_kwargs.get("debug", 0), decorator.debug,
                  self.debug if hasattr(self, "debug") else 0)
            if db >= 1:
                db_s("Managing defaults and presets for method " +
                  "'{0}' ".format(method.__name__,
                  "of class '{0}':".format(type(self).__name__)))

            out_args   = copy(in_args)
            out_kwargs = copy(in_kwargs)

            # Manage defaults
            if hasattr(self, "defaults"):
                in_defaults = get_yaml(self.defaults)
                if method.__name__ in in_defaults:
                    if db >= 1:
                        db_s("defaults available", 1)
                    out_kwargs["defaults"] = in_defaults[method.__name__]
                else:
                    if db >= 1:
                        db_s("defaults unavailable for this method", 1)
            else:
                if db >= 1:
                    db_s("defaults unavailable for this class", 1)

            # Manage presets
            out_presets = {}
            if hasattr(self, "available_presets"):
                available_presets = get_yaml(self.available_presets)
                for preset_name in sorted(available_presets):
                    preset = available_presets[preset_name]
                    if method.__name__ in preset:
                        if db >= 1:
                            db_s("preset '{0}'".format(preset_name) +
                                 " available", 1)
                        out_presets[preset_name] = preset[method.__name__]
                    else:
                        if db >= 1:
                            db_s("preset '{0}'".format(preset_name) +
                                 " unavailable for this method", 1)
            else:
                if db >= 1:
                    db_s("presets unavailable for this class", 1)
            out_kwargs["available_presets"] = out_presets

            return method(self, *out_args, **out_kwargs)

        return wrapped_method
