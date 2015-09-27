# -*- coding: utf-8 -*-
#   myplotspec.legend.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Functions for formatting legends.

Note:
  Acceptable values of ``loc`` and their meanings, for reference::

    0 = Best
    +---------+
    |2   9   1|
    |6  10   7|
    |3   8   4|
    +---------+

.. todo:
  - Double-check if legend and shared_legend are passed arguments in consistent
    style
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_legend(subplot, handles=None, **kwargs):
    """
    Draws and formats a legend on a subplot.

    Arguments:
      subplot (Axes): Subplot to which to add legend
      handles (OrderedDict): Collection of [labels]: handles for
        datasets to be plotted on legend; by default all available
        datasets are included
      legend_lw (float): Legend handle linewidth
      legend_fp (str, dict, FontProperties): Legend font
      legend_kw (dict): Keyword arguments passed to subplot.legend()

    Returns:
      (Legend): Legend

    .. todo:
      - Test legend title and accept font properties setting
    """
    from . import FP_KEYS, get_font, multi_get_copy, multi_pop

    # Manage arguments
    legend_kw = multi_get_copy("legend_kw", kwargs, {})
    legend_fp = multi_get_copy(["legend_fp"] + FP_KEYS, kwargs)
    legend_fp_2 = multi_pop(["legend_fp"] + FP_KEYS, legend_kw)
    if legend_fp_2 is not None:
        legend_kw["prop"] = get_font(legend_fp_2)
    elif legend_fp is not None:
        legend_kw["prop"] = get_font(legend_fp)

    # Draw and format legend
    if handles is not None:
        legend = subplot.legend(handles.values(), handles.keys(), **legend_kw)
    else:
        legend = subplot.legend(**legend_kw)
#    if legend_lw is not None:
#        for handle in legend.legendHandles:
#            handle.set_linewidth(legend_lw)
    return legend

def set_shared_legend(figure, subplots, **kwargs):
    """
    Draws a legend on a figure, shared by multiple subplots.

    Useful when several plots on the same figure share the same
    description and plot style.

    Arguments:
      figure (Figure): Figure to which to add shared legend
      subplots (OrderedDict): Collection of subplots to which to append
        new subplot for shared legend

    Returns:
      (Legend): Legend
    """
    from . import get_figure_subplots, get_font, multi_get_copy, multi_get
    from .axes import set_xaxis, set_yaxis

    shared_legend_kw = multi_get_copy("shared_legend_kw", kwargs, {})
    handles = multi_get(["shared_handles", "handles"], kwargs)

    # Add subplot to figure, draw and format legend
    figure, subplots = get_figure_subplots(figure=figure, subplots=subplots,
      **shared_legend_kw)
    subplot = subplots[len(subplots) - 1]
    legend = set_legend(subplot, handles=handles, **shared_legend_kw)

    # Hide subplot borders
    set_xaxis(subplot, xticks=[])
    set_yaxis(subplot, yticks=[])
    for spine in subplot.spines.values():
        spine.set_visible(False)

    return legend
