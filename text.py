#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.text.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Functions for formatting text
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_title(figure_or_subplot, title = None, title_fp = None, *args,
    **kwargs):
    """
    Draw a title on *figure_or_subplot*

    **Arguments:**
        :*figure_or_subplot*: <Figure> or <Axes> on which to act
        :*title*:    Title text
        :*title_fp*: Title font
        :*top*:      Distance between top of figure and title (inches);
                     Figure title only
        :*title_kw*: Keyword arguments passed to figure.suptitle() or
                     subplot.set_title()

    **Additional title_kw Arguments:**
        :*top*: Distance between top of figure and title

    **Returns:**
        :*title*: <Text>

    .. todo:
        - If *top* is negative, use distance from highest subplot
    """
    import matplotlib
    from . import get_font, multi_kw, fp_keys

    title_kw = kwargs.pop("title_kw", {})

    title_fp_2 = multi_kw(["title_fp"] + fp_keys, title_kw)
    if title_fp_2 is not None:
        title_kw["fontproperties"] = get_font(title_fp_2)
    elif title_fp   is not None:
        title_kw["fontproperties"] = get_font(title_fp)

    if isinstance(figure_or_subplot, matplotlib.figure.Figure):
        figure = figure_or_subplot

        title_2 = multi_kw(["title", "t"], title_kw)
        if title_2 is not None:
            title_kw["t"] = title_2
        elif title   is not None:
            title_kw["t"] = title
        elif len(args) >= 1:
            title_kw["t"] = args[0]
        else:
            return None

        if "top" in title_kw:
            top           = title_kw.pop
            fig_height    = figure.get_figheight()
            title_kw["y"] = (fig_height - top) / fig_height

        return figure.suptitle(**title_kw)

    elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
        subplot = figure_or_subplot

        title_2 = multi_kw(["title", "label"], title_kw)
        if title_2 is not None:
            title_kw["label"] = title_2
        elif title   is not None:
            title_kw["label"] = title
        elif len(args) >= 1:
            title_kw["label"] = args[0]
        else:
            return None

        return subplot.set_title(**title_kw)

