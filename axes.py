#!/usr/bin/python
#   plot_toolkit.axes.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec 14-11-01
"""
Functions for formatting axes

.. todo:
    - Finish formatting for 80 column
    - Figure out how to adjust the positions of specific ticks properly
      and automatically ('1' often looks bad)
"""
################################### MODULES ####################################
from __future__ import division, print_function
import os, sys
import numpy as np
from . import gen_font
from .text import set_bigxlabel, set_bigylabel
################################## FUNCTIONS ###################################
def set_xaxis(subplot, xkwargs = {}, **kwargs):
    """
    Formats the x-axis of a subplot using provided keyword arguments

    Arguments are pulled from three sources. Highest priority is given
    to keyword arguments included in the dictionary *xkwargs* (e.g.
    set_xaxis(subplot, xkwargs = {"label": "X Axis"})). Lower priority
    is given to keyword arguments passed directly to this function, and
    preprended with 'x' (e.g. set_xaxis(subplot, xlabel = "X Axis")).
    These will not overwrite keyword arguments already present in
    *xkwargs*. Lowest priority is given to keyword arguments passed
    directly to this function that are not prepended with either 'x' or
    'y' (e.g. set_xaxis(subplot, label = "X Axis")). These will not
    overwrite keyword arguments from either of the previous sources.

    **Arguments:**
        :*subplot*:         <Axes> on which to act
        :*xkwargs*:         Keyword arguments for x axis; may include
                            any listed below
        :*(x)ticks*:        Ticks; first and last are used as upper and
                            lower boundaries
        :*(x)tick_kw*:      Keyword arguments to be passed to
                            set_xticks(...)
        :*(x)ticklabels*:   Tick labels
        :*(x)tick_fp*:      Tick label font properties; passed to
                            gen_font(...)
        :*(x)ticklabel_kw*: Keyword arguments to be passed to
                            set_xticklabels(...)
        :*(x)tick_params*:  Keyword arguments to be passed to
                            set_tick_params(...); will only affect
                            x axis
        :*(x)label*:        Label text
        :*(x)label_fp*:     Label font properties; passed to
                            gen_font(...)
        :*(x)label_kw*:     Keyword arguments to be passed to
                            set_xlabel(...)
        :*(x)lw*:           Width of x-axis lines
    """
    for xkey in [key for key in kwargs if key.startswith("x")]:
        xvalue = kwargs.pop(xkey)
        if not xkey in xkwargs:
            xkwargs[xkey[1:]] = xvalue
    for key in [key for key in kwargs if not key.startswith("y")]:
        value = kwargs.pop(key)
        if not key in xkwargs: 
            xkwargs[key] = value
    if "tick_params" in xkwargs:
        xkwargs["tick_params"].update(dict(axis = "x"))

    subplot.spines["top"].set_lw(xkwargs.get("lw", 1))
    subplot.spines["bottom"].set_lw(xkwargs.get("lw", 1))
    _set_axes(subplot.set_xlabel, subplot.set_xbound, subplot.set_xticks,
      subplot.set_xticklabels, subplot.tick_params,
      subplot.get_xaxis().get_major_ticks, **xkwargs)

