#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.MPSInitializePlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Initializes a nascent spec.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec.plugins.InitializePlugin import InitializePlugin
################################### CLASSES ###################################
class MPSInitializePlugin(InitializePlugin):
    """
    Initializes a nascent spec.

    Differs from yspec's InitializePlugin through the addition of
    support for initializing a grid of subplots based on arguments
    defined under figures/INDEX/gridspec

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """

    def process_level(self, spec, source_spec, indexed_levels, path=None):
        """
        Initializes one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          path (list): List of keys leading to this level
          source_spec[gridspec][nrows] (int, optional): Number of rows
            of subplots to add
          source_spec[gridspec][ncols] (int, optional): Number of
            columns of subplots to add
          source_spec[gridspec][nsubplots] (int, optional): Number of
            subplots to add; if less than nrows*ncols (e.g. 2 cols and 2
            rows but only 3 subplots)
        """

        # Process arguments
        if indexed_levels is None or source_spec is None:
            return
        if path is None:
            path = []

        # Handle grid of subplots
        if (len(path) == 2 and path[0] == "figures"
        and "gridspec" in source_spec):
            gridspec  = source_spec["gridspec"]
            nrows     = gridspec.get("nrows", 1)
            ncols     = gridspec.get("ncols", 1)
            nsubplots = min(gridspec.get("nsubplots", nrows*ncols),
                         nrows*ncols)
            indexes = range(nsubplots)
            if "subplots" not in spec:
                self.initialize(spec, "subplots")
            for index in indexes:
                if index not in spec["subplots"]:
                    self.initialize(spec["subplots"], index)

        # Loop over indexed levels at this level
        for level in [k for k in indexed_levels if k in source_spec]:
            if source_spec.get(level) is None:
                continue
            if level not in spec:
                self.initialize(spec, level)
            indexes = sorted([k for k in source_spec[level]
                        if str(k).isdigit()])
            # Apply "all" to all indexes
            if "all" in source_spec.get(level, {}):
                all_indexes = sorted(list(set(indexes +
                  [k for k in spec[level] if str(k).isdigit()])))
                for index in all_indexes:
                    if index not in spec[level]:
                        self.initialize(spec[level], index)
                    self.process_level(
                      spec[level][index],
                      source_spec[level]["all"],
                      indexed_levels.get(level, {}),
                      path=path+[level, index])
            # Loop over specific indexes
            for index in indexes:
                # Add dict in which to store lower levels
                if index not in spec[level]:
                    self.initialize(spec[level], index)
                self.process_level(
                  spec[level][index],
                  source_spec[level].get(index, {}),
                  indexed_levels.get(level, {}),
                  path=path+[level, index])
