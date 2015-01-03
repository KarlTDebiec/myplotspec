#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Figure_Manager.py
#   Written by Karl Debiec on 14-11-17, last updated by Karl Debiec on 15-01-03
"""
Class to manage the generation of figures using matplotlib

.. todo:
    - Check
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
from .Figure_Output import Figure_Output
from . import merge_dicts
from kwargsieve import Collect_Kwargs
################################### CLASSES ####################################
class Figure_Manager(object):
    """
    Class to manage the generation of figures using matplotlib
    """

    defaults_yaml = ""
    default_mode  = "default"

    def __init__(self, **kwargs):
        """
        """
        import yaml
        defaults_dict = yaml.load(self.defaults_yaml)

        self.defaults_by_mode = {
          key: merge_dicts(
                 defaults_dict.get("default", {}),
                 defaults_dict.get(key,       {}))
          for key in defaults_dict if key != "default"}

        self.draw_report(**kwargs)

    @Collect_Kwargs()
    def draw_report(self, mode = None, **kwargs):
        """
        DOCUMENT

        .. todo:
            - If outfile is a pdf, open pdfpages and add to dictionary
              of pdfpages object; then add pages as the are generated;
              then close
        """
        if mode is not None:
            self.mode = mode
        else:
            self.mode = self.default_mode
        self.defaults = self.defaults_by_mode.get(self.mode, {})
        figure_spec    = kwargs.pop("figures", {})
        figure_indexes = sorted([i for i in figure_spec.keys()
                           if str(i).isdigit()])

        for i in figure_indexes:
            self.draw_figure(
              defaults           = self.defaults.get("draw_figure", {}),
              kwarg_pool         = kwargs.get("kwarg_pool", {}),
              kwarg_pool_sources = [["figures", "all"], ["figures", i]])

    @Collect_Kwargs()
    @Figure_Output
    def draw_figure(self, title = None, sharedxlabel = None,
        sharedylabel = None, **kwargs):
        """
        DOCUMENT

        **Arguments:**
            :*title*:        Figure title
            :*sharedxlabel*: X label to be shared among subplots
            :*sharedylabel*: Y label to be shared among subplots
        """
        from MYPlotSpec import gen_figure_subplots
        from MYPlotSpec.text import set_title, set_bigxlabel, set_bigylabel

        # Prepare figure and subplots with specified dimensions
        subplots_spec    = kwargs.pop("subplots", {})
        subplot_indexes  = sorted([i for i in subplots_spec.keys()
                             if str(i).isdigit()])
        figure, subplots = gen_figure_subplots(**kwargs)

        # Format
        if title is not None and str(title) != "None":
            set_title(figure,     title = title, **kwargs)
        if sharedxlabel is not None and str(sharedxlabel) != "None":
            set_bigxlabel(figure, label = sharedxlabel, **kwargs)
        if sharedylabel is not None and str(sharedylabel) != "None":
            set_bigylabel(figure, label = sharedylabel, **kwargs)

        # Configure and plot subplots
        figure_kwarg_pool_sources = kwargs.pop("kwarg_pool_sources")
        for i in subplot_indexes:
            subplot_kwarg_pool_sources = []
            for figure_kwarg_pool_source in figure_kwarg_pool_sources:
                subplot_kwarg_pool_sources += [
                  figure_kwarg_pool_source + ["subplots", "all"],
                  figure_kwarg_pool_source + ["subplots", i]]
            self.draw_subplot(subplot = subplots[i],
              defaults           = self.defaults.get("draw_subplot", {}),
              kwarg_pool         = kwargs.get("kwarg_pool", {}),
              kwarg_pool_sources = subplot_kwarg_pool_sources)

        # Return results

    @Collect_Kwargs()
    def draw_subplot(self, subplot, title = None, legend = True, **kwargs):
        """
        DOCUMENT

        **Arguments:**
            :*subplot*: <Axes> on which to act
            :*title*:   Subplot's title
            :*legend*:  Subplot's legend
        """
        from MYPlotSpec.axes import set_xaxis, set_yaxis
        from MYPlotSpec.legend import set_legend
        from MYPlotSpec.text import set_title

        # Get dataset specification
        dataset_spec    = kwargs.pop("datasets", {})
        dataset_indexes = sorted([i for i in dataset_spec.keys()
                            if str(i).isdigit()])

        # Format
        set_xaxis(subplot, **kwargs)
        set_yaxis(subplot, **kwargs)
        if title is not None and str(title) != "None":
            set_title(subplot, title = title, **kwargs)

        # Loop over datasets
        handles = []
        labels  = []
        subplot_kwarg_pool_sources = kwargs.pop("kwarg_pool_sources")
        for i in dataset_indexes:
            dataset_kwarg_pool_sources = []
            for subplot_kwarg_pool_source in subplot_kwarg_pool_sources:
                dataset_kwarg_pool_sources += [
                  subplot_kwarg_pool_source + ["datasets", "all"],
                  subplot_kwarg_pool_source + ["datasets", i]]
            self.draw_dataset(
                subplot            = subplot,
                handles            = handles,
                labels             = labels,
                defaults           = self.defaults.get("draw_dataset", {}),
                kwarg_pool         = kwargs.get("kwarg_pool", {}),
                kwarg_pool_sources = dataset_kwarg_pool_sources)

        # Draw legend
        if legend:
            set_legend(subplot, handles = handles, labels = labels, **kwargs)

    @Collect_Kwargs()
    def draw_dataset(self, subplot, label = "", color = "blue", lw = 1,
      ls = "-", xoffset = 0, yoffset = 0, handles = [], labels = [], 
      dataset_kw = {}, plot_kw = {}, **kwargs):
        """
        DOCUMENT

        **Arguments:**
            :*subplot*: <Axes> on which to act
            :*xoffset*: Offset to be added to x coordinates
            :*yoffset*: Offset to be added to y coordinates
        """
        from MYPlotSpec import  gen_color
        kwargs.pop("kwarg_pool")

        # Loop over infiles
#        dataset = FPLC_Dataset(**kwargs)
#        labels += [label]
#        color   = gen_color(color)

        # Plot
#        handles += subplot.plot(
#          dataset.absorbance_280["volume_eluted_mL"] - xoffset,
#          dataset.absorbance_280["A280_AU"] - yoffset,
#          color = color, lw = lw, ls = ls, **plot_kw)
