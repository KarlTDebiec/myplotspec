# -*- coding: utf-8 -*-
#   myplotspec.axes.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
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
def set_xaxis(subplot, **kwargs):
    """
    Formats the x axis of a subplot using provided keyword arguments.

    Arguments:
      subplot (Axes): Axes to format
      [x]ticks (list, ndarray): Ticks; first and last are used as upper
        and lower boundaries
      [x]tick_kw (dict): Keyword arguments passed to
        subplot.set_xticks()
      [x]ticklabels (list): Tick label text
      [x]tick[label]_fp (str, dict, FontProperties): Tick label
        font
      [x]ticklabel_kw (dict): Keyword arguments passed to
        subplot.set_xticklabels()
      [x]label (str): Label text
      [x]label_fp (str, dict, FontProperties): Label font
      [x]label_kw (dict): Keyword arguments passed to
        subplot.set_xlabel()
      [x]tick_params (dict): Keyword arguments passed to
        subplot.tick_params(); only affect x axis
      [x]lw (float): Subplot top and bottom line width
      kwargs (dict): Additional keyword arguments
    """
    from . import (FP_KEYS, get_colors, get_font, multi_get_copy, multi_pop)

    # Ticks
    xbound = multi_get_copy(["xbound", "bound"], kwargs)
    xtick_kw = multi_get_copy(["xtick_kw", "tick_kw"], kwargs, {})
    xticks = multi_get_copy(["xticks", "ticks"], kwargs)
    xticks_2 = multi_pop(["xticks", "ticks"], xtick_kw)
    if xticks_2 is not None:
        xticks = xticks_2
    elif xticks is None:
        xticks = subplot.get_xticks()
    if xbound is not None:
        subplot.set_xbound(float(xbound[0]), float(xbound[1]))
    elif xticks != []:
        subplot.set_xbound(float(xticks[0]), float(xticks[-1]))
    subplot.set_xticks(xticks, **xtick_kw)

    # Tick labels
    xticklabel_kw = multi_get_copy(["xticklabel_kw", "ticklabel_kw"],kwargs,{})
    xticklabels = multi_get_copy(["xticklabels", "ticklabels"], kwargs)
    xticklabels_2 = multi_pop(["xticklabels", "ticklabels"], xticklabel_kw)
    if xticklabels_2 is not None:
        xticklabels = xticklabels_2
    elif xticklabels is None:
        xticklabels = xticks
    xticklabel_fp = multi_get_copy(["xtick_fp", "tick_fp", "xticklabel_fp",
      "ticklabel_fp"] + FP_KEYS, kwargs)
    xticklabel_fp_2 = multi_pop(["xtick_fp", "tick_fp", "xticklabel_fp",
      "ticklabel_fp"] + FP_KEYS, xticklabel_kw)
    if xticklabel_fp_2 is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp_2)
    elif xticklabel_fp is not None:
        xticklabel_kw["fontproperties"] = get_font(xticklabel_fp)
    subplot.set_xticklabels(xticklabels, **xticklabel_kw)

    # Label
    xlabel_kw = multi_get_copy(["xlabel_kw", "label_kw"], kwargs, {})
    xlabel = multi_pop(["xlabel", "label"], kwargs)
    xlabel_2 = multi_pop(["xlabel", "label"], xlabel_kw)
    if xlabel_2 is not None:
        xlabel = xlabel_2
    xlabel_fp = multi_get_copy(["xlabel_fp", "label_fp"] + FP_KEYS, kwargs)
    xlabel_fp_2 = multi_pop(["xlabel_fp", "label_fp"] + FP_KEYS, xlabel_kw)
    if xlabel_fp_2 is not None:
        xlabel_kw["fontproperties"] = get_font(xlabel_fp_2)
    elif xlabel_fp is not None:
        xlabel_kw["fontproperties"] = get_font(xlabel_fp)
    if xlabel is not None:
        get_colors(xlabel_kw)
        subplot.set_xlabel(xlabel, **xlabel_kw)

    # Tick parameters
    xtick_params = multi_get_copy(["xtick_params", "tick_params"], kwargs, {})
    if xtick_params is not None:
        xtick_params["axis"] = "x"
        subplot.tick_params(**xtick_params)

    # Line width
    xlw = multi_get_copy(["xlw", "lw"], kwargs)
    if xlw is not None:
        subplot.spines["top"].set_lw(xlw)
        subplot.spines["bottom"].set_lw(xlw)
    subplot.spines["top"].set_zorder(100)
    subplot.spines["bottom"].set_zorder(100)

