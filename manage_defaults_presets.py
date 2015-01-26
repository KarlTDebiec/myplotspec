# -*- coding: utf-8 -*-
#   myplotspec.manage_defaults_presets.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Decorator to manage the passage of defaults and presets to a method.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class manage_defaults_presets(object):
    """
    Decorator to manage the passage of defaults and presets to a method.

    This decorator is a partner to
    :class:`~.manage_kwargs.manage_kwargs`, desiged to allows its use
    for methods of objects containg central ``defaults`` and ``presets``
    attributes. It obtains available defaults and presets for the
    wrapped method from their central location in the host object, and
    passes on those applicable to the wrapped method.
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
    variable ``self.presets``, in formats analagous to
    ``self.defaults``. Presets contain an outer level of keys providing
    the names of available presets::

        presets = \"\"\"
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
    specified for the method, and ``presets``, containing only the
    presets applicable to the method::

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
      verbose (bool): Enable verbose output
      debug (bool): Enable debug output
    """
    from . import get_yaml
    from .debug import db_s, db_kv

    def __init__(self, verbose=False, debug=False):
        """
        Stores arguments provided at decoration.

        Arguments:
          verbose (bool): Enable verbose output
          debug (bool): Enable debug output
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
            from . import get_yaml
            from .debug import db_s

            if hasattr(self, "debug"):
                db = (decorator.debug or self.debug or in_kwargs.get("debug",
                False))
            else:
                db = decorator.debug or in_kwargs.get("debug", False)
            if db:
                db_s("Managing defaults and presets for method " +
                  "'{0}' ".format(method.__name__,
                  "of class '{0}':".format(type(self).__name__)))

            out_args   = in_args
            out_kwargs = in_kwargs.copy()

            # Manage defaults
            out_defaults = {}
            if hasattr(self, "defaults"):
                in_defaults = get_yaml(self.defaults)
                if method.__name__ in in_defaults:
                    if db:
                        db_s("defaults available", 1)
                    out_defaults = in_defaults[method.__name__]
                else:
                    if db:
                        db_s("defaults unavailale for this method", 1)
            else:
                if db:
                    db_s("defaults unavailable for this class", 1)
            out_kwargs["defaults"] = out_defaults

            # Manage presets
            out_presets = {}
            if hasattr(self, "presets"):
                in_presets = get_yaml(self.presets)
                for preset_key, preset_value in in_presets.items():
                    if method.__name__ in preset_value:
                        if db:
                            db_s("preset '{0}'".format(preset_key) +
                                 " available", 1)
                        out_presets[preset_key] = preset_value[method.__name__]
                    else:
                        if db:
                            db_s("preset '{0}'".format(preset_key) +
                                 " unavailable for this method", 1)
            else:
                if db:
                    db_s("presets unavailable for this class", 1)
            out_kwargs["presets"] = out_presets

            return method(self, *out_args, **out_kwargs)

        return wrapped_method
