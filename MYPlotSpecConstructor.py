#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.MYPlotSpecConstructor.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs yaml-format specification
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec")
    import myplotspec
from IPython import embed
import ruamel.yaml as yaml
from yspec.YSpecConstructor import YSpecConstructor
from myplotspec.plugins.InitializePlugin import InitializePlugin
from myplotspec.plugins.DefaultsPlugin import DefaultsPlugin
################################### CLASSES ###################################
class MYPlotSpecConstructor(YSpecConstructor):
    """
    """

    available_plugins = dict(
      initialize = InitializePlugin,
      defaults   = DefaultsPlugin)
    plugin_config = dict(
      initialize = """
        indexed_levels:
          figures:
              subplots:
                  datasets:""",
      defaults = """
        indexed_levels:
          figures:
            subplots:
              datasets:
        defaults:
          figures:
            subplot_kw:
              autoscale_on: False
              axisbg: none
            subplots:
              hand: stump
              datasets:
                nay: bama
      """,
      presets = """""")

    def __init__(self, source_spec=None, **kwargs):
        """
        """
        from .yspec import yaml_load, yaml_dump

        # Identify available plugins and order
        #   Probably read from attribute
        plugins = ["initialize", "defaults", "presets", "manual", "write"]
        plugins = ["initialize", "defaults"]
        self.source_spec = yaml_load(source_spec)
        spec = yaml.comments.CommentedMap()

        print()
        print(yaml_dump(spec))
        print()

        for plugin_name in plugins:
            print(plugin_name.upper())
            if plugin_name in self.available_plugins:
                plugin = self.available_plugins[plugin_name](
                  **yaml_load(self.plugin_config.get(plugin_name, {})))
                spec = plugin(spec, self.source_spec)
            else:
                raise Exception()
            print(yaml_dump(spec))
            print()

        # Should be possible to set defaults and presets from string or file
        # if os.path.isfile(defaults):
        #   self.available_defaults = pyyaml.read(defaults)
        # elif:
        #   self.available_defaults = defaults
        # Call construct with kwargs

#################################### MAIN #####################################
def main():
    import argparse

    # Prepare argument parser
    parser = argparse.ArgumentParser(
      description = __doc__)
    parser.add_argument(
      "-spec",
      required = True,
      dest     = "source_spec",
      metavar  = "SPEC",
      type     = str,
      help     = "input file from which to load specification")

    # Source spec infile
    # Plugins
    # Arguments from plugins
    #   Defaults infile
    #   Presets infile
    parser.set_defaults(class_=MYPlotSpecConstructor)
    kwargs = vars(parser.parse_args())
    kwargs.pop("class_")(**kwargs)

if __name__ == "__main__":
    main()
