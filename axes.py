# -*- coding: utf-8 -*-
#   myplotspec.axes.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Functions for formatting axes.

.. todo:
    - Figure out how to use multiple-keyword arguments (e.g. [x]tick[label]_fp
      with sphinx
    - Reimplement set_multi and set_colorbar
    - Figure out how to adjust the positions of specific ticks properly
      and automatically ('1' often looks bad)
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_xaxis(subplot, xticks=None, xticklabels=None, xtick_fp=None,
    tick_fp=None, xticklabel_fp=None, ticklabel_fp=None, xlabel=None,
    xlabel_fp=None, label_fp=None, xtick_params=None, tick_params=None,
    xlw=None, lw=None, **kwargs):
    """
    Formats the x axis of a subplot using provided keyword arguments.

    Arguments:
      subplot (Axes): Axes to format
      xticks (list or ndarray): Ticks; first and last are used as upper
        and lower boundaries
      xtick_kw (dict): Keyword arguments passed to subplot.set_xticks()
      xticklabels (list): Tick label text
      [x]tick[label]_fp (str, dict, FontProperties): Tick label
        font
      xticklabel_kw (dict): Keyword arguments passed to
        subplot.set_xticklabels()
      xlabel (str): Label text
      [x]label_fp (str, dict, FontProperties): Label font
      xlabel_kw (dict): Keyword arguments passed to subplot.set_xlabel()
      [x]tick_params (dict): Keyword arguments passed to
        subplot.set_tick_params(); only affect x axis
      [x]lw (float): Subplot top and bottom line width
      kwargs (dict): Additional keyword arguments
    """
    from . import FP_KEYS, get_font, multi_kw

    # Ticks
    xtick_kw = kwargs.pop("xtick_kw", {})
    xticks_2 = multi_kw(["xticks", "ticks"], xtick_kw)
    if xticks_2 is not None:
        xticks = xticks_2
    if xticks is not None:
        if xticks != []:
            subplot.set_xbound(float(xticks[0]), float(xticks[-1]))
        subplot.set_xticks(xticks, **xtick_kw)

    # Tick labels
    xticklabel_kw = kwargs.pop("xticklabel_kw", {})
    xticklabels_2 = multi_kw(["xticklabels", "ticklabels"], xticklabel_kw)
    if xticklabels_2 is not None:
        xticklabels = xticklabels_2
    if xticklabels is None and xticks is not None:
        xticklabels = xticks

    xticklabel_fp_2 = multi_kw(["xtick_fp", "tick_fp", "xticklabel_fp",
                        "ticklabel_fp"] + FP_KEYS, xticklabel_kw)
    if xticklabel_fp_2 is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp_2)
    elif xtick_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(xtick_fp)
    elif xticklabel_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp)
    elif tick_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(tick_fp)
    elif ticklabel_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(ticklabel_fp)

    if xticklabels is not None:
        subplot.set_xticklabels(xticklabels, **xticklabel_kw)

    # Label
    xlabel_kw = kwargs.pop("xlabel_kw", {})
    xlabel_2  = multi_kw(["xlabel", "label"], xlabel_kw)
    if xlabel_2 is not None:
        xlabel = xlabel_2

    xlabel_fp_2 = multi_kw(["xlabel_fp", "label_fp"] + FP_KEYS, xlabel_kw)
    if xlabel_fp_2 is not None:
        xlabel_kw["fontproperties"] = get_font(xlabel_fp_2)
    elif xlabel_fp is not None:
        xlabel_kw["fontproperties"] = get_font(xlabel_fp)
    elif label_fp is not None:
        xlabel_kw["fontproperties"] = get_font(label_fp)

    if xlabel is not None:
        subplot.set_xlabel(xlabel, **xlabel_kw)

    # Tick parameters
    if xtick_params is not None:
        tick_params = xtick_params
    if tick_params is not None:
        tick_params["axis"] = "x"
        subplot.tick_params(**tick_params)

    # Line width
    if xlw is not None:
        lw = xlw
    if lw is not None:
        subplot.spines["top"].set_lw(lw)
        subplot.spines["bottom"].set_lw(lw)