def set_yaxis(subplot, ykwargs = {}, y2kwargs = {}, **kwargs):
    """
    Formats the y-axis of a subplot using provided keyword arguments

    Arguments are pulled from three sources. Highest priority is given
    to keyword arguments included in the dictionary *ykwargs* (e.g.
    set_yaxis(subplot, ykwargs = {"label": "Y Axis"})). Lower priority
    is given to keyword arguments passed directly to this function, and
    preprended with 'y' (e.g. set_yaxis(subplot, ylabel = "Y Axis")).
    These will not overwrite keyword arguments already present in
    *ykwargs*. Lowest priority is given to keyword arguments passed
    directly to this function that are not prepended with either 'x' or
    'y' (e.g. set_yaxis(subplot, label = "Y Axis")). These will not
    overwrite keyword arguments from either of the previous sources.

    Arguments may additionally be provided for the secondary y axis,
    analagously using y2kwargs and keyword arguments passed directly
    to this function prepended with 'y2'. Other keyword arguments will
    not be applied to the secondary y axis. If no keywords are provided
    for the secondary y axis, none will be created.

    **Arguments:**
        :*subplot*:         <Axes> on which to act
        :*ykwargs*:         Keyword arguments for y axis; may include
                            any listed below
        :*y2kwargs*:        Keyword arguments for second y axisl may
                            include any listed below
        :*(y)ticks*:        Ticks; first and last are used as upper and
                            lower boundaries
        :*(y)tick_kw*:      Keyword arguments to be passed to
                            set_yticks(...)
        :*(y)ticklabels*:   Tick labels
        :*(y)tick_fp*:      Tick label font properties; passed to
                            gen_font(...)
        :*(y)ticklabel_kw*: Keyword arguments to be passed to
                            set_yticklabels(...)
        :*(y)tick_params*:  Keyword arguments to be passed to
                            set_tick_params(...); will only affect
                            y axis
        :*(y)tick_right*:   Place ticks, ticklabels, and label on right
                            side
        :*(y)label*:        Label text
        :*(y)label_fp*:     Label font properties; passed to
                            gen_font(...)
        :*(y)label_kw*:     Keyword arguments to be passed to
                            set_ylabel(...)
        :*(y)lw*:           Width of y-axis lines
    """
    for y2key in [key for key in kwargs if key.startswith("y2")]:
        y2value = kwargs.pop(y2key)
        if not y2key in y2kwargs:
            y2kwargs[y2key[2:]] = y2value
    for ykey in [key for key in kwargs if key.startswith("y")]:
        yvalue = kwargs.pop(ykey)
        if not ykey in ykwargs:
            ykwargs[ykey[1:]] = yvalue
    for key in [key for key in kwargs if not key.startswith("x")]:
        value = kwargs.pop(key)
        if not key in ykwargs:
            ykwargs[key] = value
    if "tick_params" in ykwargs:
        ykwargs["tick_params"].update(dict(axis = "y"))
    if "tick_params" in y2kwargs:
        y2kwargs["tick_params"].update(dict(axis = "y"))

    if ykwargs.pop("tick_right", False):
        subplot.yaxis.tick_right()

    subplot.spines["left"].set_lw(ykwargs.get("lw", 1))
    subplot.spines["right"].set_lw(ykwargs.get("lw", 1))
    _set_axes(subplot.set_ylabel, subplot.set_ybound, subplot.set_yticks,
      subplot.set_yticklabels, subplot.tick_params,
      subplot.get_yaxis().get_major_ticks, **ykwargs)

    if y2kwargs != {} and not "disabled" in y2kwargs:
        subplot_y2 = subplot.twinx()
        subplot_y2.set_autoscale_on(False)
        _set_axes(subplot_y2.set_ylabel, subplot_y2.set_ybound,
          subplot_y2.set_yticks, subplot_y2.set_yticklabels,
          subplot_y2.tick_params, subplot_y2.get_major_ticks, **y2kwargs)

def set_multi(subplots, first, nrows, ncols, xkwargs, ykwargs, **kwargs):
    """
    Formats a set of multiple plots

    **Arguments:**
        :*subplots*: OrderedDict of <Axes> on which at act
        :*first*:    Index of first plot in multiple
        :*nrows*:    Number of rows of plots in multiple
        :*ncols*:    Number of columns of plots in multiple
        :*xkwargs*:  Keyword arguments to be passed to set_xaxis
        :*ykwargs*:  Keyword arguments to be passed to set_yaxis

    .. todo:
        - Smooth passage of keyword arguments from x/ykwargs and kwargs
          to set_bigx/ylabel
    """
    xticks      = xkwargs.pop("ticks")
    xticklabels = xkwargs.pop("ticklabels", xticks)

    xlabel_kw   = dict(xlabel = xkwargs.pop("label", kwargs.pop("xlabel", "")))
    for kw in ["label_fp", "bottom", "top"]:
        if kw in  kwargs: xlabel_kw[kw] =  kwargs.get(kw)
    for kw in ["label_fp", "bottom", "top", "x", "y", "ha", "va", "rotation"]:
        if kw in xkwargs: xlabel_kw[kw] = xkwargs.pop(kw)
    if "xlabel_kw" in xkwargs: xlabel_kw.update(xkwargs.pop("xlabel_kw"))

    yticks      = ykwargs.pop("ticks")
    yticklabels = ykwargs.pop("ticklabels", yticks)

    ylabel_kw   = dict(ylabel = ykwargs.pop("label", kwargs.pop("ylabel", "")))
    for kw in ["label_fp", "left", "right"]:
        if kw in  kwargs: ylabel_kw[kw] =  kwargs.get(kw)
    for kw in ["label_fp", "left", "right", "x", "y", "ha", "va", "rotation"]:
        if kw in ykwargs: ylabel_kw[kw] = ykwargs.pop(kw)
    if "ylabel_kw" in ykwargs: ylabel_kw.update(ykwargs.pop("ylabel_kw"))

    xkwargs.update(kwargs)
    ykwargs.update(kwargs)

    # Loop over subplots
    for i in range(first, first + (nrows * ncols), 1):

        # Format x axes
        if   (i == first + (nrows * ncols) - 1):
            set_xaxis(subplots[i], ticks = xticks, ticklabels = xticklabels,      **xkwargs)
        elif (i in range(first + ((nrows - 1) * ncols), first + (nrows * ncols) - 1, 1)):
            set_xaxis(subplots[i], ticks = xticks, ticklabels = xticklabels[:-1], **xkwargs)
        else:
            set_xaxis(subplots[i], ticks = xticks, ticklabels = [],               **xkwargs)

        # Format y axes
        if   (i == first):
            set_yaxis(subplots[i], ticks = yticks, ticklabels = yticklabels,      **ykwargs)
        elif (i in range(first + nrows, first + (nrows * ncols), nrows)):
            set_yaxis(subplots[i], ticks = yticks, ticklabels = yticklabels[:-1], **ykwargs)
        else:
            set_yaxis(subplots[i], ticks = yticks, ticklabels = [],               **ykwargs)
    set_bigxlabel(dict((j, subplots[j]) for j in range(first, first + (nrows * ncols), 1)), **xlabel_kw)
    set_bigylabel(dict((j, subplots[j]) for j in range(first, first + (nrows * ncols), 1)), **ylabel_kw)

