#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.MYPlotSpecConstructor.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs yaml-format specification
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("myplotspec")
    import myplotspec
from .yspec.YSpecConstructor import YSpecConstructor


################################### CLASSES ###################################
class MYPlotSpecConstructor(YSpecConstructor):
    """
    Constructs yaml-format specification for myplotspec
    """
    from collections import OrderedDict
    from .plugins.MPSInitializePlugin import MPSInitializePlugin
    from .plugins.MPSDefaultsPlugin import MPSDefaultsPlugin
    from .plugins.MPSPresetsPlugin import MPSPresetsPlugin
    from .yspec.plugins.ManualPlugin import ManualPlugin
    from .yspec.plugins.SortPlugin import SortPlugin

    available_plugins = OrderedDict(
        [("initialize", MPSInitializePlugin), ("defaults", MPSDefaultsPlugin),
            ("presets", MPSPresetsPlugin), ("manual", ManualPlugin),
            ("sort", SortPlugin)])
    default_plugins = ["initialize", "defaults", "presets", "manual", "sort"]
    indexed_levels = """
      figures:
          subplots:
              datasets:"""
    plugin_config = dict(defaults="""
        defaults:
          figures:
            figure_default_1_name: figure_default_1_value
            subplots:
              subplot_default_1_name: subpot_default_1_value
              datasets:
                dataset_default_1_name: dataset_default_1_value
                dataset_default_2_name: dataset_default_2_value
      """, presets="""
        available_presets:
          letter:
            _class: target
            _help: letter (width ≤ 6.5", height ≤ 9.0")
            figures:
              fig_width:  9.00
              fig_height: 6.50
              title_fp: 16b
              label_fp: 16b
              shared_legend_kw:
                legend_kw:
                  legend_fp: 14r
              subplots:
                title_fp: 16b
                label_fp: 16b
                tick_fp: 14r
                legend_fp: 14r
                tick_params:
                  length: 3
                  width: 2
                  pad: 6
                legend_kw:
                  legend_fp: 14r
                lw: 2
                datasets:
                  plot_kw:
                    lw: 2
          manuscript:
            _class: target
            _help: manuscript (width ≤ 7.0", height ≤ 9.167")
            figures:
              title_fp: 8b
              label_fp: 8b
              shared_legend_kw:
                legend_kw:
                  title_fp:  8b
                  legend_fp: 6r
              subplots:
                title_fp: 8b
                label_fp: 8b
                tick_fp: 6r
                tick_params:
                  length: 2
                  pad: 3
                  width: 1
                legend_kw:
                  legend_fp: 6r
                y2tick_params:
                  length: 2
                  pad: 3
                  width: 1
                lw: 1
                datasets:
                  plot_kw:
                    lw: 1
          notebook:
            _class: target
            _help: notebook (width ≤ 6.5", height ≤ 9.0")
            figures:
              title_fp: 10b
              label_fp: 10b
              shared_legend_kw:
                legend_kw:
                  legend_fp: 8r
              subplots:
                title_fp: 10b
                label_fp: 10b
                tick_fp: 8r
                tick_params:
                  direction: out
                  length: 2
                  pad: 6
                  width: 1
                legend_kw:
                  legend_fp: 8r
                lw: 1
                y2tick_params:
                  direction: out
                  length: 2
                  pad: 3
                  width: 1
                datasets:
                  plot_kw:
                    lw: 1
          presentation:
            _class: target
            _help: 4:3 presentation (width = 10.24", height = 7.68")
            figures:
              fig_width:  10.24
              fig_height:  7.68
              title_fp:  24b
              label_fp:  24b
              shared_legend_kw:
                legend_kw:
                  legend_fp: 16r
              subplots:
                title_fp: 18r
                label_fp: 18r
                tick_fp:  14r
                tick_params:
                  length: 3
                  pad: 6
                  width: 2
                legend_kw:
                  legend_fp: 14r
                lw: 2
                y2tick_params:
                  length: 3
                  pad: 3
                  width: 2
                datasets:
                  plot_kw:
                    lw:  2
          presentation_wide:
            _class: target
            _help: 16:9 presentation (width = 19.20", height = 10.80")
            figures:
              fig_width:  19.20
              fig_height: 10.80
              title_fp:  24b
              label_fp:  24b
              legend_fp: 24r
              subplots:
                title_fp: 24b
                label_fp: 24b
                tick_fp:  20r
                tick_params:
                  length: 6
                  width: 2
                  pad: 10
                lw: 3
                datasets:
                  plot_kw:
                    lw: 3
      """, sort="""
        header:
          - presets
      """)


#################################### MAIN #####################################
if __name__ == "__main__":
    MYPlotSpecConstructor.main()