def set_yaxis(subplot, subplot_y2=None, yticks=None, y2ticks=None,
    yticklabels=None, y2ticklabels=None, ytick_fp=None, y2tick_fp=None,
    tick_fp=None, yticklabel_fp=None, y2ticklabel_fp=None, ticklabel_fp=None,
    ylabel=None, y2label=None, ylabel_fp=None, y2label_fp=None, label_fp=None,
    ytick_params=None, y2tick_params=None, tick_params=None, ylw=None, lw=None,
    **kwargs):
    """
    Formats the y axis of a subplot using provided keyword arguments.

    Arguments:
      subplot (Axes): Axes to format
      subplot_y2 (Axes, optional): Second y axes to format; if this is
        omitted, but y2ticks is included, the second y axis will be
        generated
      yticks (list or ndarray): Ticks; first and last are used as upper
        and lower boundaries
      ytick_kw (dict): Keyword arguments passed to subplot.set_yticks()
      yticklabels (list): Tick label text
      [y]tick[label]_fp (str, dict, FontProperties): Tick label font
      yticklabel_kw (dict): Keyword arguments passed to
        subplot.set_yticklabels()
      ylabel (str): Label text
      [y]label_fp (str, dict, FontProperties): Label font
      ylabel_kw (dict): Keyword arguments passed to subplot.set_ylabel()
      [y]tick_params (dict): Keyword arguments passed to
        subplot.set_tick_params(); only affect y axis
      [y]lw (float): Subplot top and bottom line width
      y2ticks (list or ndarray): Ticks for second y axis; first and last
        are used as upper and lower boundaries; if this argument is
        provided, a y2 axis is generated using subplot.twiny()
      y2tick_kw (dict): Keyword arguments passed to subplot.set_yticks()
        for second y axis
      y2ticklabels (list): Tick label text for second y axis
      [y2]tick[label]_fp (str, dict, FontProperties): Tick label font
        for second y axis
      y2ticklabel_kw (dict): Keyword arguments passed to
        subplot.set_yticklabels() for second y axis
      y2label (str): Label text for second y axis
      [y2]label_fp (str, dict, FontProperties): Label font for second y
        axis
      y2label_kw (dict): Keyword arguments passed to subplot.set_ylabel()
        for second y axis
      kwargs (dict): Additional keyword arguments
    """
    from . import FP_KEYS, get_font, multi_kw

    # Y1 Ticks
    ytick_kw = kwargs.pop("ytick_kw", {})
    yticks_2 = multi_kw(["yticks", "ticks"], ytick_kw)
    if yticks_2 is not None:
        yticks = yticks_2
    if yticks is not None:
        if yticks != []:
            subplot.set_ybound(float(yticks[0]), float(yticks[-1]))
        subplot.set_yticks(yticks, **ytick_kw)

    # Y1 Tick labels
    yticklabel_kw = kwargs.pop("yticklabel_kw", {})
    yticklabels_2 = multi_kw(["yticklabels", "ticklabels"], yticklabel_kw)
    if yticklabels_2 is not None:
        yticklabels = yticklabels_2
    if yticklabels is None and yticks is not None:
        yticklabels = yticks

    yticklabel_fp_2 = multi_kw(["ytick_fp", "tick_fp", "yticklabel_fp",
                        "ticklabel_fp"] + FP_KEYS, yticklabel_kw)
    if yticklabel_fp_2 is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp_2)
    elif ytick_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(ytick_fp)
    elif yticklabel_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp)
    elif tick_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(tick_fp)
    elif ticklabel_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(ticklabel_fp)

    if yticklabels is not None:
        subplot.set_yticklabels(yticklabels, **yticklabel_kw)

    # Y1 Label
    ylabel_kw = kwargs.pop("ylabel_kw", {})
    ylabel_2 = multi_kw(["ylabel", "label"], ylabel_kw)
    if ylabel_2 is not None:
        ylabel = ylabel_2

    ylabel_fp_2 = multi_kw(["ylabel_fp", "label_fp"] + FP_KEYS, ylabel_kw)
    if ylabel_fp_2 is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp_2)
    elif ylabel_fp is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp)
    elif label_fp is not None:
        ylabel_kw["fontproperties"] = get_font(label_fp)

    if ylabel is not None:
        subplot.set_ylabel(ylabel, **ylabel_kw)

    # Y1 tick parameters
    if ytick_params is not None:
        tick_params = ytick_params
    if tick_params is not None:
        tick_params["axis"] = "y"
        subplot.tick_params(**tick_params)

    # Line width
    if ylw is not None:
        lw = ylw
    if lw is not None:
        subplot.spines["left"].set_lw(lw)
        subplot.spines["right"].set_lw(lw)

    # Y2 Ticks, if applicable
    y2tick_kw = kwargs.pop("y2tick_kw", {})
    y2ticks_2 = multi_kw(["y2ticks", "ticks"], y2tick_kw)
    if y2ticks_2 is not None:
        y2ticks = y2ticks_2
    if y2ticks is not None:
        if subplot_y2 is None:
            subplot_y2 = subplot.twinx()
            subplot_y2.set_autoscale_on(False)
        if y2ticks != []:
            subplot_y2.set_ybound(float(y2ticks[0]), float(y2ticks[-1]))
        subplot_y2.set_yticks(y2ticks, **y2tick_kw)

    # Y2 Tick labels
    if subplot_y2 is not None:
        y2ticklabel_kw = kwargs.pop("y2ticklabel_kw", {})
        y2ticklabels_2 = multi_kw(["y2ticklabels", "ticklabels"],
          y2ticklabel_kw)
        if y2ticklabels_2 is not None:
            y2ticklabels = y2ticklabels_2
        if y2ticklabels is None and y2ticks is not None:
            y2ticklabels = y2ticks

        y2ticklabel_fp_2 = multi_kw(["y2tick_fp", "tick_fp", "y2ticklabel_fp",
                            "ticklabel_fp"] + FP_KEYS, y2ticklabel_kw)
        if y2ticklabel_fp_2 is not None:
            y2ticklabel_kw["fontproperties"] = get_font(y2ticklabel_fp_2)
        elif y2tick_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(y2tick_fp)
        elif y2ticklabel_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(y2ticklabel_fp)
        elif ytick_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(ytick_fp)
        elif yticklabel_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(yticklabel_fp)
        elif tick_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(tick_fp)
        elif ticklabel_fp is not None:
            y2ticklabel_kw["fontproperties"] = get_font(ticklabel_fp)

        if y2ticklabels is not None:
            subplot_y2.set_yticklabels(y2ticklabels, **y2ticklabel_kw)

    # Y2 Label
    if subplot_y2 is not None:
        y2label_kw = kwargs.pop("y2label_kw", {})
        y2label_2 = multi_kw(["y2label", "label"], y2label_kw)
        if ylabel_2 is not None:
            y2label = y2label_2

        y2label_fp_2 = multi_kw(["y2label_fp", "label_fp"] + FP_KEYS,
          y2label_kw)
        if y2label_fp_2 is not None:
            y2label_kw["fontproperties"] = get_font(y2label_fp_2)
        elif y2label_fp is not None:
            y2label_kw["fontproperties"] = get_font(y2label_fp)
        elif label_fp is not None:
            y2label_kw["fontproperties"] = get_font(label_fp)

        if y2label is not None:
            subplot_y2.set_ylabel(y2label, **y2label_kw)

    # Y2 Tick parameters
    if subplot_y2 is not None:
        if y2tick_params is not None:
            tick_params = y2tick_params
        if tick_params is not None:
            tick_params["axis"] = "y"
            subplot_y2.tick_params(**tick_params)

