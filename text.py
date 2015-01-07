#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.text.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec on 15-01-03
"""
Functions for formatting text

.. todo:
    - Check
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys, types
import matplotlib
from . import gen_font, get_edges, multi_kw
from .Debug import Debug_Arguments
################################## FUNCTIONS ###################################
@Debug_Arguments()
def set_title(figure_or_subplot, title_kw = {}, **kwargs):
    """
    Prints a title for a figure or subplot

    **Arguments:**
        :*figure_or_subplot*: <Figure> or <Axes> on which to act
        :*text*: Title text; *s*, *t*, *title*, and *label* also
                 supported
        :*fp*:   Title font properties; *fontproperties* also
                 supported; passed to gen_font(...)
        :*top*:  Distance between top of figure and title (inches);
                 applies to Figure title only

    **Returns:**
        :*text*: New <Text>
    """
    if isinstance(figure_or_subplot, matplotlib.figure.Figure):
        title_kw["fontproperties"] = gen_font(multi_kw(
          ["fp", "fontproperties", "title_fp"],
          "14b",
          kwargs))
        figure       = figure_or_subplot
        title_kw["ha"] = kwargs.pop("ha", "center")
        title_kw["va"] = kwargs.pop("va", "center")
        title_kw["y"]  = kwargs.pop("y", 
          (figure.get_figheight() - title_kw.pop("top", kwargs.pop("top", 1.0)))
          / figure.get_figheight())
        title_kw["t"]  = multi_kw(["s", "t", "text", "title", "label"],
          "", kwargs)
        return figure.suptitle(t = title_kw.pop("t"), **title_kw)
    elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
        title_kw["fontproperties"] = gen_font(multi_kw(
          ["fp", "fontproperties", "title_fp"], "12b", kwargs))
        subplot = figure_or_subplot
        title_kw["label"] = multi_kw(["s", "t", "text", "title", "label"],
          "", kwargs)
        return subplot.set_title(**title_kw)

@Debug_Arguments()
def set_bigxlabel(figure_or_subplots, *args, **kwargs):
    """
    Prints a large x-axis label shared by multiple subplots

    **Arguments:**
        :*figure_or_subplots*: <Figure> or OrderedDict of <Axes> on
                               which to act
        :*text*:   Label text; *s*, *label*, and *xlabel* also
                   supported
        :*fp*:     Label font properties ; *fontproperties* also
                   supported; passed to gen_font(...)
        :*bottom*: Distance between bottom of figure and label
                   (inches); if negative, distance between bottommost
                   plot and label
        :*top*:    Distance between top of figure and label (inches); if
                   negative, distance between topmost plot and label;
                   overrides *bottom*
        :*x*:      Horizontal position of label in figure reference
                   frame (proportion 0.0-1.0); overrides *bottom*/*top*
        :*y*:      Vertical   position of label in figure reference
                   frame (proportion 0.0-1.0); overrides *bottom*/*top*

    **Returns:**
        :*text*:   New <Text>
    """
    kwargs["fontproperties"] = gen_font(multi_kw(
      ["fp", "fontproperties", "label_fp"], "12b", kwargs))
    if   isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges  = get_edges(figure)
    elif isinstance(figure_or_subplots, types.DictType):
        subplots = figure_or_subplots
        figure   = subplots.values()[0].get_figure()
        edges    = get_edges(subplots)
    if "top" in kwargs:
        top = kwargs.pop("top")
        if top < 0:
          kwargs["y"] = numpy.max(edges["y"]) - top / figure.get_figheight()
        else:
          kwargs["y"] = kwargs.pop("y",
            (figure.get_figheight() - top) / figure.get_figheight())
    else:
        bottom = kwargs.pop("bottom", 0.2)
        if bottom < 0:
          kwargs["y"] = numpy.min(edges["y"]) + bottom / figure.get_figheight()
        else:
          kwargs["y"] = kwargs.pop("y", bottom / figure.get_figheight())
    kwargs["x"] = kwargs.pop("x",
      (numpy.min(edges["x"]) + numpy.max(edges["x"])) / 2.0)
    kwargs["s"] = multi_kw(["s", "text", "label", "xlabel"],
      args[0] if len(args) >= 1 else "", kwargs)
    return set_text(figure, **kwargs)

@Debug_Arguments()
def set_bigylabel(figure_or_subplots, *args, **kwargs):
    """
    Prints a large x-axis label shared by multiple subplots

    **Arguments:**
        :*figure_or_subplots*: <Figure> or OrderedDict of <Axes> on
                               which to act
        :*text*:     Label text; *s*, *label*, and *ylabel* also
                     supported
        :*fp*:       Label font properties; *fontproperties* also
                     supported; passed to gen_font(...)
        :*left*:     Distance between left side of figure and label
                     (inches); if negative, distance between leftmost
                     plot and label
        :*right*:    Distance between right side of figure and label
                     (inches); if negative, distance between rightmost
                     plot and label; overrides *left*
        :*x*:        Horizontal position of label in figure reference
                     frame (proportion 0.0-1.0); overrides
                     *left*/*right*
        :*y*:        Vertical position of label in figure reference
                     frame (proportion 0.0-1.0); overrides
                     *left*/*right*
        :*rotation*: Label rotation; default: 'vertical'

    **Returns:**
        :*text*:   New <Text>
    """
    kwargs["fontproperties"] = gen_font(multi_kw(
      ["fp", "fontproperties", "label_fp"], "12b", kwargs))
    if   isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges  = get_edges(figure)
    elif isinstance(figure_or_subplots, types.DictType):
        subplots = figure_or_subplots
        figure   = subplots.values()[0].get_figure()
        edges    = get_edges(subplots)
    if "right" in kwargs:
        right = kwargs.pop("right")
        if right < 0:
          kwargs["x"] = numpy.max(edges["x"]) - right / figure.get_figwidth()
        else:
          kwargs["x"] = kwargs.pop("x",
            (figure.get_figwidth() - right) / figure.get_figwidth())
    else:
        left = kwargs.pop("left", 0.2)
        if left < 0:
           kwargs["x"] = numpy.min(edges["x"]) + left / figure.get_figwidth()
        else:
           kwargs["x"] = kwargs.pop("x", left / figure.get_figwidth())
    kwargs["y"]     = kwargs.pop("y",
      (numpy.min(edges["y"]) + numpy.max(edges["y"])) / 2.0)
    kwargs["rotation"] = kwargs.pop("rotation", "vertical")
    kwargs["s"] = multi_kw(["s", "text", "label", "ylabel"],
      args[0] if len(args) >= 1 else "", kwargs)
    return set_text(figure, **kwargs)

@Debug_Arguments()
def set_inset(subplot, *args, **kwargs):
    """
    Prints an inset to a subplot

    **Arguments:**
        :*subplot*: <Axes> on which to act
        :*text*:    Inset text; *s* and *inset* also supported
        :*fp*:      Inset font; *fontproperties* also supported; passed
                    to gen_font(...)
        :*xpro*:    Horizontal position of inset in subplot reference
                    frame; (proportion 0.0-1.0)
        :*ypro*:    Vertical   position of inset in subplot reference
                    frame; (proportion 0.0-1.0)
        :*x*:       Horizontal position of inset in subplot reference
                    frame; overrides *xpro*
        :*y*:       Vertical   position of inset in subplot reference
                    frame; overrides *ypro*
        :*ha*:      Text horizontal alignment; default: 'left'
        :*va*:      Text vertical alignment; default: 'top'

    **Returns:**
        :*text*:    New <Text>
    """
    kwargs["fontproperties"] = gen_font(multi_kw(
      ["fp", "fontproperties", "inset_fp"], "12b", kwargs))
    xpro         = kwargs.pop("xpro", 0.05)
    ypro         = kwargs.pop("ypro", 0.95)
    kwargs["ha"] = kwargs.pop("ha", "left")
    kwargs["va"] = kwargs.pop("va", "top")
    xbound       = subplot.get_xbound()
    ybound       = subplot.get_ybound()
    if subplot.xaxis_inverted():
        kwargs["x"] = kwargs.pop("x",
          xbound[0] + (1-xpro) * (xbound[1] - xbound[0]))
    else:
        kwargs["x"] = kwargs.pop("x",
          xbound[0] + xpro     * (xbound[1] - xbound[0]))
    if subplot.yaxis_inverted():
        kwargs["y"] = kwargs.pop("y",
          ybound[0] + (1-ypro) * (ybound[1] - ybound[0]))
    else:
        kwargs["y"] = kwargs.pop("y",
          ybound[0] + ypro     * (ybound[1] - ybound[0]))
    kwargs["s"] = multi_kw(["s", "text", "inset"],
      args[0] if len(args) >= 1 else "", kwargs)
    return set_text(subplot, **kwargs)

@Debug_Arguments()
def set_text(figure_or_subplot, *args, **kwargs):
    """
    Prints text on a figure or subplot

    **Arguments:**
        :*figure_or_subplot*: <Figure> or <Axes> on which to act
        :*text*: Text; *s* also supported
        :*fp*:   Font properties ; *fontproperties* also supported;
                 passed to gen_font(...)
        :*ha*:   Text horizontal alignment; default: 'center'
        :*va*:   Text vertical alignment; default: 'center'

    **Returns:**
        :*text*:              New <Text>
    """
    kwargs["fontproperties"] = gen_font(multi_kw(["fp", "fontproperties"],
      "10r", kwargs))
    kwargs["s"]  = multi_kw(["s", "text"],
      args[0] if len(args) >= 1 else "", kwargs)
    kwargs["ha"] = kwargs.pop("ha", "center")
    kwargs["va"] = kwargs.pop("va", "center")
    if "left" in kwargs:
        if   isinstance(figure_or_subplot, matplotlib.figure.Figure):
            kwargs["x"] = kwargs.pop("left") / figure_or_subplot.get_figwidth()
        elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
            raise()
    if "top" in kwargs:
        if   isinstance(figure_or_subplot, matplotlib.figure.Figure):
            kwargs["y"] = kwargs.pop("top") / figure_or_subplot.get_figheight()
        elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
            raise()
    return figure_or_subplot.text(**kwargs)


