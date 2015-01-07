#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Manage_Kwargs.py
#   Written by Karl Debiec on 14-10-25, last updated by Karl Debiec on 15-01-06
"""
Decorator class to manage the passage of keyword arguments to a wrapped
function or method
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
import six
from . import get_yaml, merge_dicts
from .Debug import db_s, db_kv, Debug_Arguments
################################### CLASSES ####################################
class Manage_Kwargs(Debug_Arguments):
    """
    Decorator class to manage the passage keyword arguments to a
    wrapped function or method

    Accumulates keyword arguments from several sources, in order of
    increasing priority:
        - *defaults* keyword argument at call:
            ::

                my_function(
                  defaults = {
                    "width":  5.0
                    "height": 5.0
                    },
                ...)

          *defaults* may be a dictionary, path to a yaml file, or a
          yaml string.
        - *preset* and *presets* keyword arguments at call:
            ::

                my_function(
                  preset  = "letter",
                  presets = {
                    "letter": {
                      "width":   8.5
                      "height": 11.0
                    },
                    "legal": {
                      "width":   8.5
                      "height": 14.0
                    }
                ...)

          *preset* defines the selected preset (or a list of selected
          presets), and *presets* the available presets; *preset* may
          be a string or list, and *presets* may be a dictionary, path
          to a yaml file, or yaml string.
        - *yaml_dict* and *yaml_keys* keyword arguments at function
          call:
            ::

                my_function(
                  yaml_dict = \"\"\"
                    figures:
                      all:
                        width:   11.0
                        height:  17.0
                        outfile: plot.pdf
                    figures:
                      0:
                        width:   12.0
                  \"\"\"
                  yaml_keys = [["figures", "all"], ["figures", "0"]]
                ...)

          *yaml_dict* defines the yaml file, and *yaml_keys* the paths
          within the yaml file from whih to load arguments, in order of
          priority. *yaml_dict* may be a dictionary, path to a yaml
          file, or yaml string if yaml_keys* is omitted, the complete
          yaml file will be used.

        - Additional keyword arguments at call
            ::

                my_wrapped_function(
                  width = 6.0,
                ...)

    All of the above will override defaults provided in the function
    declaration itself.
    """

    def __call__(self, function):
        """
        Wraps function or method

        **Arguments:**
            :*function*: Function or method to wrap

        **Returns:**
            :*wrapped_function*: Wrapped function or method
        """
        from functools import wraps

        dec_debug = self.debug

        @wraps(function)
        def wrapped_function(*in_args, **in_kwargs):
            """
            Wrapped version of function or method

            **Arguments:**
                :*defaults*:      Call-time default arguments to
                                  function; may be dictionary, path to
                                  yaml file, or yaml string
                :*\*in_args*:     Arguments passed to function at call
                :*\*\*in_kwargs*: Keyword arguments passed to function
                                  at call
            """
            if hasattr(self, "debug"):
                db = dec_debug or self.debug or in_kwargs.get("debug", False)
            else:
                db = dec_debug or in_kwargs.get("debug", False)

            # Prepare inputs and outputs
            if db:
                db_s("Managing kwargs for function '{0}':".format(
                  function.__name__))
            in_defaults   = get_yaml(in_kwargs.pop("defaults", {}))
            in_presets    = get_yaml(in_kwargs.pop("presets", {}))
            sel_presets   = in_kwargs.pop("preset", [])
            if isinstance(sel_presets, six.string_types):
                sel_presets = [sel_presets]
            in_yaml       = get_yaml(in_kwargs.get("yaml_dict", {}))
            sel_yaml_keys = map(tuple, in_kwargs.get("yaml_keys",
                              [["__complete_file__"]]))
            out_args      = in_args
            out_kwargs    = {}

            # Prepare selected yaml keys and determine presets
            sel_yaml  = {}
            for sel_yaml_key in sel_yaml_keys:
                node = in_yaml.copy()
                if sel_yaml_key != ("__complete_file__",):
                    for key in sel_yaml_key:
                        if key  in node.keys():
                            node = node[key]
                        elif str(key) in map(str, node.keys()):
                            node = node[str(key)]
                        else:
                            node = {}
                            break
                sel_yaml[sel_yaml_key] = node
                if "preset" in node and not node["preset"] in sel_presets:
                    sel_presets += [node.pop("preset")]

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
                    if not sel_preset in in_presets:
                        continue
                    for key in sorted(in_presets[sel_preset]):
                        if key in out_kwargs:
                            db_kv(key, in_presets[sel_preset][key], 3, "*")
                        else:
                            db_kv(key, in_presets[sel_preset][key], 3, "+")
            for sel_preset in sel_presets:
                if not sel_preset in in_presets:
                    continue
                out_kwargs = merge_dicts(out_kwargs, in_presets[sel_preset])

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

            # Run function
            return function(*out_args, **out_kwargs)

        return wrapped_function
