# -*- coding: utf-8 -*-
#   myplotspec.manage_kwargs.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Decorator to manage the passage of keyword arguments to function or method.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class manage_kwargs(object):
    """
    Decorator to manage the passage of keyword arguments to function or
    method.

    Accumulates keyword arguments from several sources, in order of
    increasing priority:

    1. Defaults

      Obtained from the argument ``defaults``, which may be a dict, a
      path to a YAML file, or a YAML string::

        my_function(
            defaults = {
                'fig_width':  5.0
                'fig_height': 5.0
            },
            ...
        )

    2. Presets

      Available presets are obtained from the argument ``presets``,
      which may be a dict, a path to a YAML file, or a YAML string.
      Selected presets are obtained from the argument ``preset``, which
      may be a string or list of strings::

        my_function(
            preset = 'letter',
            presets = {
                'letter': {
                    'fig_width':   8.5
                    'fig_height': 11.0
                },
                'legal': {
                    'fig_width':   8.5
                    'fig_height': 14.0
                }
            },
            ...
        )

    3. YAML file

      YAML file is obtained from the keyword argument ``yaml_dict``,
      which may be a dict, a path to a YAML file, or a YAML string.
      Selected keys within the YAML file from which to load arguments
      are obtained from the argument ``yaml_keys``, which is a list of
      lists in order of increasing priority::

        my_function(
            yaml_dict = {
                'figures': {
                    'all': {
                        'fig_width':  11.0,
                        'fig_height': 17.0,
                        'outfile':    'plot.pdf'
                    },
                    '0': {
                        'fig_width':  12.0
                    }
                }
            },
            yaml_keys = [['figures', 'all'], ['figures', '0']],
            ...
        )

      If ``yaml_keys`` is omitted, the complete yaml file will be used.

    4. Function call

      Arguments provided at function call::

        my_wrapped_function(
            fig_width  = 6.0,
            fig_height = 6.0,
            ...
        )

    All of the above will override defaults provided in the function
    declaration itself.

    Attributes:
      verbose (bool): Enable verbose output
      debug (bool): Enable debug output
    """

    def __init__(self, verbose=False, debug=False):
        """
        Stores arguments provided at decoration.

        Arguments:
          verbose (bool): Enable verbose output
          debug (bool): Enable debug output
        """
        self.verbose = verbose
        self.debug = debug

    def __call__(self, function):
        """
        Wraps function or method.

        Arguments:
          function (function): Function or method to wrap

        Returns:
          (function): Wrapped function or method
        """
        from functools import wraps

        self.function = function

        decorator = self

        @wraps(function)
        def wrapped_function(*in_args, **in_kwargs):
            """
            Wrapped version of function or method

            Arguments:
              in_args (tuple): Arguments passed to function
              in_kwargs (dict): Keyword arguments passed to function

            Returns:
              Return value of wrapped function
            """
            from copy import copy
            import six
            from . import get_yaml, merge_dicts
            from .debug import db_s, db_kv

            if hasattr(self, "debug"):
                db = (decorator.debug or self.debug or in_kwargs.get("debug",
                  False))
            else:
                db = decorator.debug or in_kwargs.get("debug", False)

            # Prepare inputs and outputs
            if db:
                db_s("Managing kwargs for function '{0}':".format(
                  function.__name__))
            in_defaults   = get_yaml(in_kwargs.pop("defaults", {}))
            in_presets    = get_yaml(in_kwargs.pop("presets", {}))
            sel_presets   = copy(in_kwargs.get("preset", []))
            if isinstance(sel_presets, six.string_types):
                sel_presets = [sel_presets]
            in_yaml       = get_yaml(in_kwargs.get("yaml_dict", {}))
            sel_yaml_keys = list(map(tuple, in_kwargs.get("yaml_keys",
                              [["__complete_file__"]])))
            out_args      = in_args
            out_kwargs    = {}

            # Prepare selected yaml keys and determine presets
            sel_yaml = {}
            for sel_yaml_key in sel_yaml_keys:
                node = in_yaml.copy()
                if sel_yaml_key != ("__complete_file__",):
                    for key in sel_yaml_key:
                        if key in node.keys():
                            node = node[key]
                        elif str(key) in map(str, node.keys()):
                            node = node[str(key)]
                        else:
                            node = {}
                            break
                sel_yaml[sel_yaml_key] = node
                if "preset" in node and not node["preset"] in sel_presets:
                    add_presets = copy(node.get("preset"))
                    if isinstance(add_presets, six.string_types):
                        sel_presets += [add_presets]
                    else:
                        sel_presets += add_presets
            if db:
                db_s("Selected presets that are available: '{0}'".format(
                  sel_presets))

            # Lowest priority: Defaults
            if db:
                db_s("Low priority: Defaults", 1)
                for key in sorted(in_defaults.keys()):
                    if key in out_kwargs:
                        db_kv(key, in_defaults[key], 2, "*")
                    else:
                        db_kv(key, in_defaults[key], 2, "+")
            out_kwargs = merge_dicts(out_kwargs, in_defaults)

            # Low priority: Presets
            if db:
                db_s("Intermediate priority: Presets", 1)
                for sel_preset in sel_presets:
                    db_s(sel_preset, 2)
                    if sel_preset not in in_presets:
                        continue
                    for key in sorted(in_presets[sel_preset]):
                        if key in out_kwargs:
                            db_kv(key, in_presets[sel_preset][key], 3, "*")
                        else:
                            db_kv(key, in_presets[sel_preset][key], 3, "+")
            if sel_presets is not None:
                for sel_preset in sel_presets:
                    if sel_preset not in in_presets:
                        continue
                    out_kwargs = merge_dicts(out_kwargs,
                      in_presets[sel_preset])

            # High priorty: Yaml
            if db:
                db_s("High priority: Yaml", 1)
                for sel_yaml_key in sel_yaml_keys:
                    db_s(sel_yaml_key, 2)
                    if sel_yaml[sel_yaml_key] == {}:
                        continue
                    for key in sorted(sel_yaml[sel_yaml_key]):
                        if key in out_kwargs:
                            db_kv(key, sel_yaml[sel_yaml_key][key], 3, "*")
                        else:
                            db_kv(key, sel_yaml[sel_yaml_key][key], 3, "+")
            for sel_yaml_key in sel_yaml_keys:
                if sel_yaml[sel_yaml_key] == {}:
                    continue
                out_kwargs = merge_dicts(out_kwargs, sel_yaml[sel_yaml_key])

            # Highest priorty: Function call
            if db:
                db_s("Highest priority: Arguments provided at function or " +
                     "method call", 1)
                for key in sorted(in_kwargs.keys()):
                    if key in out_kwargs:
                        db_kv(key, in_kwargs[key], 2, "*")
                    else:
                        db_kv(key, in_kwargs[key], 2, "+")
            out_kwargs           = merge_dicts(out_kwargs, in_kwargs)
            out_kwargs["preset"] = sel_presets
            out_kwargs["yaml_dict"] = in_yaml

            # Run function
            return function(*out_args, **out_kwargs)

        return wrapped_function
