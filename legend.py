# -*- coding: utf-8 -*-
#   myplotspec.legend.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
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

    title_fp = multi_get_copy(["legend_title_fp"] + FP_KEYS, kwargs)
    title_fp_2 = multi_pop(["legend_title_fp", "title_fp"],legend_kw)
    if title_fp_2 is not None:
        title_fp = get_font(title_fp_2)
    elif title_fp is not None:
        title_fp = get_font(title_fp)
    elif "prop" in legend_kw:
        title_fp = legend_kw["prop"]

    # Draw and format legend
    if handles is not None:
        legend = subplot.legend(handles.values(), handles.keys(), **legend_kw)
    else:
        legend = subplot.legend(**legend_kw)

    if title_fp is not None:
        legend.get_title().set_fontproperties(title_fp)

    return legend

def set_shared_legend(figure, subplots, handles, mode="manual", spines=False,
    **kwargs):
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
    from collections import OrderedDict
    from . import (get_colors, get_figure_subplots, get_font, multi_get_copy,
                   multi_get)
    from .axes import set_xaxis, set_yaxis

    # Add subplot to figure, draw and format legend
    if mode == "manual":
        figure, subplots = get_figure_subplots(figure=figure, subplots=subplots,
          verbose=0, **kwargs)
        subplot = subplots[len(subplots) - 1]
    elif mode == "partner":
        from .axes import add_partner_subplot

        subplot = add_partner_subplot(subplots[0], figure, subplots, **kwargs)

    handle_kw = kwargs.get("handle_kw", {})
    get_colors(handle_kw)
    if not isinstance(handles, OrderedDict):
        handles = OrderedDict(handles)
    for label, handle in handles.items():
        if isinstance(handle, dict):
            get_colors(handle)
            h_kw = handle_kw.copy()
            h_kw.update(handle)
            handles[label] = subplot.plot((-1),(-1), **h_kw)[0]

    legend = set_legend(subplot, handles=handles, **kwargs)

    # Hide subplot borders
    set_xaxis(subplot, xbound=[0,1], xticks=[])
    set_yaxis(subplot, ybound=[0,1], yticks=[])
    if not spines:
        for spine in subplot.spines.values():
            spine.set_visible(False)
    return legend
