# -*- coding: utf-8 -*-
#   myplotspec.text.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Functions for formatting text.

.. todo:
  - Resolve inconsistencies in how positions are determined, without
    conflicting with matplotlib's style. Most likely, x and y should
    retain their matplotlib behavior, being proportions when used with
    figures and coordinates when used with subplots. Text functions
    below should support xpro and ypro that are always proportions, xabs
    and yabs that are always absolute coordinates, for subplots xcrd and
    ycrd in subplot coordinates, and finally left, right, top, and
    bottom in inches.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def set_title(figure_or_subplot, title=None, title_fp=None, *args,
    **kwargs):
    """
    Draws a title on a Figure or subplot.

    Arguments:
      figure_or_subplot (Figure, Axes): Object on which to draw title
      title (str): Title text
      title_fp (str, dict, FontProperties): Title font
      top (float): Distance between top of figure and title (inches);
        Figure title only
      title_kw (dict): Keyword arguments passed to ``Figure.suptitle()``
        or ``Axes.set_title()``

    Returns:
      (*Text*): Title

    .. todo:
        - If top is negative, use distance from highest subplot
    """
    import matplotlib
    from . import get_font, multi_kw, FP_KEYS

    title_kw = kwargs.pop("title_kw", {})

    title_fp_2 = multi_kw(["title_fp"] + FP_KEYS, title_kw)
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

def set_shared_xlabel(figure_or_subplots, xlabel=None, xlabel_fp=None,
    label_fp=None, *args, **kwargs):
    """
    Draws an x axis label shared by multiple subplots.

    The horizontal position of the shared x label is (by default) the
    center of the selected subplots, and the vertical position is a
    specified distance from the bottom of the figure.

    Arguments:
      figure_or_subplots (Figure, OrderedDict): Subplots to use to
        calculate label horizontal position; if Figure, all subplots
        present on figure are used
      xlabel (str): Label text
      [x]label_fp (str, dict, FontProperties): Label font
      xlabel_kw (dict): Keyword arguments passed to :func:`set_text`
      bottom (float): Distance between bottom of figure and label
        (inches); if negative, distance between bottommost plot and
        label
      top (float): Distance between top of figure and label; if
        negative, distance between topmost subplot and label; overrides
        ``bottom``
      x (float): X position within figure (proportion 0.0-1.0); default
        = center of selected subplots
      y (float): Y position within figure (proportion 0.0-1.0);
        overrides ``bottom`` and ``top``

    Returns:
      (*Text*): X axis label
    """
    import matplotlib
    from . import get_edges, get_font, multi_kw, FP_KEYS

    label_kw = kwargs.pop("xlabel_kw", {})

    label_fp_2 = multi_kw(["xlabel_fp", "label_fp"] + FP_KEYS, label_kw)
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
        label_kw["x"] = (edges["left"] + edges["right"]) / 2.0
    if "y" not in label_kw:
        fig_height = figure.get_figheight()
        if "top" in label_kw:
            top = label_kw.pop("top")
            if top >= 0:
                label_kw["y"] = (fig_height - top) / fig_height
            else:
                label_kw["y"] = (((edges["top"] * fig_height) + top)
                              / fig_height)
        elif "bottom" in label_kw:
            bottom = label_kw.pop("bottom")
            if bottom >= 0:
                label_kw["y"] = bottom / fig_height
            else:
                label_kw["y"] = (((edges["bottom"] * fig_height) + bottom)
                              / fig_height)
        else:
            label_kw["y"] = edges["bottom"] / 2

    return set_text(figure, text_kw = label_kw, **kwargs)

def set_shared_ylabel(figure_or_subplots, ylabel=None, ylabel_fp=None,
    label_fp=None, *args, **kwargs):
    """
    Draws a y-axis label shared by multiple subplots.

    The vertical position of the shared y label is (by default) the
    center of the selected subplots, and the horizontal position is a
    specified distance from the left edge of the figure.

    Arguments:
      figure_or_subplots (Figure, OrderedDict): Subplots to use to
        calculate label vertical position; if Figure, all subplots
        present on figure are used
      ylabel (str): Label text
      [y]label_fp (str, dict, FontProperties): Label font
      ylabel_kw (dict): Keyword arguments passed to :func:`set_text`
      left (float): Distance between left side of figure and label; if
        negative, distance between leftmost plot and label
      right (float): Distance between right side of figure and label; if
        negative, distance between rightmost plot and label; overrides
        ``left``
      x (float): X position within figure (proportion 0.0-1.0);
        overrides ``left`` and ``right``
      y (float): Y position within figure (proportion 0.0-1.0); default
        = center of selected subplots

    Returns:
      (*Text*): Y axis label
    """
    import matplotlib
    from . import get_edges, get_font, multi_kw, FP_KEYS

    label_kw = kwargs.pop("ylabel_kw", {})

    label_fp_2 = multi_kw(["ylabel_fp", "label_fp"] + FP_KEYS, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif ylabel_fp is not None:
        label_kw["fontproperties"] = get_font(ylabel_fp)
    elif label_fp   is not None:
        label_kw["fontproperties"] = get_font(label_fp)

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
    elif isinstance(figure_or_subplots, dict):
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
                label_kw["x"] = (edges["left"] + left) / fig_width
            else:
                label_kw["x"] = left / fig_width

    if "y" not in label_kw:
        label_kw["y"] = (edges["bottom"] + edges["top"]) / 2.0

    return set_text(figure, text_kw = label_kw, **kwargs)

def set_inset(subplot, inset=None, inset_fp=None, *args, **kwargs):
    """
    Draws a text inset on a subplot.

    Arguments:
      subplot (Axes): Subplot on which to draw inset
      inset (str): Inset text
      inset_fp (str, dict, FontProperties): Inset font
      inset_kw (dict): Keyword arguments passed to :func:`set_text`
      xpro (float): X position within subplot (proportion 0.0-1.0)
      ypro (float): Y position within subplot (proportion 0.0-1.0)
      x (float): X position within subplot (subplot coordinate);
        overrides ``xpro``
      y (float): Y position within subplot (subplot coordinate),
        overrides ``ypro``

    Returns:
      (*Text*): Inset text
    """
    from . import get_font, multi_kw, FP_KEYS

    inset_kw = kwargs.pop("inset_kw", {})

    inset_fp_2 = multi_kw(["inset_fp"] + FP_KEYS, inset_kw)
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

def set_text(figure_or_subplot, s=None, text=None, text_fp=None, *args,
    **kwargs):
    """
    Prints text on a figure or subplot.

    Arguments:
      figure_or_subplot (Figure, Axes): Object on which to draw
      text (str): Text
      text_fp (str, dict, FontProperties): Text font
      text_kw (dict): Keyword arguments passed to ``text()``

    Returns:
      (*Text*): Text
    """
    from . import get_font, multi_kw, FP_KEYS

    text_kw = kwargs.pop("text_kw", {})

    text_fp_2 = multi_kw(["text_fp"] + FP_KEYS, text_kw)
    if text_fp_2 is not None:
        text_kw["fontproperties"] = get_font(text_fp_2)
    elif text_fp   is not None:
        text_kw["fontproperties"] = get_font(text_fp)

    text_2 = multi_kw(["text", "s"], text_kw)
    if text_2 is not None:
        text_kw["s"] = text_2
    elif s is not None:
        text_kw["s"] = s
    elif text is not None:
        text_kw["s"] = text
    elif len(args) >= 1:
        text_kw["s"] = args[0]
    else:
        return None

    return figure_or_subplot.text(**text_kw)
