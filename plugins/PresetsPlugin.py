#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.PresetsPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs specification

.. todo:
    - Move this version to yspec
    - Write updated version for myplotspec
      - Must read presets from dataset classes
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec import yaml_load, yaml_dump
from ..yspec.plugins import YSpecPlugin
################################### CLASSES ###################################
class PresetsPlugin(YSpecPlugin):
    """
    """
    name = "presets"

    def __init__(self, indexed_levels=None, available_presets=None,**kwargs):
        """
        Store settings for this plugin here
        """

        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}
        if available_presets is not None:
            self.available_presets = available_presets
        else:
            self.available_presets = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Apply settings to spec here
        """

        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels,
              self.available_presets)
        return spec

    def process_level(self, spec, source_spec, indexed_levels,
        available_presets, selected_presets=None):
        """
        """
        # Figure out which presets to apply
        # Figure out which presets are applicable to this level
        # Apply presets to this level

        if selected_presets is None:
            selected_presets = []
        if "presets" in source_spec:
            selected_presets += source_spec["presets"]

        # Loop over keys in current level of nascent spec
        for key in spec:

            # Loop over presets that are currently chosen
            for selected_preset in selected_presets:

                # Select presets that are available at this level
                # and have settings for this key
                if ((selected_preset in available_presets)
                and (key in available_presets[selected_preset])):
                    value = available_presets[selected_preset][key]
                    if indexed_levels is not None and key in indexed_levels:
                        i_keys = spec[key].keys()
                        i_keys =sorted([k for k in i_keys if str(k).isdigit()])
                        print(key,_keys)
                        for i_key in i_keys:
                            if isinstance(value, dict):
                                spec[key].update(value)
                            else:
                                spec[key] = value
                    else:
                        if isinstance(value, dict):
                            spec[key].update(value)
                        else:
                            spec[key] = value
