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
Constructs specification

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
    """
    name = "initialize"

    def __init__(self, indexed_levels=None, **kwargs):
        """
        Store settings for this plugin here
        """
        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Apply settings to spec here
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels):
        """
        """

        if indexed_levels is not None:
            for key in indexed_levels.keys():
                if key in source_spec:
                    spec[key] = {}
                    i_keys = source_spec.get(key).keys()
                    i_keys = sorted([k for k in i_keys if str(k).isdigit()])
                    for i_key in i_keys:
                        spec[key][i_key] = {}
                        self.process_level(
                          spec[key][i_key],
                          source_spec[key][i_key],
                          indexed_levels.get(key, {}))

