#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Method_Defaults_Presets.py
#   Written by Karl Debiec on 15-01-03, last updated by Karl Debiec on 15-01-06
"""
Decorator class to manage the passage of defaults and presets from
a class to a method of that class.
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
from . import get_yaml
from .Debug import db_s, db_kv, Debug_Arguments
################################### CLASSES ####################################
class Method_Defaults_Presets(Debug_Arguments):
    """
    Decorator class to manage the passage of defaults and presets from
    a class to a method of that class.

    Defaults are accessed from the class's instance (or class)variable
    ``self.defaults``, and may be a dictionary, a path to a yaml file,
    or a yaml string. The first level of keys are the names of methods
    of the class, and the values are the corresponding defaults for each
    argument of that method:

    ::

        self.defaults = \"\"\"
            method_1:
              method_1_argument_1: 1000
              method_1_argument_2: abcd
            method_2
              method_2_argument_1: 2000
              method_2_argument_2: efgh
            ...
        \"\"\"

    Presets are accessed from the instance variable ``self.presets``.
    These are treated similarly to defaults, but contain an outer level
    of keys corresponding to names of the available presets:

    ::
        self.presets = \"\"\"
            preset_1:
                method_1:
                  method_1_argument_1: 1001
                  method_1_argument_2: abcde
                method_2
                  method_2_argument_1: 2001
                  method_2_argument_2: efghi
            preset_2:
                method_1:
                  method_1_argument_1: 1002
                  method_1_argument_2: abcdef
                method_2
                  method_2_argument_1: 2002
                  method_2_argument_2: efghij
        \"\"\"

    When this decorator is used to wrap a method of a class, it adds to
    the arguments being passed ``defaults``, containing only the
    defaults specified for that method, and ``presets``, containing
    only the presets containing arguments for that method.

    ::
        @Method_Defaults_Presets()
        def method_1(*args, **kwargs):
            ...

        > kwargs = {
        >   "defaults": {
        >     "method_1_argument_1": 1000,
        >     "method_1_argument_2": "asdf"
        >   },
        >   "presets": {
        >     "preset_1": {
        >       "method_1_argument_1": 1001,
        >       "method_1_argument_2": "asde"
        >     },
        >     "preset_1": {
        >       "method_1_argument_1": 1002,
        >       "method_1_argument_2": "asdef"
        >     }
        >   },
        >   ...
        > }

    """

    def __call__(self, method):
        """
        Wraps method

        **Arguments:**
            :*method*: method to wrap

        **Returns:**
            :*wrapped_method*: Wrapped method
        """
        from functools import wraps

        dec_debug = self.debug

        @wraps(method)
        def wrapped_method(self, *in_args, **in_kwargs):
            """
            Wrapped version of method

            **Arguments:**
                :*\*in_args*:     Arguments passed to method at call
                :*\*\*in_kwargs*: Keyword arguments passed to method at
                                  call
            """
            if hasattr(self, "debug"):
                db = dec_debug or self.debug or in_kwargs.get("debug", False)
            else:
                db = dec_debug or in_kwargs.get("debug", False)
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
                            db_s("preset '{0}' available".format(preset_key), 1)
                        out_presets[preset_key] = preset_value[method.__name__]
                    else:
                        if db:
                            db_s("preset '{0}' unavailable".format(preset_key) +
                                 " for this method", 1)
            else:
                if db:
                    db_s("presets unavailable for this class", 1)
            out_kwargs["presets"] = out_presets

            return method(self, *out_args, **out_kwargs)

        return wrapped_method