def set_colorbar(cbar, ticks, ticklabels = None, label = "", label_fp = "11b",
      tick_fp = "8r", **kwargs):
    """
    Formats a colorbar

    **Arguments:**
        :*cbar*:       <ColorBar> to act on
        :*ticks*:      Ticks
        :*ticklabels*: Tick labels
        :*tick_fp*:    Tick label font; passed to gen_font(...)
        :*label*:      Label text
        :*label_fp*:   Label font; passed to gen_font(...)
    """
    import warnings

    if ticklabels is None:
        ticklabels = ticks
    zticks  = np.array(ticks, np.float32)
    zticks  = (zticks - zticks[0]) / (zticks[-1] - zticks[0])
    cbar.ax.tick_params(bottom = "off", top = "off", left = "off",
      right = "off")
    cbar.set_ticks(ticks)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [])
        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticklabels,
          tick_fp = tick_fp)
    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
    cbar.set_label(label, fontproperties = gen_font(label_fp))

############################## INTERNAL FUNCTIONS ##############################
def _set_axes(set_label, set_bound, set_ticks, set_ticklabels, set_tick_params,
    get_major_ticks, ticks, ticklabels = None, tick_fp = "8r", label = "",
    label_fp = "10b", tick_pad = 8, **kwargs):
    """
    Formats an axis

    **Arguments:**
        :*set_label*:       Function to set axis label
        :*set_bound*:       Function to set axis boundaries
        :*set_ticks*:       Function to set axis ticks
        :*set_ticklabels*:  Function to set axis ticklabels
        :*set_tick_params*: Function to set axis tick parameters
        :*ticks*:           Ticks
        :*tick_kw*:         Keyword arguments to be passed to
                            set_ticks(...)
        :*ticklabels*:      Tick labels
        :*tick_fp*:         Tick label font properties; passed to
                            gen_font(...)
        :*ticklabel_kw*:    Keyword arguments to be passed to
                            set_ticklabels(...)
        :*tick_params*:     Keyword arguments to be passed to
                            set_tick_params(...)
        :*label*:           Label text
        :*label_fp*:        Label font properties; passed to
                            gen_font(...)
        :*label_kw*:        Keyword arguments to be passed to
                            set_label(...)

    .. todo::
        - Support gridlines
    """
    if ticks != []:
        set_bound(float(ticks[0]), float(ticks[-1]))
    if ticklabels is None:
        ticklabels = ticks
    set_ticks(np.array(ticks, np.float32),
      **kwargs.get("tick_kw", {}))
    set_ticklabels(ticklabels, fontproperties = gen_font(tick_fp),
      **kwargs.get("ticklabel_kw", {}))
    set_label(label, fontproperties = gen_font(label_fp),
      **kwargs.get("label_kw", {}))
    set_tick_params(
      **kwargs.get("tick_params", {}))
    for tick in get_major_ticks():
        tick.set_pad(tick_pad)