def add_secondary_plot(figure, subplots, **kwargs):
    """
    """
    from . import get_figure_subplots, get_font
    from .axes import set_xaxis, set_yaxis

    # Add subplot to figure and format
    figure, subplots = get_figure_subplots(figure=figure, subplots=subplots,
      **kwargs)
    subplot = subplots[len(subplots) - 1]

    return subplot

########################### TEMPORARILY DEPRECIATED ###########################
#def set_multi(subplots, first, nrows, ncols, xaxis_kw, yaxis_kw, **kwargs):
#    ""
#    Formats a set of multiple plots
#
#    Arguments:
#        subplots: OrderedDict of <Axes> on which at act
#        first:    Index of first plot in multiple
#        nrows:    Number of rows of plots in multiple
#        ncols:    Number of columns of plots in multiple
#        xaxis_kw:  Keyword arguments to be passed to set_xaxis
#        yaxis_kw:  Keyword arguments to be passed to set_yaxis
#
#    .. todo:
#        - Smooth passage of keyword arguments from x/yaxis_kw and kwargs
#          to set_bigx/ylabel
#    """
#    xticks      = xaxis_kw.pop("ticks")
#    xticklabels = xaxis_kw.pop("ticklabels", xticks)
#
#    xlabel_kw = dict(xlabel = xaxis_kw.pop("label", kwargs.pop("xlabel", "")))
#    for kw in ["label_fp", "bottom", "top"]:
#        if kw in  kwargs: xlabel_kw[kw] =  kwargs.get(kw)
#    for kw in ["label_fp", "bottom", "top", "x", "y", "ha", "va", "rotation"]:
#        if kw in xaxis_kw: xlabel_kw[kw] = xaxis_kw.pop(kw)
#    if "xlabel_kw" in xaxis_kw: xlabel_kw.update(xaxis_kw.pop("xlabel_kw"))
#
#    yticks      = yaxis_kw.pop("ticks")
#    yticklabels = yaxis_kw.pop("ticklabels", yticks)
#
#    ylabel_kw = dict(ylabel = yaxis_kw.pop("label", kwargs.pop("ylabel", "")))
#    for kw in ["label_fp", "left", "right"]:
#        if kw in  kwargs: ylabel_kw[kw] =  kwargs.get(kw)
#    for kw in ["label_fp", "left", "right", "x", "y", "ha", "va", "rotation"]:
#        if kw in yaxis_kw: ylabel_kw[kw] = yaxis_kw.pop(kw)
#    if "ylabel_kw" in yaxis_kw: ylabel_kw.update(yaxis_kw.pop("ylabel_kw"))
#
#    xaxis_kw.update(kwargs)
#    yaxis_kw.update(kwargs)
#
#    # Loop over subplots
#    for i in range(first, first + (nrows * ncols), 1):
#
#        # Format x axes
#        if   (i == first + (nrows * ncols) - 1):
#            set_xaxis(subplots[i], ticks = xticks,
#              ticklabels = xticklabels, **xaxis_kw)
#        elif (i in range(first + ((nrows - 1) * ncols),
#           first + (nrows * ncols) - 1, 1)):
#            set_xaxis(subplots[i], ticks = xticks,
#              ticklabels = xticklabels[:-1], **xaxis_kw)
#        else:
#            set_xaxis(subplots[i], ticks = xticks,
#              ticklabels = [], **xaxis_kw)
#
#        # Format y axes
#        if   (i == first):
#            set_yaxis(subplots[i], ticks = yticks, ticklabels = yticklabels,
#              **yaxis_kw)
#        elif (i in range(first + nrows, first + (nrows * ncols), nrows)):
#            set_yaxis(subplots[i], ticks = yticks,
#              ticklabels = yticklabels[:-1], **yaxis_kw)
#        else:
#            set_yaxis(subplots[i], ticks = yticks,
#              ticklabels = [], **yaxis_kw)
#    set_bigxlabel(dict((j, subplots[j])
#      for j in range(first, first + (nrows * ncols), 1)), **xlabel_kw)
#    set_bigylabel(dict((j, subplots[j])
#      for j in range(first, first + (nrows * ncols), 1)), **ylabel_kw)
#
#def set_colorbar(cbar, ticks, ticklabels=None, label="", label_fp="11b",
#    **kwargs):
#    """
#    Formats a colorbar
#
#    Arguments:
#        cbar:       <ColorBar> to act on
#        ticks:      Ticks
#        ticklabels: Tick labels
#        tick_fp:    Tick label font; passed to get_font(...)
#        label:      Label text
#        label_fp:   Label font; passed to get_font(...)
#    """
#    import warnings
#
#    if ticklabels is None:
#        ticklabels = ticks
#    zticks  = numpy.array(ticks, numpy.float32)
#    zticks  = (zticks - zticks[0]) / (zticks[-1] - zticks[0])
#    cbar.ax.tick_params(bottom = "off", top = "off", left = "off",
#      right = "off")
#    cbar.set_ticks(ticks)
#    with warnings.catch_warnings():
#        warnings.simplefilter("ignore")
#        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [])
#        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticklabels,
#          tick_fp = tick_fp)
#    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
#    cbar.set_label(label, fontproperties = get_font(label_fp))
