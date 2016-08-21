#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.DefaultsPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs specification
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec import yaml_load, yaml_dump
from ..yspec.plugins import YSpecPlugin
################################### CLASSES ###################################
class DefaultsPlugin(YSpecPlugin):
    """
    """
    name = "defaults"

    def __init__(self, indexed_levels=None, defaults=None,**kwargs):
        """
        Store settings for this plugin here
        """
        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}
        if defaults is not None:
            self.defaults = defaults
        else:
            self.defaults = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Apply settings to spec here
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels,
              self.defaults)
        return spec

    def process_level(self, spec, source_spec, indexed_levels, defaults):
        """
        """

        if defaults is not None:
            for key in defaults.keys():
                value = defaults[key]
                if key not in spec:
                    spec[key] = {}
                if indexed_levels is not None and key in indexed_levels:
                    i_keys = spec[key].keys()
                    i_keys = sorted([k for k in i_keys if str(k).isdigit()])
                    for i_key in i_keys:
                        if isinstance(value, dict):
                            self.process_level(
                              spec[key][i_key],
                              source_spec[key][i_key],
                              indexed_levels.get(key, {}),
                              value)
                        else:
                            spec[key][i_key] = value
                else:
                    if isinstance(value, dict):
                        self.process_level(
                          spec[key],
                          source_spec.get(key, {}),
                          indexed_levels.get(key, {}),
                          value)
                    else:
                        spec[key] = value
