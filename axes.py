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
        subplot.tick_params(); only affect x axis
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
        subplot.tick_params(); only affect y axis
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
            subplot_y2 = subplot._mps_y2 = subplot.twinx()
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

def add_partner_subplot(subplot, figure, subplots, verbose=1, debug=0,
    **kwargs):
    """
    Adds a subplot to the side 

    Typically used for colorbars

    Arguments:
      subplot (Axes): Host subplot to which partner will be added
      figure (Figure): Figure on which subplot and partner are located
      subplots (OrderedDict): subplots
      partner_kw (dict): Keyword arguments passed to
        :func:`get_figure_subplots` to add partner subplot; 'position'
        key is used to control position relative to host subplot
      verbose (int): Level of verbose output
      debug (int): Level of debug output

    Returns:
      partner (Axes): Parter subplot

    .. todo:
      - implement 'left' and 'bottom'
    """
    from copy import copy
    import numpy as np
    from . import get_figure_subplots

    # Get figure and host subplot dimensions in inches
    fig_size = np.array(figure.get_size_inches())
    fig_width, fig_height = fig_size
    host_width, host_height = np.array(subplot.get_position().size) * fig_size
    host_left, host_bottom = np.array(subplot.get_position().min) * fig_size
    host_right, host_top = (fig_size - np.array(subplot.get_position().max)
      * fig_size)

    # Determine partner dimensions in inches
    partner_kw = copy(kwargs.get("partner_kw", {}))
    position = partner_kw.get("position", "right")
    if position == "top":
        partner_kw["left"] = partner_kw.get("left", host_left)
        partner_kw["right"] = partner_kw.get("right", host_right)
        partner_kw["hspace"] = partner_kw.pop("hspace", 0.05)
        partner_kw["sub_height"] = partner_kw.get("sub_height", 0.1)
        partner_kw["bottom"] = partner_kw.get("bottom",
          host_bottom + host_height + partner_kw["hspace"])
        partner_kw["top"] = partner_kw.get("top",
          host_top - partner_kw["hspace"] - partner_kw["sub_height"])
    elif position == "right":
        partner_kw["bottom"] = partner_kw.get("bottom", host_bottom)
        partner_kw["top"] = partner_kw.get("top", host_top)
        partner_kw["wspace"] = partner_kw.pop("wspace", 0.1)
        partner_kw["sub_width"] = partner_kw.get("sub_width", 0.1)
        partner_kw["left"] = partner_kw.get("left",
          host_left + host_width + partner_kw["wspace"])
        partner_kw["right"] = partner_kw.get("right",
          host_right - partner_kw["wspace"] - partner_kw["sub_width"])
    else:
        raise
    get_figure_subplots(figure=figure, subplots=subplots, **partner_kw)
    partner = subplots[subplots.keys()[-1]]

    subplot._mps_partner_subplot = partner
    return partner

