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
Adds preset argument groups to a nascent spec

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
    Adds preset argument groups to a nascent spec

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      available_presets (dict): Available presets; outermost keys are
        the preset names, while the values are the arguments associated
        with each preset
    """
    name = "presets"

    def __init__(self, indexed_levels=None, available_presets=None,**kwargs):
        """
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
        Adds preset argument groups to a nascent spec

        Arguments:
          spec (dict): Nascent spec
          source_spec (dict): Source spec to use to determine where
            defaults should be added

        Returns:
          dict: Updated spec including default arguments
        """

        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels,
              self.available_presets)
        return spec

    def process_level(self, spec, source_spec, indexed_levels,
        available_presets, selected_presets=None):
        """
        Adds selected preset arguments to one level of spec hierarchy

        Arguments:
          spec (dict): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          available_presets (dict): Available presets within current
            level
          selected_presets (list): Presets selected above current level
        """
        from copy import deepcopy

        if available_presets is None:
            return
        if indexed_levels is None:
            indexed_levels = {}

        # Determine selected presets, including those inherited from a
        # parent level and those first selected at this level
        if selected_presets is None:
            selected_presets = []
        else:
            selected_presets = selected_presets[:]
        if "presets" in source_spec:
            for preset in source_spec["presets"]:
                if preset in selected_presets:
                    selected_presets.remove(preset)
                selected_presets += [preset]
        # Even if no presets are selected, cannot return here, because
        # lower levels may activate presets

        # Loop over presets that are currently selected
        for selected_preset in selected_presets:
            if selected_preset not in available_presets:
                continue

            # Loop over preset argument keys and values at this level
            for preset_key, preset_val in [(k, v)
            for k, v in available_presets[selected_preset].items()
            if not k.startswith("_")]:
                # This key is indexed; use indexed function
                if indexed_levels is not None and preset_key in indexed_levels:
                    # Make new dict of available_presets including only
                    # those applicable to the next level
                    for index in sorted([k for k in spec[preset_key]
                    if str(k).isdigit()]):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key]
                          for k, v in available_presets.items()
                          if preset_key in v}
                        self.process_level(
                          spec[preset_key][index],
                          source_spec.get(preset_key, {}).get(index, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets,
                          selected_presets)
                # This level is not indexed
                else:
                    # preset_val is a dict; recurse
                    if isinstance(preset_val, dict):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key]
                          for k, v in available_presets.items()
                          if preset_key in v}
                        if preset_key not in spec:
                            spec[preset_key] = {}
                        self.process_level(
                          spec[preset_key],
                          source_spec.get(preset_key, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets,
                          selected_presets)
                    # preset_val is singular; store and continue loop
                    else:
                        spec[preset_key] = deepcopy(preset_val)
