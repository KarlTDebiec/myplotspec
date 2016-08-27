#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.InitializePlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Initializes a nascent spec.

.. todo:
    - Move this version to ypec
    - Write updated version for myplotspec
      - Must understand nrows, ncols, nsubplots and add those indexes
      - Must somehow get indexes from presets if present
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec import yaml_load, yaml_dump
from ..yspec.plugins import YSpecPlugin
################################### CLASSES ###################################
class InitializePlugin(YSpecPlugin):
    """
    Initializes a nascent spec.

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "initialize"

    def __init__(self, indexed_levels=None, **kwargs):
        """
        """
        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Initializes a nascent spec.

        Arguments:
          spec (dict): Nascent spec (typically {} at this time)
          source_spec (dict): Source spec to use to determine initial
            structure

        Returns:
          dict: Initialized spec
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels):
        """
        Initialize one level of spec hierarchy

        Arguments:
          spec (dict): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
        """

        # Process arguments
        if indexed_levels is None:
            return

        for level in [k for k in indexed_levels if k in source_spec]:
            if level not in spec:
                spec[level] = {}
            # Loop over indexes
            for index in sorted([k for k in source_spec.get(level, {})
            if str(k).isdigit()]):
                # Add dict in which to store lower levels
                spec[level][index] = {}
                self.process_level(
                  spec[level][index],
                  source_spec[level][index],
                  indexed_levels.get(level, {}))