def set_colorbar(subplot, mappable, **kwargs):
    """
    Configures a colorbar.

    Arguments:
      subplot (Axes): axes on which 
      mappable (?): Object used to generate colorbar; typically returned
        by matplotlib's imshow or pcolormesh
      colorbar_kw (dict): Keyword arguments used to configure colorbar;
        'position' key is used to control orientation
      [z|c]ticks (list or ndarray): Ticks; first and last are used as
        upper and lower boundaries
      [z|c]tick_kw (dict): Keyword arguments passed to
        subplot.set_ticks
      [z|c]ticklabels (list): Tick label text
      [z|c]tick[label]_fp (str, dict, FontProperties): Tick label
        font
      [z|c]ticklabel_kw (dict): Keyword arguments passed to
        subplot.set_[x|y]ticklabels()
      [z|c]label (str): Label text
      [z|c]label_fp (str, dict, FontProperties): Label font
      zlabel_kw (dict): Keyword arguments passed to subplot.set_label
      [z|c]tick_params (dict): Keyword arguments passed to
        subplot.tick_params()
      kwargs (dict): Additional keyword arguments
    """
    from matplotlib.pyplot import colorbar
    from . import FP_KEYS, get_font, multi_kw

    colorbar_kw = kwargs.get("colorbar_kw", {})
    position = colorbar_kw.get("position", "right")

    orientation = colorbar_kw.get("orientation", "vertical"
      if position in ["left", "right"] else "horizontal")
    subplot._mps_colorbar = colorbar(mappable,
      cax=subplot._mps_partner_subplot, orientation=orientation)
    if position == "top":
        subplot._mps_partner_subplot.xaxis.set_label_position("top")

    # Ticks
    tick_kw = multi_kw(["ztick_kw", "ctick_kw", "tick_kw"], colorbar_kw, {})
    ticks = multi_kw(["zticks", "cticks", "ticks"], colorbar_kw)
    ticks_2 = multi_kw(["zticks", "cticks", "ticks"], tick_kw)
    if ticks_2 is not None:
        ticks = ticks_2
    if ticks is not None:
        subplot._mps_colorbar.set_ticks(ticks)
        if position in ["left", "right"]:
            for tick in ticks:
                tick_y = ((tick - subplot._mps_colorbar.vmin) /
                  (subplot._mps_colorbar.vmax - subplot._mps_colorbar.vmin))
                subplot._mps_partner_subplot.axhline(y=tick_y, lw=0.5,
                  color="k")
        if position == "top":
            subplot._mps_partner_subplot.xaxis.tick_top()
            for tick in ticks:
                tick_x = ((tick - subplot._mps_colorbar.vmin) /
                  (subplot._mps_colorbar.vmax - subplot._mps_colorbar.vmin))
                subplot._mps_partner_subplot.axvline(x=tick_x, lw=0.5,
                  color="k")

    # Tick labels
    ticklabel_kw = multi_kw(
      ["zticklabel_kw", "cticklabel_kw", "ticklabel_kw"], colorbar_kw, {})
    ticklabels = multi_kw(["zticklabels", "cticklabels", "ticklabels"],
      colorbar_kw)
    ticklabels_2 = multi_kw(["zticklabels", "cticklabels", "ticklabels"],
      ticklabel_kw)
    if ticklabels_2 is not None:
        ticklabels = ticklabels_2
    elif ticklabels is None and ticks is not None:
        ticklabels = ticks

    ticklabel_fp = multi_kw(["ztick_fp", "ctick_fp", "tick_fp",
      "zticklabel_fp", "cticklabel_fp", "ticklabel_fp"] + FP_KEYS, colorbar_kw)
    ticklabel_fp_2 = multi_kw(["ztick_fp", "ctick_fp", "tick_fp",
      "zticklabel_fp", "cticklabel_fp", "ticklabel_fp"] + FP_KEYS,
      ticklabel_kw)
    if ticklabel_fp_2 is not None:
        ticklabel_kw["fontproperties"] = get_font(ticklabel_fp_2)
    elif ticklabel_fp is not None:
        ticklabel_kw["fontproperties"] = get_font(ticklabel_fp)
    if ticklabels is not None:
        if position in ["left", "right"]:
            subplot._mps_colorbar.ax.set_yticklabels(ticklabels,
              **ticklabel_kw)
        else:
            subplot._mps_colorbar.ax.set_xticklabels(ticklabels,
              **ticklabel_kw)

    # Label
    label_kw = multi_kw(["zlabel_kw", "clabel_kw"], colorbar_kw, {})
    label = multi_kw(["zlabel", "clabel", "label"], colorbar_kw)
    label_2 = multi_kw(["zlabel", "clabel", "label"], label_kw)
    if label_2 is not None:
        label = label_2

    label_fp = multi_kw(["zlabel_fp", "clabel_fp", "label_fp"] + FP_KEYS,
      colorbar_kw)
    label_fp_2 = multi_kw(["zlabel_fp", "clabel_fp", "label_fp"] + FP_KEYS,
      label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif label_fp is not None:
        label_kw["fontproperties"] = get_font(label_fp)
    if label is not None:
        subplot._mps_colorbar.set_label(label, **label_kw)

    # Tick parameters
    tick_params = multi_kw(["ztick_params", "ctick_params", "tick_params"],
      colorbar_kw)
    if tick_params is not None:
        subplot._mps_partner_subplot.tick_params(**tick_params)