def set_yaxis(subplot, **kwargs):
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
    from . import (FP_KEYS, get_colors, get_font, multi_get_copy, multi_pop)

    # Ticks
    ybound = multi_get_copy(["ybound", "bound"], kwargs)
    ytick_kw = multi_get_copy(["ytick_kw", "tick_kw"], kwargs, {})
    yticks = multi_get_copy(["yticks", "ticks"], kwargs)
    yticks_2 = multi_pop(["yticks", "ticks"], ytick_kw)
    if yticks_2 is not None:
        yticks = yticks_2
    elif yticks is None:
        yticks = subplot.get_yticks()
    if ybound is not None:
        subplot.set_ybound(float(ybound[0]), float(ybound[1]))
    elif yticks != []:
        subplot.set_ybound(float(yticks[0]), float(yticks[-1]))
    subplot.set_yticks(yticks, **ytick_kw)

    # Tick labels
    yticklabel_kw = multi_get_copy(["yticklabel_kw", "ticklabel_kw"],kwargs,{})
    yticklabels = multi_get_copy(["yticklabels", "ticklabels"], kwargs)
    yticklabels_2 = multi_pop(["yticklabels", "ticklabels"], yticklabel_kw)
    if yticklabels_2 is not None:
        yticklabels = yticklabels_2
    elif yticklabels is None:
        yticklabels = yticks
    yticklabel_fp = multi_get_copy(["ytick_fp", "tick_fp", "yticklabel_fp",
      "ticklabel_fp"] + FP_KEYS, kwargs)
    yticklabel_fp_2 = multi_pop(["ytick_fp", "tick_fp", "yticklabel_fp",
      "ticklabel_fp"] + FP_KEYS, yticklabel_kw)
    if yticklabel_fp_2 is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp_2)
    elif yticklabel_fp is not None:
        yticklabel_kw["fontproperties"] = get_font(yticklabel_fp)
    subplot.set_yticklabels(yticklabels, **yticklabel_kw)

    # Label
    ylabel_kw = multi_get_copy(["ylabel_kw", "label_kw"], kwargs, {})
    ylabel = multi_pop(["ylabel", "label"], kwargs)
    ylabel_2 = multi_pop(["ylabel", "label"], ylabel_kw)
    if ylabel_2 is not None:
        ylabel = ylabel_2
    ylabel_fp = multi_get_copy(["ylabel_fp", "label_fp"] + FP_KEYS, kwargs)
    ylabel_fp_2 = multi_pop(["ylabel_fp", "label_fp"] + FP_KEYS, ylabel_kw)
    if ylabel_fp_2 is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp_2)
    elif ylabel_fp is not None:
        ylabel_kw["fontproperties"] = get_font(ylabel_fp)
    if ylabel is not None:
        get_colors(ylabel_kw)
        subplot.set_ylabel(ylabel, **ylabel_kw)

    # Tick parameters
    ytick_params = multi_get_copy(["ytick_params", "tick_params"], kwargs, {})
    if ytick_params is not None:
        ytick_params["axis"] = "y"
        subplot.tick_params(**ytick_params)

    # Line width
    ylw = multi_get_copy(["ylw", "lw"], kwargs)
    if ylw is not None:
        subplot.spines["left"].set_lw(ylw)
        subplot.spines["right"].set_lw(ylw)
    subplot.spines["left"].set_zorder(100)
    subplot.spines["right"].set_zorder(100)

    # For Y2 axis, check all keyword arguments first, if any are
    # provided, add y2 axis if not already present

    # Y2 ticks
    y2tick_kw = multi_get_copy("y2tick_kw", kwargs, {})
    y2ticks = multi_get_copy("y2ticks", kwargs)
    y2ticks_2 = multi_pop(["y2ticks", "yticks", "ticks"], y2tick_kw)
    if y2ticks_2 is not None:
        y2ticks = y2ticks_2
    elif yticks is None and hasattr(subplot, "_mps_y2"):
        y2ticks = subplot._mps_y2.get_yticks()

    # Y2 tick labels
    y2ticklabel_kw = multi_get_copy("y2ticklabel_kw", kwargs, {})
    y2ticklabels = multi_get_copy("y2ticklabels", kwargs)
    y2ticklabels_2 = multi_pop(["y2ticklabels", "yticklabels",
      "ticklabels"], y2ticklabel_kw)
    if y2ticklabels_2 is not None:
        y2ticklabels = y2ticklabels_2
    if y2ticklabels is None and y2ticks is not None:
        y2ticklabels = y2ticks

    # Y2 label
    y2label_kw = multi_get_copy("y2label_kw", kwargs, {})
    y2label = multi_pop("y2label", kwargs)
    y2label_2 = multi_pop(["y2label", "ylabel", "label"], ylabel_kw)
    if y2label_2 is not None:
        y2label = y2label_2

    # Y2 tick parameters
    y2tick_params = multi_get_copy("y2tick_params", kwargs, {})
    if y2tick_params is not None:
        y2tick_params["axis"] = "y"

    # Now check if Y2 settings have been specified
    if y2ticks is not None or y2ticklabels is not None or y2label is not None:
        if not hasattr(subplot, "_mps_y2"):
            subplot._mps_y2 = subplot.twinx()
            if y2ticks is None:
                y2ticks = subplot._mps_y2.get_yticks()
            if y2ticklabels is None:
                y2ticklabels = y2ticks
        subplot._mps_y2.set_zorder(subplot.get_zorder() - 1)

        # Set ticks, ticklabels, and label
        if y2ticks is not None:
            if y2ticks != []:
                subplot._mps_y2.set_ybound(float(y2ticks[0]),
                  float(y2ticks[-1]))
            subplot._mps_y2.set_yticks(y2ticks, **y2tick_kw)
        if y2ticklabels is not None:
            y2ticklabel_fp = multi_get_copy(["y2tick_fp", "tick_fp",
              "y2ticklabel_fp", "ticklabel_fp"] + FP_KEYS, kwargs)
            y2ticklabel_fp_2 = multi_pop(["y2tick_fp", "tick_fp",
              "y2ticklabel_fp", "ticklabel_fp"] + FP_KEYS, y2ticklabel_kw)
            if y2ticklabel_fp_2 is not None:
                y2ticklabel_kw["fontproperties"] = get_font(y2ticklabel_fp_2)
            elif y2ticklabel_fp is not None:
                y2ticklabel_kw["fontproperties"] = get_font(y2ticklabel_fp)
            subplot._mps_y2.set_yticklabels(y2ticklabels, **y2ticklabel_kw)
        if y2label is not None:
            y2label_fp = multi_get_copy(["y2label_fp", "label_fp"] + FP_KEYS,
              kwargs)
            y2label_fp_2 = multi_pop(["y2label_fp", "ylabel_fp", "label_fp"] 
              + FP_KEYS, ylabel_kw)
            if y2label_fp_2 is not None:
                y2label_kw["fontproperties"] = get_font(y2label_fp_2)
            elif ylabel_fp is not None:
                y2label_kw["fontproperties"] = get_font(y2label_fp)
            get_colors(y2label_kw)
            subplot._mps_y2.set_ylabel(y2label, **y2label_kw)

        # Set tick parameters, must reset Y1 tick parameters,
        #   Nobody knows why
        if y2tick_params is not None:
            subplot._mps_y2.tick_params(**y2tick_params)
        if ytick_params is not None:
            subplot.tick_params(**ytick_params)

        # Set zorder
        subplot._mps_y2.spines["left"].set_zorder(100)
        subplot._mps_y2.spines["right"].set_zorder(100)


