#!/usr/bin/python
#   plot_toolkit.text.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-05-03
"""
Functions for formatting text
"""
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys
import numpy as np
import matplotlib
from . import gen_font, get_edges, multi_kw
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_title(figure_or_subplot, *args, **kwargs):
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
    if   isinstance(figure_or_subplot, matplotlib.figure.Figure):
        kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "14b"))
        figure       = figure_or_subplot
        kwargs["ha"] = kwargs.pop("ha", "center")
        kwargs["va"] = kwargs.pop("va", "center")
        kwargs["y"]  = (figure.get_figheight() - kwargs.pop("top", 1.0)) / figure.get_figheight()
        kwargs["t"]  = multi_kw(["s", "t", "text", "title", "label"], args[0] if len(args) >= 1 else "", kwargs)
        return figure.suptitle(**kwargs)
    elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
        kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "12b"))
        kwargs["label"] = multi_kw(["s", "text", "title", "label"], args[0] if len(args) >= 1 else "", kwargs)
        return figure_or_subplot.set_title(**kwargs)

def set_bigxlabel(figure, *args, **kwargs):
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
    kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "12b", kwargs))
    edges           = get_edges(figure)
    if "top" in kwargs:
        top         = kwargs.pop("top")
        kwargs["y"] = kwargs.get("y", (figure.get_figheight() - top) / figure.get_figheight())
    else:
        bottom      = kwargs.get("bottom", 0.2)
        kwargs["y"] = kwargs.get("y", bottom / figure.get_figheight())
    kwargs["x"]     = kwargs.get("x", (np.min(edges["x"]) + np.max(edges["x"])) / 2.0)
    kwargs["s"]     = multi_kw(["s", "text", "label", "xlabel"], args[0] if len(args) >= 1 else "", kwargs)
    return set_text(figure, **kwargs)

def set_bigylabel(figure, *args, **kwargs):
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
    kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "12b", kwargs))
    edges           = get_edges(figure)
    if "right" in kwargs:
        right       = kwargs.pop("right")
        kwargs["x"] = kwargs.get("x", (figure.get_figwidth() - right) / figure.get_figwidth())
    else:
        left        = kwargs.get("left", 0.2)
        kwargs["x"] = kwargs.get("x", left / figure.get_figwidth())
    kwargs["y"]     = kwargs.get("y", (np.min(edges["y"]) + np.max(edges["y"])) / 2.0)
    kwargs["rotation"] = kwargs.get("rotation", "vertical")
    kwargs["s"]     = multi_kw(["s", "text", "label", "ylabel"], args[0] if len(args) >= 1 else "", kwargs)
    return set_text(figure, **kwargs)

def set_inset(subplot, *args, **kwargs):
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
    kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "12b", kwargs))
    xpos         = kwargs.pop("xpos", 0.05)
    ypos         = kwargs.pop("ypos", 0.95)
    kwargs["ha"] = kwargs.pop("ha", "left")
    kwargs["va"] = kwargs.pop("va", "top")
    xbound       = subplot.get_xbound()
    ybound       = subplot.get_ybound()
    if subplot.xaxis_inverted(): kwargs["x"] = kwargs.get("x", xbound[0] + (1-xpos) * (xbound[1] - xbound[0]))
    else:                        kwargs["x"] = kwargs.get("x", xbound[0] + xpos     * (xbound[1] - xbound[0]))
    if subplot.yaxis_inverted(): kwargs["y"] = kwargs.get("y", ybound[0] + (1-ypos) * (ybound[1] - ybound[0]))
    else:                        kwargs["y"] = kwargs.get("y", ybound[0] + ypos     * (ybound[1] - ybound[0]))
    kwargs["s"]  = multi_kw(["s", "text", "inset"], args[0] if len(args) >= 1 else "", kwargs)
#    print(kwargs, xpos, ypos, xbound, ybound)
    return set_text(subplot, **kwargs)

def set_text(figure_or_subplot, *args, **kwargs):
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
    kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"], "10r", kwargs))
    kwargs["s"]  = multi_kw(["s", "text"], args[0] if len(args) >= 1 else "", kwargs)
    kwargs["ha"] = kwargs.pop("ha", "center")
    kwargs["va"] = kwargs.pop("va", "center")
    return figure_or_subplot.text(**kwargs)

