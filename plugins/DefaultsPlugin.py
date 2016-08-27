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
Adds default arguments to a nascent spec.

.. todo:
    - Move this version to yspec
    - Write updated version for myplotspec
      - Must read defaults from dataset classes
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
    Adds default arguments to a nascent spec.

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      defaults (dict): Default arguments
    """
    name = "defaults"

    def __init__(self, indexed_levels=None, defaults=None, **kwargs):
        """
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
        Adds default arguments to a nascent spec.

        Arguments:
          spec (dict): Nascent spec
          source_spec (dict): Source spec to use to determine where
            defaults should be added

        Returns:
          dict: Updated spec including default arguments
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels,
              self.defaults)
        return spec

    def process_level(self, spec, source_spec, indexed_levels, defaults):
        """
        Adds default arguments at one level of spec hierarchy.

        Arguments:
          spec (dict): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          defaults (dict): Defaults within current level
        """

        if defaults is None:
            return

        # Loop over default argument keys and values at this level
        for key, value in defaults.items():

            # This level is indexed; loop over next level here as well
            if indexed_levels is not None and key in indexed_levels:
                # No need to loop through indexes if none present
                if key not in spec:
                    continue
                # Loop over indexes
                i_keys = spec[key].keys()
                i_keys = sorted([k for k in i_keys if str(k).isdigit()])
                for i_key in i_keys:
                    # Add dict in which to store argument values
                    if i_key not in spec[key]:
                        spec[key][i_key] = {}
                    # Argument value is a dict; recurse
                    if isinstance(value, dict):
                        self.process_level(
                          spec[key][i_key],
                          source_spec[key][i_key],
                          indexed_levels.get(key, {}),
                          value)
                    # Argument value is singular; store and continue loop
                    else:
                        spec[key][i_key] = value
            # This level is not indexed
            else:
                # Argument value is a dict; recurse
                if isinstance(value, dict):
                    # Add dict in which to store argument values
                    if key not in spec:
                        spec[key] = {}
                    self.process_level(
                      spec[key],
                      source_spec.get(key, {}),
                      indexed_levels.get(key, {}),
                      value)
                # Argument value is singular; store and continue loop
                else:
                    spec[key] = value
