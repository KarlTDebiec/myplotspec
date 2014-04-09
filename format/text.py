#!/usr/bin/python
#   plot_toolkit.format.text.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-09
####################################################### MODULES ########################################################
import os, sys
import numpy as np
from   ...plot_toolkit.auxiliary import get_edges, gen_font
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_title(figure, edge_distance = 0.5, fp = "16b", **kwargs):
    """
    Prints a title for a figure

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*edge_distance*:   Distance between top of subplots and vertical center of title; proportion (0.0-1.0)
        :*s*:               Figure title
        :*fp*:              Figure title font in form of '##L'
        :*x*:               Horizontal center of title in figure reference frame (0.0-1.0)
        :*y*:               Vertical center of title in figure reference frame (0.0-1.0)

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Consider merging with plot_toolkit.set_subtitle and acting appropriately depending on whether a figure or
          subplot is passed
        - Several of these labeling functions can probably be merged analagously to set_[x,y]axis
    """
    edges       = get_edges(figure)
    kwargs["x"] = kwargs.get("x", (np.min(edges["x"]) + np.max(edges["x"])) / 2.0)
    kwargs["y"] = kwargs.get("y",  np.max(edges["y"]) + float(1.0 - np.max(edges["y"])) * edge_distance)
    set_text(figure, fp = fp, **kwargs)

def set_subtitle(subplot, label, fp = "11b", **kwargs):
    """
    Prints a title above a subplot

    **Arguments:**
        :*subplot*: <matplotlib.axes.AxesSubplot> on which to act
        :*label*:   Subplot label
        :*fp*:      Subplot label font in form of '##L'

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Consider merging with plot_toolkit.set_title and acting appropriately depending on whether a figure or
          subplot is passed
        - Several of these labeling functions can probably be merged analagously to set_[x,y]axis
    """
    subplot.set_title(label = label, fontproperties = gen_font(fp), **kwargs)

def set_bigxlabel(figure, edge_distance = 0.3, fp = "11b", **kwargs):
    """
    Prints a large X axis label shared by multiple subplots

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*edge_distance*:   Distance between bottom of subplots and vertical center of title; proportion (0.0-1.0)
        :*s*:               Figure X axis label
        :*fp*:              Figure X axis label font in form of '##L'
        :*x*:               Horizontal center of title in figure reference frame (0.0-1.0)
        :*y*:               Vertical center of title in figure reference frame (0.0-1.0)

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Several of these labeling functions can probably be merged analagously to set_[x,y]axis
    """
    edges       = get_edges(figure)
    kwargs["x"] = (np.min(edges["x"]) + np.max(edges["x"])) / 2.0
    kwargs["y"] =  np.min(edges["y"]) * edge_distance
    set_text(figure, fp = fp, **kwargs)

def set_bigylabel(figure, side = "left", edge_distance = 0.3, fp = "11b", **kwargs):
    """
    Prints a large Y axis label shared by multiple subplots

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*edge_distance*:   Distance between furthest left of subplots and horizontal center of title;
                            proportion (0.0-1.0)
        :*s*:               Figure X axis label
        :*fp*:              Figure X axis label font in form of '##L'
        :*x*:               Horizontal center of title in figure reference frame; proportion (0.0-1.0)
        :*y*:               Vertical center of title in figure reference frame; proportion (0.0-1.0)

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Several of these labeling functions can probably be merged analagously to set_[x,y]axis
    """
    edges               = get_edges(figure)
    if side == "left":    kwargs["x"] = np.min(edges["x"]) * edge_distance
    else:                 kwargs["x"] = 1.0 - (1.0 - np.max(edges["x"])) * edge_distance
    kwargs["y"]         = (np.min(edges["y"]) + np.max(edges["y"])) / 2.0
    set_text(figure, fp = fp, rotation = "vertical", **kwargs)

def set_inset(subplot, xpos = 0.5, ypos = 0.9, fp = "11b", **kwargs):
    """
    Prints text as an inset to a subplot
    Text is formally printed to subplot's parent figure, not subplot itself

    **Arguments:**
        :*subplot*: matplotlib.axes.AxesSubplot on which to act
        :*s*:       Inset text
        :*fp*:      Inset text font in form of '##L'
        :*xpos*:    Horizontal center of title in subplot reference frame; proportion (0.0-1.0)
        :*ypos*:    Vertical center of title in subplot reference frame; proportion (0.0-1.0)
        :*x*:       Horizontal center of inset in subplot reference frame; proportion (0.0-1.0); overrides *xpos*
        :*y*:       Vertical center of inset in subplot reference frame; proportion (0.0-1.0); overrides *ypos*

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Why is text printed to figure and not subplot?
        - Several of these labeling functions can probably be merged analagously to set_[x,y]axis
    """
    position    = axes.get_position()
    kwargs["x"] = kwargs.get("x", position.xmin + xpos * position.width)
    kwargs["y"] = kwargs.get("y", position.ymin + ypos * position.height)
    set_text(subplot.get_figure(), fp = fp, **kwargs)

def set_text(figure_or_subplot, fp = "11b", ha = "center", va = "center", **kwargs):
    """
    Prints text on a figure or subplot

    **Arguments:**
        :*figure_or_subplot*:   <matplotlib.figure.Figure> or <matplotlib.axes.AxesSubplot> on which to act
        :*s*:                   Text
        :*fp*:                  Text font in form of '##L'
        :*ha*:                  Text horizontal alignment
        :*va*:                  Text vertical alignment

    **Returns:**
        :*text*:                <matplotlib.text.Text>

    .. todo::
        - Accept text more intelligently (i.e. as a positional or better-named argument than *s*)
        - Do *ha* and *va* need to be arguments to this function?
    """
    return figure_or_subplot.text(ha = ha, va = va, fontproperties = gen_font(fp), **kwargs)


