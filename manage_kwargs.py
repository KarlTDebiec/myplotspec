# -*- coding: utf-8 -*-
#   myplotspec.manage_kwargs.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Decorator to manage the passage of keyword arguments to a function or
method.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class manage_kwargs(object):
    """
    Decorator to manage the passage of keyword arguments to a function
    or method.

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

      Available presets are obtained from the argument
      ``available_presets``, which may be a dict, a path to a YAML file,
      or a YAML string. Selected presets are obtained from the argument
      ``presets``, which may be a string or list of strings in order of
      increasing priority::

        my_function(
            presets = 'letter',
            available_presets = {
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

      YAML file is obtained from the keyword argument ``yaml_spec``,
      which may be a dict, a path to a YAML file, or a YAML string.
      Selected keys within the YAML file from which to load arguments
      are obtained from the argument ``yaml_keys``, which is a list of
      lists in order of increasing priority::

        my_function(
            yaml_spec = {
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

        my_function(
            fig_width  = 6.0,
            fig_height = 6.0,
            ...
        )

    All of the above will override defaults provided in the function
    declaration itself.

    Attributes:
      verbose (int): Level of verbose output
      debug (int): Level of debug output
    """

    def __init__(self, verbose=0, debug=0):
        """
        Stores arguments provided at decoration.

        Arguments:
          verbose (int): Level of verbose output
          debug (int): Level of debug output
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

        decorator = self
        self.function = function

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
            from . import get_yaml, merge_dicts, multi_kw
            from .debug import db_s, db_kv

            db = max(in_kwargs.get("debug", 0), decorator.debug,
                  self.debug if hasattr(self, "debug") else 0)

            # Prepare sources and destinations
            if db >= 1:
                db_s("Managing kwargs for function '{0}':".format(
                  function.__name__))
            defaults = get_yaml(in_kwargs.pop("defaults", {}))
            available_presets = get_yaml(in_kwargs.pop("available_presets",
                                  {}))
            selected_presets = copy(multi_kw(["presets", "preset"],
                                   in_kwargs, []))
            if isinstance(selected_presets, six.string_types):
                selected_presets = [selected_presets]
            elif selected_presets is None:
                selected_presets = []
            available_yaml = copy(get_yaml(in_kwargs.get("yaml_spec", {})))
            selected_yaml_keys = list(map(tuple, in_kwargs.get("yaml_keys",
                                   [["__complete_file__"]])))
            out_args = copy(in_args)
            out_kwargs = {}

            # Prepare selected yaml keys and determine presets
            selected_yaml = {}
            for selected_yaml_key in selected_yaml_keys:
                node = available_yaml
                if selected_yaml_key != ("__complete_file__",):
                    for key in selected_yaml_key:
                        if key in node.keys():
                            node = node[key]
                        elif str(key) in map(str, node.keys()):
                            node = node[str(key)]
                        else:
                            node = {}
                            break
                if node is None:
                    node = {}
                selected_yaml[selected_yaml_key] = node
                if "presets" in node or "preset" in node:
                    additional_presets = copy(multi_kw(["presets", "preset"],
                                     node, []))
                    if isinstance(additional_presets, six.string_types):
                        additional_presets = [additional_presets]
                    elif additional_presets is None:
                        addition_presets = []
                    for additional_preset in additional_presets:
                        if additional_preset in selected_presets:
                            selected_presets.remove(additional_preset)
                        selected_presets.append(additional_preset)
            if db >= 1:
                db_s("Selected presets that are available: '{0}'".format(
                  selected_presets))

            # Lowest priority: Defaults
            if db >= 1:
                db_s("Low priority: Defaults", 1)
                for key in sorted(defaults.keys()):
                    if key in out_kwargs:
                        db_kv(key, defaults[key], 2, "*")
                    else:
                        db_kv(key, defaults[key], 2, "+")
            out_kwargs = merge_dicts(out_kwargs, defaults)

            # Low priority: Presets
            if db >= 1:
                db_s("Intermediate priority: Presets", 1)
                for selected_preset in selected_presets:
                    db_s(selected_preset, 2)
                    if selected_preset not in available_presets:
                        continue
                    for key in sorted(available_presets[selected_preset]):
                        if key in out_kwargs:
                            db_kv(key, available_presets[selected_preset][key],
                              3, "*")
                        else:
                            db_kv(key, available_presets[selected_preset][key],
                              3, "+")
            for selected_preset in selected_presets:
                if selected_preset in available_presets:
                    out_kwargs = merge_dicts(out_kwargs,
                                   available_presets[selected_preset])

            # High priorty: Yaml
            if db >= 1:
                db_s("High priority: Yaml", 1)
                for selected_yaml_key in selected_yaml_keys:
                    db_s(selected_yaml_key, 2)
                    for key in sorted(selected_yaml[selected_yaml_key]):
                        if key in out_kwargs:
                            db_kv(key, selected_yaml[selected_yaml_key][key],
                              3, "*")
                        else:
                            db_kv(key, selected_yaml[selected_yaml_key][key],
                              3, "+")
            for selected_yaml_key in selected_yaml_keys:
                out_kwargs = merge_dicts(out_kwargs,
                               selected_yaml[selected_yaml_key])

            # Highest priorty: Function call
            if db >= 1:
                db_s("Highest priority: Arguments provided at function or " +
                     "method call", 1)
                for key in sorted(in_kwargs.keys()):
                    if key in out_kwargs:
                        db_kv(key, in_kwargs[key], 2, "*")
                    else:
                        db_kv(key, in_kwargs[key], 2, "+")
            out_kwargs = merge_dicts(out_kwargs, in_kwargs)
            out_kwargs["presets"] = selected_presets
            out_kwargs["yaml_spec"] = available_yaml

            # Run function
            return function(*out_args, **out_kwargs)

        return wrapped_function
