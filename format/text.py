#!/usr/bin/python
#   plot_toolkit.format.text.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-16
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys
import numpy as np
from ..auxiliary import get_edges, gen_font
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_title(figure, edge_distance = 0.5, fp = "16b", **kwargs):
    """
    Prints a title for a figure

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*text*:            Figure title text ('s' and 'title' also supported)
        :*edge_distance*:   Distance between top of subplots and vertical center of title; proportion (0.0-1.0)
        :*fp*:              Figure title font in form of '##L'
        :*x*:               Horizontal position of title in figure reference frame (0.0-1.0); (override)
        :*y*:               Vertical   position of title in figure reference frame (0.0-1.0); (override)

    .. todo::
        - Consider merging with plot_toolkit.set_subtitle and acting appropriately depending on whether a figure or
          subplot is passed
    """
    edges       = get_edges(figure)
    kwargs["x"] = kwargs.get("x", (np.min(edges["x"]) + np.max(edges["x"])) / 2.0)
    kwargs["y"] = kwargs.get("y",  np.max(edges["y"]) + float(1.0 - np.max(edges["y"])) * edge_distance)
    kwargs["s"] = kwargs.pop("s", kwargs.pop("text", kwargs.pop("title")))
    return set_text(figure, fp = fp, **kwargs)

def set_subtitle(subplot, label, fp = "11b", **kwargs):
    """
    Prints a title above a subplot

    **Arguments:**
        :*subplot*: <matplotlib.axes.AxesSubplot> on which to act
        :*label*:   Subplot label
        :*fp*:      Subplot label font in form of '##L'

    .. todo::
        - Consider merging with plot_toolkit.set_title and acting appropriately depending on whether a figure or
          subplot is passed
    """
    return subplot.set_title(label = label, fontproperties = gen_font(fp), **kwargs)

def set_bigxlabel(figure, edge_distance = 0.3, fp = "11b", **kwargs):
    """
    Prints a large X axis label shared by multiple subplots

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*text*:            Figure X axis label text ('s' and 'label' also supported)
        :*edge_distance*:   Distance between bottom of subplots and vertical center of title; proportion (0.0-1.0)
        :*fp*:              Figure X axis label font in form of '##L'
        :*x*:               Horizontal position of title in figure reference frame (0.0-1.0); (override)
        :*y*:               Vertical   position of title in figure reference frame (0.0-1.0); (override)

    **Returns:**
        :*text*:                <matplotlib.text.Text>
    """
    edges       = get_edges(figure)
    kwargs["x"] = kwargs.get("x", (np.min(edges["x"]) + np.max(edges["x"])) / 2.0)
    kwargs["y"] = kwargs.get("y",  np.min(edges["y"]) * edge_distance)
    kwargs["s"] = kwargs.pop("s", kwargs.pop("text", kwargs.pop("label")))
    return set_text(figure, fp = fp, **kwargs)

def set_bigylabel(figure, side = "left", edge_distance = 0.3, fp = "11b", **kwargs):
    """
    Prints a large Y axis label shared by multiple subplots

    **Arguments:**
        :*figure*:          <matplotlib.figure.Figure> on which to act
        :*text*:            Figure Y axis label text ('s' and 'label' also supported)
        :*fp*:              Figure Y axis label font in form of '##L'
        :*edge_distance*:   Distance between furthest left of subplots and horizontal center of title;
                            proportion (0.0-1.0)
        :*x*:               Horizontal position of label in figure reference frame; proportion (0.0-1.0); (override)
        :*y*:               Vertical   position of label in figure reference frame; proportion (0.0-1.0); (override)

    **Returns:**
        :*text*:                <matplotlib.text.Text>
    """
    edges   = get_edges(figure)
    if side == "left":    kwargs["x"] = kwargs.get("x", np.min(edges["x"]) * edge_distance)
    else:                 kwargs["x"] = kwargs.get("x", 1.0 - (1.0 - np.max(edges["x"])) * edge_distance)
    kwargs["y"]                       = kwargs.get("y", (np.min(edges["y"]) + np.max(edges["y"])) / 2.0)
    kwargs["s"] = kwargs.pop("s", kwargs.pop("text", kwargs.pop("label")))
    return set_text(figure, fp = fp, rotation = "vertical", **kwargs)

def set_inset(subplot, xpos = 0.5, ypos = 0.5, fp = "11b", **kwargs):
    """
    Prints text as an inset to a subplot

    **Arguments:**
        :*subplot*: <matplotlib.axes.AxesSubplot> on which to act
        :*text*:    Inset text ('s' and 'inset' also supported)
        :*fp*:      Inset text font in form of '##L'
        :*xpos*:    Horizontal position of inset in subplot reference frame; proportion (0.0-1.0)
        :*ypos*:    Vertical   position of inset in subplot reference frame; proportion (0.0-1.0)
        :*x*:       Horizontal position of inset in subplot reference frame; absolute (overrides *xpos*)
        :*y*:       Vertical   position of inset in subplot reference frame; absolute (overrides *ypos*)

    **Returns:**
        :*text*:    <matplotlib.text.Text>
    """
    xbound      = subplot.get_xbound()
    ybound      = subplot.get_ybound()
    kwargs["x"] = kwargs.get("x", xbound[0] + xpos * xbound[1])
    kwargs["y"] = kwargs.get("y", ybound[0] + ypos * ybound[1])
    kwargs["s"] = kwargs.pop("s", kwargs.pop("text", kwargs.pop("inset")))
    return set_text(subplot, fp = fp, **kwargs)

def set_text(figure_or_subplot, fp = "11b", ha = "center", va = "center", **kwargs):
    """
    Prints text on a figure or subplot

    **Arguments:**
        :*figure_or_subplot*:   <matplotlib.figure.Figure> or <matplotlib.axes.AxesSubplot> on which to act
        :*text*:                Text ('s' also supported)
        :*fp*:                  Text font in form of '##L' (default: '11b')
        :*ha*:                  Text horizontal alignment  (default: 'center')
        :*va*:                  Text vertical alignment    (default: 'center')

    **Returns:**
        :*text*:                <matplotlib.text.Text>
    """
    kwargs["s"] = kwargs.pop("s", kwargs.pop("text"))
    return figure_or_subplot.text(ha = ha, va = va, fontproperties = gen_font(fp), **kwargs)