def set_shared_xlabel(figure_or_subplots, xlabel = None, xlabel_fp = None,
    label_fp = None, *args, **kwargs):
    """
    Draws an x-axis label shared by multiple subplots

    **Arguments:**
        :*figure_or_subplots*: <Figure> or OrderedDict of <Axes> on
                               which to act; if Figure, position is
                               relative to all subplots, if
                               OrderedDict, position is relative to
                               subplots in OrderedDict only
        :*xlabel*:      Label text
        :*[x]label_fp*: Label font
        :*xlabel_kw*:   Keyword arguments passed to set_text()

    **Additional xlabel_kw Arguments:**
        :*top*:    Distance between top of figure and label; if
                   negative, distance between topmost plot and label;
                   overrides *bottom*
        :*bottom*: Distance between bottom of figure and label; if
                   negative, distance between bottommost plot and label

    **Returns:**
        :*label*: <Text>
    """
    import matplotlib
    from . import get_font, multi_kw, fp_keys

    label_kw = kwargs.pop("xlabel_kw", {})

    label_fp_2 = multi_kw(["xlabel_fp", "label_fp"] + fp_keys, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif xlabel_fp is not None:
        label_kw["fontproperties"] = get_font(xlabel_fp)
    elif label_fp is not None:
        label_kw["fontproperties"] = get_font(label_fp)

    label_2 = multi_kw(["xlabel", "label", "s"], label_kw)
    if label_2 is not None:
        label_kw["s"] = label_2
    elif xlabel is not None:
        label_kw["s"] = xlabel
    elif len(args) >= 1:
        label_kw["s"] = args[0]
    else:
        return None

    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges  = get_edges(figure)
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots
        figure   = subplots.values()[0].get_figure()
        edges    = get_edges(subplots)

    if "x" not in label_kw:
        label_kw["x"] = (edges["min"] + edges["max"]) / 2.0

    if "y" not in label_kw:
        fig_height = figure.get_figheight()
        if "top" in label_kw:
            top = label_kw.pop("top")
            if top < 0:
                label_kw["y"] = (edges["top"] - top) / fig_height
            else:
                label_kw["y"] = (fig_height - top) / fig_height
        else:
            bottom = label_kw.pop("bottom", -0.5)
            if bottom < 0:
                label_kw["y"] = (edges["bottom"] + bottom) / fig_height
            else:
                label_kw["y"] = bottom / fig_height

    return set_text(figure, text_kw = label_kw, **kwargs)

def set_shared_ylabel(figure_or_subplots, ylabel = None, ylabel_fp = None,
    label_fp = None, *args, **kwargs):
    """
    Draws a y-axis label shared by multiple subplots

    **Arguments:**
        :*figure_or_subplots*: <Figure> or OrderedDict of <Axes> on
                               which to act; if Figure, position is
                               relative to all subplots, if OrderDict,
                               position is relative to subplots in
                               OrderedDict
        :*ylabel*:      Label text
        :*[y]label_fp*: Label font
        :*ylabel_kw*:   Keyword arguments passed to set_text()

    **Additional ylabel_kw Arguments:**
        :*left*:     Distance between left side of figure and label; if
                     negative, distance between leftmost plot and label
        :*right*:    Distance between right side of figure and label;
                     if negative, distance between rightmost plot and
                     label; overrides *left*
        :*rotation*: Label rotation; default: 'vertical'

    **Returns:**
        :*text*: <Text>
    """
    import matplotlib
    from . import get_font, multi_kw, fp_keys

    label_kw = kwargs.pop("ylabel_kw", {})

    label_fp_2 = multi_kw(["ylabel_fp", "label_fp"] + fp_keys, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif ylabel_fp is not None:
        label_kw["fontproperties"] = get_font(ylabel_fp)
    elif label_fp   is not None:
        label_kw["fontproperties"] = get_font(label_fp)

    if "rotation" not in label_kw:
        label_kw["rotation"] = rotation

    label_2 = multi_kw(["ylabel", "label", "s"], label_kw)
    if label_2 is not None:
        label_kw["s"] = label_2
    elif ylabel is not None:
        label_kw["s"] = ylabel
    elif len(args) >= 1:
        label_kw["s"] = args[0]
    else:
        return None

    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges  = get_edges(figure)
    elif isinstance(figure_or_subplots, types.DictType):
        subplots = figure_or_subplots
        figure   = subplots.values()[0].get_figure()
        edges    = get_edges(subplots)

    if "x" not in label_kw:
        fig_width = figure.get_figwidth()
        if "right" in label_kw:
            right = label_kw.pop("right")
            if right < 0:
                label_kw["x"] = (edges["right"] - right) / fig_width
            else:
                label_kw["x"] = (fig_width - right) / fig_width
        else:
            left = label_kw.pop("left", -0.5)
            if left < 0:
                label_kw["x"] = (edges["min"] + left) / fig_width
            else:
                label_kw["x"] = left / fig_width

    if "y" not in label_kw:
        label_kw["y"] = (edges["min"] + edges["max"]) / 2.0

    return set_text(figure, text_kw = label_kw, **kwargs)

def set_inset(subplot, inset = None, inset_fp = None, *args, **kwargs):
    """
    Draws an inset on a subplot

    **Arguments:**
        :*subplot*:  <Axes> on which to act
        :*inset*:    Inset text
        :*inset_fp*: Inset font
        :*inset_kw*: Keyword arguments passed to set_text()

    **Additional inset_kw Arguments:**
        :*x*:        Horizontal position of inset in subplot reference
                     frame (subplot coordinate); overrides *xpro*
        :*y*:        Vertical   position of inset in subplot reference
                     frame (subplot coordinate), overrides *ypro*
        :*xpro*:     Horizontal position of inset in subplot reference
                     frame (proportion)
        :*ypro*:     Vertical   position of inset in subplot reference
                     frame (proportion)

    **Returns:**
        :*text*: <Text>

    .. todo:
        - Support providing x and y in standard units (e.g. inches),
          probably via *left*, *right*, *top*, *bottom*
    """
    from . import get_font, multi_kw, fp_keys

    inset_kw = kwargs.pop("inset_kw", {})

    inset_fp_2 = multi_kw(["inset_fp"] + fp_keys, inset_kw)
    if inset_fp_2 is not None:
        inset_kw["fontproperties"] = get_font(inset_fp_2)
    elif inset_fp   is not None:
        inset_kw["fontproperties"] = get_font(inset_fp)

    if "ha" not in inset_kw:
        inset_kw["ha"] = "left"

    if "va" not in inset_kw:
        inset_kw["va"] = "top"

    inset_2 = multi_kw(["inset", "s"], inset_kw)
    if inset_2 is not None:
        inset_kw["s"] = inset_2
    elif inset is not None:
        inset_kw["s"] = inset_2
    elif len(args) >= 1:
        inset_kw["s"] = args[0]
    else:
        return None

    if "x" not in inset_kw:
        xmin, xmax = subplot.get_xbound()
        xpro = inset_kw.pop("xpro", 0.05)
        if subplot.xaxis_inverted():
            inset_kw["x"] = xmin + (1 - xpro) * (xmax - xmin)
        else:
            inset_kw["x"] = xmin +      xpro  * (xmax - xmin)

    if "y" not in inset_kw:
        ymin, ymax = subplot.get_ybound()
        ypro = inset_kw.pop("ypro", 0.95)
        if subplot.yaxis_inverted():
            inset_kw["y"] = ymin + (1 - ypro) * (ymax - ymin)
        else:
            inset_kw["y"] = ymax +      ypro  * (ymax - ymin)

    return set_text(subplot, test_kw = inset_kw, **kwargs)

def set_text(figure_or_subplot, text = None, text_fp = None, *args, **kwargs):
    """
    Prints text on a figure or subplot

    **Arguments:**
        :*figure_or_subplot*: <Figure> or <Axes> on which to act
        :*text*:    Text
        :*text_fp*: Text Font
        :*text_kw*: Keyword arguments passed to text()

    **Returns:**
        :*text*: <Text>
    """
    from . import get_font, multi_kw, fp_keys

    text_kw = kwargs.pop("text_kw", {})

    text_fp_2 = multi_kw(["text_fp"] + fp_keys, text_kw)
    if text_fp_2 is not None:
        text_kw["fontproperties"] = get_font(text_fp_2)
    elif text_fp   is not None:
        text_kw["fontproperties"] = get_font(text_fp)

    if "va" not in inset_kw:
        inset_kw["va"] = "top"

    text_2 = multi_kw(["text", "s"], text_kw)
    if text_2 is not None:
        text_kw["s"] = text_2
    elif text is not None:
        text_kw["s"] = text_2
    elif len(args) >= 1:
        text_kw["s"] = args[0]
    else:
        return None

    return figure_or_subplot.text(**text_kw)
