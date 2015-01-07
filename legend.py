#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.legend.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec on 15-01-04
"""
Functions for formatting legends

.. todo:
    - Check
    - Allow legend from one figure to be sent to another
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
from .Debug import Debug_Arguments
################################## FUNCTIONS ###################################
def set_legend(subplot, handles = None, legend_kw = {}, **kwargs):
    """
    Draws and formats a legend on *subplot*

    By default includes all series; may alternatively accept manual
    lists of *handles* and *labels* for plotted series

    **Arguments:**
        :*subplot*: <Axes> on which to act
        :*handles*: List of handles for plotted series
        :*labels*:  List of labels for plotted series
        :*fp*:      Legend font; *fontproperties* and *prop* also
                    supported; passed to gen_font(...)

    **Returns:**
        :*legend*:  <Legend>
    """
    from . import multi_kw, gen_font

    legend_kw["prop"] = gen_font(multi_kw(
      ["fp", "fontproperties", "legend_fp", "prop"], "8r", kwargs))
    if str(handles) != "None":
        return subplot.legend(handles.values(), handles.keys(), **legend_kw)
    else:
        return subplot.legend(**legend_kw)

def set_shared_legend(figure, subplots, **kwargs):
    """
    """
    from . import gen_figure_subplots
    from .axes import set_xaxis, set_yaxis

    figure, subplots = gen_figure_subplots(
      figure = figure, subplots = subplots, **kwargs)
    subplot = subplots[len(subplots) - 1]
    legend  = set_legend(subplot, **kwargs)
    set_xaxis(subplot, ticks = [])
    set_yaxis(subplot, ticks = [])
    for spine in subplot.spines.values():
        spine.set_visible(False)
    for handle in legend.legendHandles:
        handle.set_linewidth(5.0)
    legend.draw_frame(False)

