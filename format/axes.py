#!/usr/bin/python
#   plot_toolkit.format.axes.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-09
####################################################### MODULES ########################################################
import os, sys, warnings
import numpy as np
from   ...plot_toolkit.auxiliary import get_edges, gen_font
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_xaxis(subplot, **kwargs):
    """
    Formats an X axis

    **Arguments:**
        :*subplot*:             <matplotlib.axes.AxesSubplot> on which to act
        :*ticks*:               X Axis ticks
        :*tick_kwargs*:         Keyword arguments to be passed to set_xticks
        :*ticklabels*:          X Axis tick labels
        :*tick_fp*:             X Axis tick font in form of '##L'
        :*ticklabel_kwargs*:    Keyword arguments to be passed to set_xticklabels
        :*label*:               X Axis label
        :*label_fp*:            X Axis label font in form of '##L'
        :*label_kwargs*:        Keyword arguments to be passed to set_xlabel
        :*outline*:             Add dark outline to axis
    """
    _set_axes(subplot.set_xlabel, subplot.set_xbound, subplot.axvline, subplot.set_xticks, subplot.set_xticklabels,
             **kwargs)

def set_yaxis(subplot, **kwargs):
    """
    Formats a Y axis

    **Arguments:**
        :*subplot*:             <matplotlib.axes.AxesSubplot> on which to act
        :*ticks*:               Y Axis ticks
        :*tick_kwargs*:         Keyword arguments to be passed to set_yticks
        :*ticklabels*:          Y Axis tick labels
        :*tick_fp*:             Y Axis tick font in form of '##L'
        :*ticklabel_kwargs*:    Keyword arguments to be passed to set_yticklabels
        :*label*:               Y Axis label
        :*label_fp*:            Y Axis label font in form of '##L'
        :*label_kwargs*:        Keyword arguments to be passed to set_ylabel
        :*outline*:             Add dark outline to axis
    """
    _set_axes(subplot.set_ylabel, subplot.set_ybound, subplot.axhline, subplot.set_yticks, subplot.set_yticklabels,
             **kwargs)

def set_colorbar(cbar, ticks, ticklabels, label = "", label_fp = "12b", tick_fp = "8r", **kwargs):
    """
    Formats a colorbar

    **Arguments:**
        :*cbar*:        <matplotlib.colorbar.ColorBar> to be acted on
        :*ticks*:       Color bar ticks
        :*ticklabels*:  Color bar tick labels
        :*tick_fp*:     Color bar tick label font in form of '##L'
        :*label*:       Color bar label
        :*label_fp*:    Color bar label font in form of '##L'
    """
    zticks  = np.array(ticks, np.float32)
    zticks  = (zticks - zticks[0]) / (zticks[-1] - zticks[0])
    cbar.ax.tick_params(bottom = "off", top = "off", left = "off", right = "off")
    cbar.set_ticks(ticks)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [],         outline = False)
        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticklabels, outline = False, tick_fp = tick_fp)
    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
    cbar.set_label(label, fontproperties = gen_font(label_fp))

################################################## PRIVATE FUNCTIONS ###################################################
def _set_axes(set_label, set_bound, axline, set_ticks, set_ticklabels, ticks = range(11), ticklabels = range(11),
             tick_fp = "8r", label = "", label_fp = "11b", **kwargs):
    """
    Formats an axis

    **Arguments:**
        :*set_label*:           Function to set the axis label
        :*set_bound*:           Function to set the axis' boundaries
        :*axline*:              Function to draw a vertical or horizontal line on the axis
        :*set_ticks*:           Function to set the axis' ticks
        :*set_ticklabels*:      Function to set the axis'
        :*ticks*:               Axis ticks
        :*tick_kwargs*:         Keyword arguments to be passed to set_ticks
        :*ticklabels*:          Axis tick labels
        :*tick_fp*:             Axis tick font in form of '##L'
        :*ticklabel_kwargs*:    Keyword arguments to be passed to set_ticklabels
        :*label*:               Axis label
        :*label_fp*:            Axis label font in form of '##L'
        :*label_kwargs*:        Keyword arguments to be passed to set_label
        :*outline*:             Add dark outline to axis

    .. todo::
        - Should not draw outline using setax[h,v]line, should set the spline width directly
        - Consider accepting font as either '##L' or <matplotlib.font_manager.FontProperties> object
        - Consider adding support for gridlines
    """
    if ticks != []:
        set_bound(float(ticks[0]), float(ticks[-1]))
        if kwargs.get("outline", True):
            axline(ticks[0],  linewidth = 2, color = "black")
            axline(ticks[-1], linewidth = 2, color = "black")
    set_ticks(np.array(ticks, np.float32),                          **kwargs.get("tick_kwargs",      {}))
    set_ticklabels(ticklabels, fontproperties = gen_font(tick_fp),  **kwargs.get("ticklabel_kwargs", {}))
    set_label(label, fontproperties = gen_font(label_fp),           **kwargs.get("label_kwargs",     {}))

