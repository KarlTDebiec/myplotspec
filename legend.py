#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.legend.py
#   Written:    Karl Debiec     12-10-22
#   Updated:    Karl Debiec     15-01-10
"""
Functions for formatting legends

Note: Acceptable values of *loc* and their meanings, for reference:

::

    0 = Best
    +---------+
    |2   9   1|
    |6  10   7|
    |3   8   4|
    +---------+

"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_legend(subplot, handles = None, legend_lw = None, legend_fp = None,
    **kwargs):
    """
    Draws and formats a legend on *subplot*

    By default includes all series; may alternatively accept manual
    OrderedDict of handles and labels

    **Arguments:**
        :*subplot*:   <Axes> on which to act
        :*handles*:   OrderedDict; keys are series labels and values
                      are handles
        :*legend_lw*: Legend handle linewidth
        :*legend_fp*: Legend font
        :*legend_kw*: Keyword arguments passed to *subplot*.legend()

    **Returns:**
        :*legend*: <Legend>
    """
    from . import fp_keys, get_font, multi_kw

    # Manage arguments
    legend_kw   = kwargs.pop("legend_kw", {})
    legend_fp_2 = multi_kw(["legend_fp"] + fp_keys, legend_kw)
    if legend_fp_2 is not None:
        legend_kw["prop"] = get_font(legend_fp_2)
    elif legend_fp is not None:
        legend_kw["prop"] = get_font(legend_fp)

    # Draw and format legend
    if handles is not None:
        legend = subplot.legend(handles.values(), handles.keys(), **legend_kw)
    else:
        legend = subplot.legend(**legend_kw)
    if legend_lw is not None:
        for handle in legend.legendHandles:
            handle.set_linewidth(legend_lw)
    return legend

def set_shared_legend(figure, subplots, **kwargs):
    """
    Adds a subplot to *figure*, draws a legend on it and hides subplot
    borders

    Useful when several plots on the same figure share the same source.

    **Arguments:**
        :*figure*:   Figure
        :*subplots*: OrderedDict of subplots

    **Returns:**
        :*legend*: new legend
    """
    from . import gen_figure_subplots, get_font
    from .axes import set_xaxis, set_yaxis

    # Add subplot to figure, draw and format legend
    figure, subplots = gen_figure_subplots(
      figure = figure, subplots = subplots, **kwargs)
    subplot = subplots[len(subplots) - 1]
    legend  = set_legend(subplot, **kwargs)

    # Hide subplot borders
    set_xaxis(subplot, xticks = [])
    set_yaxis(subplot, yticks = [])
    for spine in subplot.spines.values():
        spine.set_visible(False)

    return legend
