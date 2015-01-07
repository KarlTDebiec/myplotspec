#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Figure_Manager.py
#   Written by Karl Debiec on 14-11-17, last updated by Karl Debiec on 15-01-06
"""
Class to manage the generation of figures using matplotlib
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
from collections import OrderedDict
from . import merge_dicts, get_yaml
from .Method_Defaults_Presets import Method_Defaults_Presets
from .Manage_Kwargs import Manage_Kwargs
from .Figure_Output import Figure_Output
################################### CLASSES ####################################
class Figure_Manager(object):
    """
    Class to manage the generation of figures using matplotlib
    """
    defaults = """
          draw_figure:
            left:         1
            sub_width:    5.5
            right:        1
            top:          1
            sub_height:   5.5
            bottom:       1
            title_fp:     12r
            label_fp:     12r
            hand:
                stump: 1
                nay:   bama
          draw_subplot:
            title_fp:     12r
            label_fp:     12r
            tick_fp:      10r
            lw:           1
          draw_dataset:
            lw:           1
    """
    presets  = """
        presentation:
          draw_figure:
            title_fp:     24r
            label_fp:     24r
          draw_subplot:
            title_fp:     24r
            label_fp:     24r
            tick_fp:      18r
            legend_fp:    18r
            lw:           2
          draw_dataset:
            lw:           2
        notebook:
          draw_figure:
            title_fp:     12r
            label_fp:     12r
          draw_subplot:
            title_fp:     12r
            label_fp:     12r
            tick_fp:      10r
            legend_fp:    10r
            lw:           1
          draw_dataset:
            lw:           1
        letter:
          draw_figure:
            title_fp:     18r
            label_fp:     18r
          draw_subplot:
            title_fp:     18r
            label_fp:     18r
            tick_fp:      14r
            legend_fp:    14r
            lw:           2
          draw_dataset:
            lw:           2
    """

    def __init__(self, **kwargs):
        """
        Initializes
        """
        self.draw_report(**kwargs)

    @Method_Defaults_Presets()
    @Manage_Kwargs()
    def draw_report(self, **in_kwargs):
        """
        Draws a series of figures based on a series of figure
        specifications

        **Arguments:**
            :*outfile*:
            :*figures*: Figure specifications
        """

        figure_specs   = in_kwargs.pop("figures", {})
        figure_indexes = sorted([i for i in figure_specs.keys()
                           if str(i).isdigit()])
        outfiles       = {}

        # Configure and plot figures
        for i in figure_indexes:
            out_kwargs              = in_kwargs.copy()
            out_kwargs["yaml_keys"] = [["figures", "all"], ["figures", i]]
            out_kwargs["outfiles"]  = outfiles
            self.draw_figure(**out_kwargs)

        # Clean up
        for outfile in outfiles.values():
            outfile.close()

    @Method_Defaults_Presets()
    @Manage_Kwargs()
    @Figure_Output()
    def draw_figure(self, title = None, shared_xlabel = None,
        shared_ylabel = None, shared_legend = None, **in_kwargs):
        """
        Draws a figure

        **Arguments:**
            :*outfile*:       Output filename
            :*title*:         Figure title
            :*shared_xlabel*: X label to be shared among subplots
            :*shared_ylabel*: Y label to be shared among subplots
            :*shared_legend*: Legend to be shared among subplots
        """
        from collections import OrderedDict
        from . import gen_figure_subplots
        from .legend import set_shared_legend
        from .text import set_title, set_bigxlabel, set_bigylabel

        # Prepare figure and subplots with specified dimensions
        subplot_specs    = in_kwargs.pop("subplots", {})
        subplot_indexes  = sorted([i for i in subplot_specs.keys()
                             if str(i).isdigit()])
        figure, subplots = gen_figure_subplots(**in_kwargs)

        # Format Figure
        if str(title) != "None":
            set_title(figure, title = title, **in_kwargs)
        if str(shared_xlabel) != "None":
            set_bigxlabel(figure, label = shared_xlabel, **in_kwargs)
        if str(shared_ylabel) != "None":
            set_bigylabel(figure, label = shared_ylabel, **in_kwargs)
        if str(shared_legend) != "None":
            shared_handles = OrderedDict()

        # Configure and plot subplots
        for i in subplot_indexes:
            out_kwargs                      = {}
            out_kwargs["subplot"]           = subplots[i]
            out_kwargs["debug"]             = in_kwargs.get("debug", False)
            out_kwargs["yaml_dict"]         = in_kwargs.get("yaml_dict", {})
            out_kwargs["yaml_keys"]         = [key
              for key2 in [[key3 + ["subplots", "all"],
                            key3 + ["subplots", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]
            if str(shared_legend) != "None":
                out_kwargs["shared_handles"] = shared_handles
            self.draw_subplot(**out_kwargs)

        # Draw legend
        if str(shared_legend) != "None":
            set_shared_legend(figure, subplots, handles = shared_handles,
              **shared_legend)

        # Return results
        return figure

    @Method_Defaults_Presets()
    @Manage_Kwargs()
    def draw_subplot(self, subplot, title = None, legend = None,
        shared_handles = None, debug = False, **in_kwargs):
        """
        Draws a subplot

        **Arguments:**
            :*subplot*:        <Axes> on which to act
            :*title*:          Subplot's title
            :*legend*:         Subplot's legend
            :*shared_handles*: Nascent OrderedDict of handles and
                               labels shared among subplots of host
                               figure
        """
        from collections import OrderedDict
        from .axes import set_xaxis, set_yaxis
        from .legend import set_legend
        from .text import set_title

        # Format
        set_xaxis(subplot, **in_kwargs)
        set_yaxis(subplot, **in_kwargs)
        if str(title) != "None":
            set_title(subplot, title = title, **in_kwargs)

        # Configure and plot datasets
        handles         = OrderedDict()
        dataset_specs   = in_kwargs.pop("datasets", {})
        dataset_indexes = sorted([i for i in dataset_specs.keys()
                            if str(i).isdigit()])
        for i in dataset_indexes:
            out_kwargs                      = {}
            out_kwargs["debug"]             = in_kwargs.get("debug", False)
            out_kwargs["yaml_dict"]         = in_kwargs.get("yaml_dict", {})
            out_kwargs["yaml_keys"]         = [key
              for key2 in [[key3 + ["datasets", "all"],
                            key3 + ["datasets", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]
            self.draw_dataset(subplot = subplot, handles = handles,
              **out_kwargs)

        # Draw legend
        if str(legend) != "None":
            set_legend(subplot, handles = handles, **in_kwargs)
        if str(shared_handles) != "None":
            for label, handle in handles.items():
                if not label in shared_handles:
                    shared_handles[label] = handle

#    @Select_Defaults()
#    @Collect_Kwargs()
#    @Debug_Args()
#    def draw_dataset(self, subplot, infile, label = "",
#      xoffset = 0, yoffset = 0, handles = OrderedDict(),
#      dataset_kw = {}, plot_kw = {}, **in_kwargs):
#        """
#        Draws a dataset
#
#        **Arguments:**
#            :*subplot*: <Axes> on which to act
#            :*xoffset*: Offset to be added to x coordinates
#            :*yoffset*: Offset to be added to y coordinates
#        """
#        from . import gen_color
#
#        # Loop over infiles
#        dataset = np.loadtxt(infile, **dataset_kw)
#        color   = gen_color(color)
#
#        # Plot
#        import numpy as np
#        handle = subplot.plot(np.random.randn(10)+5, np.random.randn(10)+5,
#          **plot_kw)
#        handles[label] = handle
