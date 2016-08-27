#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.ManualPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds manually-set arguments to a nascent spec.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec import yaml_load, yaml_dump
from ..yspec.plugins import YSpecPlugin
################################### CLASSES ###################################
class ManualPlugin(YSpecPlugin):
    """
    Adds manually-set arguments to a nascent spec.

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "manual"

    def __init__(self, indexed_levels=None, **kwargs):
        """
        """
        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Adds manually-set arguments to a nascent spec.

        Arguments:
          spec (dict): Nascent spec
          source_spec (dict): Source spec used as source of manual
            arguments

        Returns:
          dict: Updated spec including maually-set arguments
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels):
        """
        Adds manually-set arguments to one level of spec hierarchy

        Arguments:
          spec (dict): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels within current level
        """
        from copy import deepcopy

        # Loop over source argument keys and values at this level
        for source_key, source_val in source_spec.items():
            print(source_key)

            # This level is indexed; loop over indexes as well
            if indexed_levels is not None and source_key in indexed_levels:
                for index in sorted([k for k in spec[source_key]
                if str(k).isdigit()]):
                    self.process_level(
                      spec[source_key][index],
                      source_spec.get(source_key, {}).get(index, {}),
                      indexed_levels.get(source_key, {}))
            # This level is not indexed
            else:
                # source_val is a dict; recurse
                if isinstance(source_val, dict):
                    if source_key not in spec:
                        spec[source_key] = {}
                    self.process_level(
                      spec[source_key],
                      source_spec.get(source_key, {}),
                      indexed_levels.get(source_key, {}))
                # source_val is singular; store and continue loop
                else:
                    spec[source_key] = deepcopy(source_val)
