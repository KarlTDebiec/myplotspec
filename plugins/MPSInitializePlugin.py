#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.MPSInitializePlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Initializes a nascent spec.

.. todo:
  - Somehow get indexes from presets if present
  - Intersphinx documentation
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
import ruamel.yaml as yaml
from ..yspec.plugins import YSpecPlugin
################################### CLASSES ###################################
class MPSInitializePlugin(YSpecPlugin):
    """
    Initializes a nascent spec.

    Differs from yspec's InitializePlugin through the addition of
    support for initializing a grid of subplots based on arguments
    defined under figures/INDEX/subplots/grid

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "initialize"
    description = """Initializes indexed levels of nascent spec based on
      structure present in source spec."""

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

    def process_level(self, spec, source_spec, indexed_levels, path=None):
        """
        Initialize one level of spec hierarchy

        Arguments:
          spec (dict): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          path (list): List of keys leading to this level
          source_spec[grid][nrows] (int, optional): Number of rows of subplots
            to add
          source_spec[grid][ncols] (int, optional): Number of columns of
            subplots to add
          source_spec[grid][nsubplots] (int, optional): Number of subplots to
            add; if less than nrows*ncols (e.g. 2 cols and 2 rows but
            only three subplots)
        """

        # Process arguments
        if indexed_levels is None or source_spec is None:
            return
        if path is None:
            path = []

        # Loop over indexed levels at this level
        for level in [k for k in indexed_levels if k in source_spec]:
            if source_spec.get(level) is None:
                continue
            if level not in spec:
                spec[level] = yaml.comments.CommentedMap()
            indexes = sorted(list(set([k for k in source_spec[level]
              if str(k).isdigit()])))
            # Handle grid of subplots
            if level == "subplots" and "grid" in source_spec.get(level, {}):
                grid = source_spec[level]["grid"]
                nrows     = grid.get("nrows", 1)
                ncols     = grid.get("ncols", 1)
                nsubplots = min(grid.get("nsubplots", nrows*ncols),
                             nrows*ncols)
                indexes = sorted(list(set(indexes + range(nsubplots))))
            # Apply "all" to all indexes
            if "all" in source_spec.get(level, {}):
                all_indexes = sorted(list(set(indexes +
                  [k for k in spec[level] if str(k).isdigit()])))
                for index in all_indexes:
                    if index not in spec[level]:
                        spec[level][index] = yaml.comments.CommentedMap()
                    self.process_level(
                      spec[level][index],
                      source_spec[level]["all"],
                      indexed_levels.get(level, {}),
                      path=path+[level, index])
            # Loop over specific indexes
            for index in indexes:
                # Add dict in which to store lower levels
                if index not in spec[level]:
                    spec[level][index] = yaml.comments.CommentedMap()
                self.process_level(
                  spec[level][index],
                  source_spec[level].get(index, {}),
                  indexed_levels.get(level, {}),
                  path=path+[level, index])
