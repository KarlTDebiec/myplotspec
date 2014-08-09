#!/usr/bin/python
#   plot_toolkit.axes.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec 14-06-24
"""
Functions for formatting axes

.. todo:
    - Consider smooth acceptance of kwargs named xticks, xticklabels, etc. instead of forcing ticks, ticklabels
    - Figure out how to adjust the positions of specific ticks properly ('1' often looks bad)
"""
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys
import numpy as np
from . import gen_font
from .text import set_bigxlabel, set_bigylabel
###################################################### FUNCTIONS #######################################################
def set_xaxis(subplot, lw = 1, **kwargs):
    """
    Formats an x-axis

    **Arguments:**
        :*subplot*:      <Axes> on which to act
        :*ticks*:        Ticks
        :*tick_kw*:      Keyword arguments to be passed to set_xticks(...)
        :*ticklabels*:   Tick labels
        :*tick_fp*:      Tick label font; passed to gen_font(...)
        :*ticklabel_kw*: Keyword arguments to be passed to set_xticklabels(...)
        :*tick_params*:  Keyword arguments to be passed to set_tick_params(...)
        :*label*:        Label text
        :*label_fp*:     Label font; passed to gen_font(...)
        :*label_kw*:     Keyword arguments to be passed to set_xlabel(...)
        :*lw*:           Width of x-axis lines
    """
    for xkey in [key for key in kwargs if key.startswith("x")]:
        kwargs[xkey[1:]] = kwargs.pop(xkey)
    kwargs["tick_params"] = dict(kwargs.get("tick_params", {}).items() + dict(axis = "x").items())

    _set_axes(subplot.set_xlabel, subplot.set_xbound, subplot.set_xticks,
      subplot.set_xticklabels, subplot.tick_params, **kwargs)

    subplot.spines["top"].set_lw(lw)
    subplot.spines["bottom"].set_lw(lw)

def set_yaxis(subplot, lw = 1, **kwargs):
    """
    Formats a y-axis

    **Arguments:**
        :*subplot*:      <Axes> on which to act
        :*ticks*:        Ticks
        :*tick_kw*:      Keyword arguments to be passed to set_yticks(...)
        :*ticklabels*:   Tick labels
        :*tick_fp*:      Tick label font; passed to gen_font(...)
        :*ticklabel_kw*: Keyword arguments to be passed to set_yticklabels(...)
        :*tick_params*:  Keyword arguments to be passed to set_tick_params(...)
        :*tick_right*:   Place ticks, ticklabels, and label on right side
        :*label*:        Label text
        :*label_fp*:     Label font; passed to gen_font(...)
        :*label_kw*:     Keyword arguments to be passed to set_ylabel(...)
        :*lw*:           Width of y-axis lines
    """
    for ykey in [key for key in kwargs if key.startswith("y")]:
        kwargs[ykey[1:]] = kwargs.pop(ykey)
    kwargs["tick_params"] = dict(kwargs.get("tick_params", {}).items() + dict(axis = "y").items())
    if kwargs.get("tick_right", False):
        subplot.yaxis.tick_right()

    _set_axes(subplot.set_ylabel, subplot.set_ybound, subplot.set_yticks,
      subplot.set_yticklabels, subplot.tick_params, **kwargs)

    subplot.spines["left"].set_lw(lw)
    subplot.spines["right"].set_lw(lw)

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
        - Smooth passage of keyword arguments from x/ykwargs and kwargs to set_bigx/ylabel
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

def set_colorbar(cbar, ticks, ticklabels = None, label = "", label_fp = "11b", tick_fp = "8r", **kwargs):
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
    cbar.ax.tick_params(bottom = "off", top = "off", left = "off", right = "off")
    cbar.set_ticks(ticks)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [])
        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticklabels, tick_fp = tick_fp)
    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
    cbar.set_label(label, fontproperties = gen_font(label_fp))

################################################## INTERNAL FUNCTIONS ##################################################
def _set_axes(set_label, set_bound, set_ticks, set_ticklabels, set_tick_params, ticks, ticklabels = None, tick_fp = "8r",
      label = "", label_fp = "10b", **kwargs):
    """
    Formats an axis

    **Arguments:**
        :*set_label*:       Function to set axis label
        :*set_bound*:       Function to set axis boundaries
        :*set_ticks*:       Function to set axis ticks
        :*set_ticklabels*:  Function to set axis ticklabels
        :*set_tick_params*: Function to set axis tick parameters
        :*ticks*:           Ticks
        :*tick_kw*:         Keyword arguments to be passed to set_ticks(...)
        :*ticklabels*:      Tick labels
        :*tick_fp*:         Tick label font; passed to gen_font(...)
        :*ticklabel_kw*:    Keyword arguments to be passed to set_ticklabels(...)
        :*tick_params*:     Keyword arguments to be passed to set_tick_params(...)
        :*label*:           Label text
        :*label_fp*:        Label font; passed to gen_font(...)
        :*label_kw*:        Keyword arguments to be passed to set_label(...)

    .. todo::
        - Support gridlines
    """
    if ticks != []:
        set_bound(float(ticks[0]), float(ticks[-1]))
    if ticklabels is None:
        ticklabels = ticks
    set_ticks(np.array(ticks, np.float32),                         **kwargs.get("tick_kw",      {}))
    set_ticklabels(ticklabels, fontproperties = gen_font(tick_fp), **kwargs.get("ticklabel_kw", {}))
    set_label(label, fontproperties = gen_font(label_fp),          **kwargs.get("label_kw",     {}))
    set_tick_params(                                               **kwargs.get("tick_params",  {}))


