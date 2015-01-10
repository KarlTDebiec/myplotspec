#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.axes.py
#   Written:    Karl Debiec     13-10-22
#   Updated:    Karl Debiec     15-01-10
"""
Functions for formatting axes

.. todo:
    - Reimplement set_multi and set_colorbar
    - Reimplement support for second x and y axes
    - Figure out how to adjust the positions of specific ticks properly
      and automatically ('1' often looks bad)
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_xaxis(subplot, xticks = None, xtick_kw = None, xticklabels = None,
    xticklabel_fp = None, ticklabel_fp = None, xticklabel_kw = None,
    xlabel = None, xlabel_fp = None, label_fp = None, xlabel_kw = None,
    xtick_params = None, tick_params = None, xtick_pad = None, tick_pad = None,
    xlw = None, lw = None, **kwargs):
    """
    Formats the x-axis of a subplot using provided keyword arguments

    **Arguments:**
        :*subplot*:        <Axes> on which to act
        :*xticks*:          Ticks; first and last are used as upper and
                            lower boundaries
        :*xtick_kw*:        Keyword arguments passed to set_xticks()
        :*xticklabels*:     Tick label text
        :*[x]ticklabel_fp*: Tick label font
        :*xticklabel_kw*:   Keyword arguments passed to
                            set_xticklabels()
        :*xlabel*:          Label text
        :*[x]label_fp*:     Label font
        :*xlabel_kw*:       Keyword arguments passed to set_xlabel()
        :*[x]tick_params*:  Keyword arguments passed to
                            set_tick_params(); only affect x axis
        :*xaxis_kw*:        Additional keyword arguments
        :*[x]tick_pad*: Padding between ticks and labels
        :*[x]lw*:       Line width
    """
    from . import fp_keys, get_font, multi_kw

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

    xticklabel_fp_2 = multi_kw(["xticklabel_fp", "ticklabel_fp"] + fp_keys,
                        xticklabel_kw)
    if xticklabel_fp_2 is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp_2)
    elif xticklabel_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp)
    elif ticklabel_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(ticklabel_fp)

    if xticklabels is not None:
        subplot.set_xticklabels(xticklabels, **xticklabel_kw)

    # Label
    xlabel_kw = kwargs.pop("xlabel_kw", {})
    xlabel_2  = multi_kw(["xlabel", "label"], xlabel_kw)
    if xlabel_2 is not None:
        xlabel = xlabel_2

    xlabel_fp_2 = multi_kw(["xlabel_fp", "label_fp"] + fp_keys, xlabel_kw)
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

    # Additional settings
    if xtick_pad is not None:
        tick_pad = xtick_pad
    if tick_pad is not None:
        for tick in subplot.get_major_ticks():
            tick.set_pad(tick_pad)

    if xlw is not None:
        lw = xlw
    if lw is not None:
        subplot.spines["top"].set_lw(lw)
        subplot.spines["bottom"].set_lw(lw)

def set_yaxis(subplot, yticks = None, ytick_kw = None, yticklabels = None,
    yticklabel_fp = None, ticklabel_fp = None, yticklabel_kw = None,
    ylabel = None, ylabel_fp = None, label_fp = None, ylabel_kw = None,
    ytick_params = None, tick_params = None,  ytick_pad = None,
    tick_pad = None, ylw = None, lw = None, **kwargs):
    """
    Formats the y-axis of a subplot using provided keyword arguments

    **Arguments:**
        :*subplot*:        <Axes> on which to act
        :*yticks*:          Ticks; first and last are used as upper and
                            lower boundaries
        :*ytick_kw*:        Keyword arguments passed to set_yticks()
        :*yticklabels*:     Tick label text
        :*[y]ticklabel_fp*: Tick label font
        :*yticklabel_kw*:   Keyword arguments passed to
                            set_yticklabels()
        :*ylabel*:          Label text
        :*[y]label_fp*:     Label font
        :*ylabel_kw*:       Keyword arguments passed to set_ylabel()
        :*[y]tick_params*:  Keyword arguments passed to
                            set_tick_params(); only affect y axis
        :*yaxis_kw*:        Additional keyword arguments
        :*[y]tick_pad*:     Padding between ticks and labels
        :*[y]lw*:           Line width

    """
    from . import fp_keys, get_font, multi_kw

    # Ticks
    ytick_kw = kwargs.pop("ytick_kw", {})
    yticks_2 = multi_kw(["yticks", "ticks"], ytick_kw)
    if yticks_2 is not None:
        yticks = yticks_2
    if yticks is not None:
        if yticks != []:
            subplot.set_ybound(float(yticks[0]), float(yticks[-1]))
        subplot.set_yticks(yticks, **ytick_kw)

    # Tick labels
    yticklabel_kw = kwargs.pop("yticklabel_kw", {})
    yticklabels_2 = multi_kw(["yticklabels", "ticklabels"], yticklabel_kw)
    if yticklabels_2 is not None:
        yticklabels = yticklabels_2
    if yticklabels is None and yticks is not None:
        yticklabels = yticks

    yticklabel_fp_2 = multi_kw(["yticklabel_fp", "ticklabel_fp"] + fp_keys,
                        yticklabel_kw)
    if yticklabel_fp_2 is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp_2)
    elif yticklabel_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp)
    elif ticklabel_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(ticklabel_fp)

    if yticklabels is not None:
        subplot.set_yticklabels(yticklabels, **yticklabel_kw)

    # Label
    ylabel_kw = kwargs.pop("ylabel_kw", {})
    ylabel_2  = multi_kw(["ylabel", "label"], ylabel_kw)
    if ylabel_2 is not None:
        ylabel = ylabel_2

    ylabel_fp_2 = multi_kw(["ylabel_fp", "label_fp"] + fp_keys, ylabel_kw)
    if ylabel_fp_2 is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp_2)
    elif ylabel_fp is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp)
    elif label_fp is not None:
        ylabel_kw["fontproperties"] = get_font(label_fp)

    if ylabel is not None:
        subplot.set_ylabel(ylabel, **ylabel_kw)

    # Tick parameters
    if ytick_params is not None:
        tick_params = ytick_params
    if tick_params is not None:
        tick_params["axis"] = "y"
        subplot.tick_params(**tick_params)

    # Additional settings
    if ytick_pad is not None:
        tick_pad = ytick_pad
    if tick_pad is not None:
        for tick in subplot.get_major_ticks():
            tick.set_pad(tick_pad)

    if ylw is not None:
        lw = ylw
    if lw is not None:
        subplot.spines["left"].set_lw(lw)
        subplot.spines["right"].set_lw(lw)

########################### TEMPORARILY DEPRECIATED ###########################
#def set_multi(subplots, first, nrows, ncols, xaxis_kw, yaxis_kw, **kwargs):
#    ""
#    Formats a set of multiple plots
#
#    **Arguments:**
#        :*subplots*: OrderedDict of <Axes> on which at act
#        :*first*:    Index of first plot in multiple
#        :*nrows*:    Number of rows of plots in multiple
#        :*ncols*:    Number of columns of plots in multiple
#        :*xaxis_kw*:  Keyword arguments to be passed to set_xaxis
#        :*yaxis_kw*:  Keyword arguments to be passed to set_yaxis
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
#def set_colorbar(cbar, ticks, ticklabels = None, label = "", label_fp = "11b",
#      tick_fp = "8r", **kwargs):
#    """
#    Formats a colorbar
#
#    **Arguments:**
#        :*cbar*:       <ColorBar> to act on
#        :*ticks*:      Ticks
#        :*ticklabels*: Tick labels
#        :*tick_fp*:    Tick label font; passed to get_font(...)
#        :*label*:      Label text
#        :*label_fp*:   Label font; passed to get_font(...)
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
