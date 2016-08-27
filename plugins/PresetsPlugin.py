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
          selected_presets (list): 
        """
        from copy import deepcopy
        print(spec.keys(), source_spec.keys(), indexed_levels,
        available_presets.keys(), selected_presets)

        if available_presets is None:
            return

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

        # Loop over keys in current level of nascent spec
        for key in spec:

            # Loop over presets that are currently chosen
            for selected_preset in selected_presets:

                # Select presets that are available at this level
                # and have settings for this key
                if not ((selected_preset in available_presets)
                and     (key in available_presets[selected_preset])):
                    continue

                val = available_presets[selected_preset][key]
                # This level is indexed; loop over index level here as well
                if indexed_levels is not None and key in indexed_levels:
                    i_keys = spec[key].keys()
                    i_keys = sorted([k for k in i_keys if str(k).isdigit()])
                    for i_key in i_keys:
                        if isinstance(val, dict):
                            for p_key, p_val in val.items():
                                if p_key not in indexed_levels.get(key, {}):
                                    spec[key][i_key][p_key] = deepcopy(p_val)
                                else:
                                    ap = {}
                                    for k, v in available_presets.items():
                                        if key in v:
                                            print(k, key)
                                            if p_key in v[key]:
                                                print(k, p_key)
                                    print(yaml_dump(ap))
                                    self.process_level(
                                      spec[key][i_key],
                                      source_spec[key][i_key],
                                      indexed_levels.get(key, {}),
                                      {k: v for k, v in
                                      available_presets.items()},
                                      selected_presets)
                                    pass
                                    # Go deeper
                        else:
                            spec[key][i_key] = val
#                # This level is not indexed
#                else:
#                    if isinstance(val, dict):
#                        for p_key, p_val in val.items():
#                            if p_key not in indexed_levels.get(key, {}):
#                                spec[key][p_key] = deepcopy(p_val)
#                            else:
#                                self.process_level(
#                                  spec[key][p_key],
#                                  source_spec[key].get(p_key, {}),
#                                  indexed_levels.get(key, {}),
#                                  val,
#                                  selected_presets)
#                    else:
#                        spec[key][i_key] = val