def add_partner_subplot(subplot, figure, subplots, verbose=1, debug=0,
    **kwargs):
    """
    Adds a subplot to the side 

    Typically used for colorbars.

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
      - implement 'left'
      - store position somewhere (e.g. _position) so that later functions don't
        need their own position argument
      - Error text
    """
    from copy import copy
    from matplotlib import rcParams
    import numpy as np
    from . import get_figure_subplots, multi_get_copy

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
    for k in [k for k, v in partner_kw.items() if v is None]:
        del(partner_kw[k])

    if position == "top":
        partner_kw["left"] = partner_kw.get("left", host_left)
        partner_kw["right"] = partner_kw.get("right", host_right)
        partner_kw["hspace"] = partner_kw.pop("hspace", 0.05)
        partner_kw["sub_height"] = partner_kw.get("sub_height", 0.1)
        partner_kw["bottom"] = partner_kw.get("bottom",
          host_bottom + host_height + partner_kw["hspace"])
        partner_kw["top"] = partner_kw.get("top",
          host_top - partner_kw["hspace"] - partner_kw["sub_height"])

    elif position == "bottom":
        if "sub_width" in partner_kw:
            if "right" not in partner_kw and "left" not in partner_kw:
                partner_kw["left"] = (host_left
                  + (host_width - partner_kw["sub_width"]) / 2)
                partner_kw["right"] = (host_right
                  - (host_width - partner_kw["sub_width"]) / 2)
        else:
            if "left" not in partner_kw and "right" not in partner_kw:
                partner_kw["left"]  = host_left
                partner_kw["right"] = host_right
            elif "left" in partner_kw:
                if partner_kw["left"] < host_right:
                    partner_kw["right"] = host_right
                else:
                    partner_kw["sub_width"] = host_width
            elif "right" in partner_kw:
                if partner_kw["right"] < host_right:
                    partner_kw["left"] = host_left
                else:
                    partner_kw["left"] = partner_kw["right"] - host_width
        if "hspace" not in partner_kw:
            partner_kw["hspace"] = rcParams["figure.subplot.hspace"]
        if "sub_height" in partner_kw:
            if "bottom" not in partner_kw and "top" not in partner_kw:
                partner_kw["bottom"] = \
                  (host_bottom + host_height - partner_kw["hspace"])
        else:
            if "bottom" not in partner_kw and "top" not in partner_kw:
                partner_kw["top"] = host_bottom - partner_kw["hspace"]
                partner_kw["sub_height"] = host_height * 0.1
            elif "bottom" in partner_kw:
                partner_kw["sub_height"] = host_height * 0.1
            elif "top" in partner_kw:
                partner_kw["sub_height"] = host_height * 0.1

    elif position == "right":
        if "sub_height" in partner_kw:
            if "bottom" not in partner_kw and "top" not in partner_kw:
                partner_kw["bottom"] = (host_bottom
                  + (host_height - partner_kw["sub_height"]) / 2)
                partner_kw["top"] = (host_top
                  - (host_height - partner_kw["sub_height"]) / 2)
        else:
            if "bottom" not in partner_kw and "top" not in partner_kw:
                partner_kw["bottom"] = host_bottom
                partner_kw["top"]    = host_top
            elif "bottom" in partner_kw:
                if partner_kw["bottom"] < host_top:
                    partner_kw["top"] = host_top
                else:
                    partner_kw["sub_height"] = host_height
            elif "top" in partner_kw:
                if partner_kw["top"] < host_top:
                    partner_kw["bottom"] = host_bottom
                else:
                    partner_kw["bottom"] = partner_kw["top"] - host_height
        if "wspace" not in partner_kw:
            partner_kw["wspace"] = rcParams["figure.subplot.wspace"]
        if "sub_width" in partner_kw:
            if "right" not in partner_kw and "left" not in partner_kw:
                partner_kw["left"] = \
                  (host_left + host_width + partner_kw["hspace"])
        else:
            if "left" not in partner_kw and "right" not in partner_kw:
                partner_kw["left"] = host_right + partner_kw["wspace"]
                partner_kw["sub_width"] = host_width * 0.1
            elif "left" in partner_kw:
                partner_kw["sub_width"] = host_width * 0.1
            elif "right" in partner_kw:
                partner_kw["sub_width"] = host_width * 0.1

    else:
        raise()

    get_figure_subplots(figure=figure, subplots=subplots, **partner_kw)
    partner = subplots[list(subplots)[-1]]
    set_xaxis(partner, **partner_kw)
    set_yaxis(partner, **partner_kw)
    if partner_kw.get("grid", False):
        grid_kw = multi_get_copy("grid_kw", partner_kw, {})
        partner.grid(**grid_kw)
    partner._mps_position = position
    partner.set_autoscale_on(False)

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
    import numpy as np
    from . import FP_KEYS, get_font, multi_kw

    colorbar_kw = kwargs.get("colorbar_kw", {})
    if "position" in colorbar_kw:
        position = colorbar_kw.get("position")
    elif hasattr(subplot._mps_partner_subplot, "_mps_position"):
        position = subplot._mps_partner_subplot._mps_position
    else:
        position = "right"

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
    lw = multi_kw(["zlw", "clw", "lw"], colorbar_kw, 1.0)
    if ticks_2 is not None:
        ticks = ticks_2
    if ticks is not None:
        subplot._mps_colorbar.set_ticks(ticks)
        if position in ["left", "right"]:
            for tick in ticks:
                tick_y = ((tick - subplot._mps_colorbar.vmin) /
                  (subplot._mps_colorbar.vmax - subplot._mps_colorbar.vmin))
                subplot._mps_partner_subplot.axhline(y=tick_y, lw=lw,
                  color="k")
        if position == "top":
            subplot._mps_partner_subplot.xaxis.tick_top()
        if position in ["top", "bottom"]:
            for tick in ticks:
                tick_x = ((tick - subplot._mps_colorbar.vmin) /
                  (subplot._mps_colorbar.vmax - subplot._mps_colorbar.vmin))
                subplot._mps_partner_subplot.axvline(x=tick_x, lw=lw,
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
    label_kw = multi_kw(["zlabel_kw", "clabel_kw", "label_kw", ], colorbar_kw,
                 {})
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

    # Line width
    if lw is not None:
        subplot._mps_colorbar.outline.set_lw(lw)
        outline_path = subplot._mps_colorbar.outline.get_path()
        outline_path.vertices = np.append(outline_path.vertices,
          [[0.0, 0.00390625]], axis=0)
        outline_path.codes = np.array(np.append(outline_path.codes[:-1],
          [2, 2]), dtype=np.uint8)
