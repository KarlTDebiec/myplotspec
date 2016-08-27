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
from myplotspec.plugins.PresetsPlugin import PresetsPlugin
################################### CLASSES ###################################
class MYPlotSpecConstructor(YSpecConstructor):
    """
    """

    available_plugins = dict(
      initialize = InitializePlugin,
      defaults   = DefaultsPlugin,
      presets    = PresetsPlugin)
    indexed_levels = """
      figures:
          subplots:
              datasets:"""
    plugin_config = dict(
      defaults = """
        defaults:
          yumbo: elephant
          figures:
            subplot_kw:
              autoscale_on: False
              axisbg: none
            subplots:
              hand: stump
              datasets:
                nay: bama""",
      presets = """
        available_presets:
          letter:
            class: target
            help: Letter (width ≤ 6.5", height ≤ 9.0")
            figures:
              fig_width: 100.00
              subplots:
                title_fp: 16b
                datasets:
                  plot_kw:
                    lw: 2
          manuscript:
            class: target
            help: Manuscript (width ≤ 7.0", height ≤ 9.167")
            figures:
              fig_width: 10.00
              shared_legend_kw:
                legend_kw:
                  title_fp:  8b
              subplots:
                title_fp: 8b
                datasets:
                  plot_kw:
                    lw: 1
          dssp:
            class: content
            help: Dynamic secondary structure of proteins calculated by cpptraj
            figures:
              shared_legend: True
              shared_legend_kw:
                handles:
                  - ["None",                 {color: [0,0,7]}]
                  - ["Parallel β Sheet",     {color: [1,0,7]}]
                  - ["Antiparallel β Sheet", {color: [2,0,7]}]
                legend_kw:
                  title: Secondary Structure
              subplots:
                ylabel: Residue
                datasets:
                  dataset_kw:
                    downsample_mode: mode
          perresrmsd:
            class: content
            help: Per-residue RMSD calculated by cpptraj
            figures:
              shared_legend: False
              subplots:
                ylabel: yoop
                datasets:
                  dataset_kw:
                  downsample_mode: mean
      """)

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
                  indexed_levels=yaml_load(self.indexed_levels),
                  **yaml_load(self.plugin_config.get(plugin_name, {})))
                spec = plugin(spec, self.source_spec)
            else:
                raise Exception()
            print(yaml_dump(spec))
            print()

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
