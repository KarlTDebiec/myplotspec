#!/usr/bin/python
#   plot_toolkit.axes.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec 14-05-04
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
    kwargs["tick_params"] = dict(kwargs.get("tick_params", {}).items() + dict(axis = "x").items())
    _set_axes(subplot.set_xlabel, subplot.set_xbound, subplot.set_xticks, subplot.set_xticklabels, subplot.tick_params,
      **kwargs)
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
        :*label*:        Label text
        :*label_fp*:     Label font; passed to gen_font(...)
        :*label_kw*:     Keyword arguments to be passed to set_ylabel(...)
        :*lw*:           Width of y-axis lines
    """
    kwargs["tick_params"] = dict(kwargs.get("tick_params", {}).items() + dict(axis = "y").items())
    _set_axes(subplot.set_ylabel, subplot.set_ybound, subplot.set_yticks, subplot.set_yticklabels, subplot.tick_params,
      **kwargs)
    subplot.spines["left"].set_lw(lw)
    subplot.spines["right"].set_lw(lw)

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


