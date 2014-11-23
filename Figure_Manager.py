#!/usr/bin/python
#   plot_toolkit.Figure_Manager.py
#   Written by Karl Debiec on 14-11-17, last updated by Karl Debiec on 14-11-22
"""
Class to manage figure generation
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
from .Figure_Output import Figure_Output
from kwargsieve import Sieve_Kwargs
################################### CLASSES ####################################
def merge_dicts(dict1, dict2):
    def merge(dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(merge(dict1[k], dict2[k])))
                else:
                    yield (k, dict2[k])
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])
    return dict(merge(dict1, dict2))

class Figure_Manager(object):
    """
    Class to manage figure generation
    """

    defaults_yaml = ""
    default_mode  = "default"

    def __init__(self, **kwargs):
        import yaml
        defaults_dict = yaml.load(self.defaults_yaml)

        self.defaults_by_mode = {
          key: merge_dicts(
                 defaults_dict.get("default", {}),
                 defaults_dict.get(key,       {}))
          for key in defaults_dict if key != "default"}

        self.draw_report(**kwargs)

    @Sieve_Kwargs()
    def draw_report(self, mode = None, **kwargs):
        """
        .. todo:
            - Loop over figures properly
            - If outfile is a pdf, open pdfpages and add to dictionary
              of pdfpages object; then add pages as the are generated;
              then close
        """
        if mode is not None:
            self.mode = mode
        else:
            self.mode = self.default_mode
        self.defaults = self.defaults_by_mode.get(self.mode, {})
        self.draw_figure(
          defaults           = self.defaults.get("draw_figure", {}),
          kwarg_pool         = kwargs.get("kwarg_pool", {}),
          kwarg_pool_sources = [["figures", "all"], ["figures", 0]])

    @Sieve_Kwargs()
    @Figure_Output
    def draw_figure(self, title, sharedxlabel, sharedylabel, **kwargs):
        from plot_toolkit import gen_figure_subplots
        from plot_toolkit.text import set_title, set_bigxlabel, set_bigylabel

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
        return figure

    def draw_subplot(self, **kwargs):
        raise NotImplementedError("draw_subplot function is not implemented " +
          "in this base Figure_Manager class")

    def draw_dataset(self, **kwargs):
        raise NotImplementedError("draw_dataset function is not implemented " +
          "in this base Figure_Manager class")
