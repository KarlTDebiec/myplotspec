# -*- coding: utf-8 -*-
#   myplotspec.text.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
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
def set_title(figure_or_subplot, *args, **kwargs):
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
    from warnings import warn
    import matplotlib
    from . import (FP_KEYS, get_edges, get_font, multi_get,
                   multi_get_copy, multi_pop)

    # Determine title and keyword arguments
    title_kw = multi_get_copy("title_kw", kwargs, {})
    title = multi_get_copy("title", kwargs)

    # Determine font and other settings
    title_fp = multi_get_copy("title_fp", kwargs)
    title_fp_2 = multi_pop(["title_fp"] + FP_KEYS, title_kw)
    if title_fp_2 is not None:
        title_kw["fontproperties"] = get_font(title_fp_2)
    elif title_fp is not None:
        title_kw["fontproperties"] = get_font(title_fp)
    title_kw["horizontalalignment"] = multi_pop(["horizontalalignment", "ha"],
      title_kw, "center")
    title_kw["verticalalignment"] = multi_pop(["verticalalignment", "va"],
      title_kw, "center")

    # Determine drawing target and title
    if isinstance(figure_or_subplot, matplotlib.figure.Figure):
        figure = figure_or_subplot
        fig_height = figure.get_figheight()
        edges = get_edges(figure)

        title_2 = multi_pop(["title", "t"], title_kw)
        if title_2 is not None:
            title_kw["t"] = title_2
        elif title is not None:
            title_kw["t"] = title
        elif len(args) >= 1:
            title_kw["t"] = args[0]
        else:
            return None

        if "x" not in title_kw:
            title_kw["x"] = (edges["left"] + edges["right"]) / 2

        if "top" in title_kw:
            top = title_kw.pop("top")
            if top > 0:
                title_kw["y"] = (fig_height - top) / fig_height
            else:
                title_kw["y"] = ((edges["top"] * fig_height)
                  - top) / fig_height

        if "fontproperties" in title_kw:
            warn("matplotlib's figure.suptitle method currently supports "
                 "setting only only font size and weight, other font "
                 "settings may be lost.")
            fontproperties = title_kw.pop("fontproperties")
            title_kw["size"] = fontproperties.get_size()
            title_kw["weight"] = fontproperties.get_weight()

        return figure.suptitle(**title_kw)

    elif isinstance(figure_or_subplot, matplotlib.axes.Axes):
        subplot = figure_or_subplot

        title_2 = multi_pop(["title", "label"], title_kw)
        if title_2 is not None:
            title_kw["label"] = title_2
        elif title is not None:
            title_kw["label"] = title
        elif len(args) >= 1:
            title_kw["label"] = args[0]
        else:
            return None

        return subplot.set_title(**title_kw)

def set_shared_xlabel(figure_or_subplots, *args, **kwargs):
    """
    Draws an x axis label shared by multiple subplots.

    The horizontal position of the shared x label is by default the
    center of the selected subplots, and the vertical position is
    halfway between the bottommost subplot and the bottom of the figure.

    Arguments:
      figure_or_subplots (Figure, OrderedDict): Subplots to use to
        calculate label horizontal position; if Figure, all subplots
        present on figure are used
      [shared_][x]label (str): Label text
      [shared_][x]label_fp (str, dict, FontProperties): Label font
      [shared_][x]label_kw (dict): Keyword arguments passed to
        :func:`set_text`
      bottom (float): Distance between bottom of figure and label
        (inches); if negative, distance between bottommost plot and
        label
      top (float): Distance between top of figure and label (inches); if
        negative, distance between topmost subplot and label; overrides
        ``bottom``
      x (float): X position within figure (proportion 0.0-1.0); default
        = center of selected subplots
      y (float): Y position within figure (proportion 0.0-1.0);
        overrides ``bottom`` and ``top``; default = halfway between
        bottommost subplot and bottom of figure

    Returns:
      (Text): X axis label
    """
    import matplotlib
    from . import (FP_KEYS, get_edges, get_font, multi_get,
                   multi_get_copy, multi_pop)

    # Determine label and keyword arguments
    label_kw = multi_get_copy(["shared_xlabel_kw", "xlabel_kw", "label_kw"],
                 kwargs, {})
    label = multi_get_copy(["shared_xlabel", "xlabel", "label"], kwargs)
    label_2 = multi_pop(["shared_xlabel", "xlabel", "label", "s"], label_kw)
    if label_2 is not None:
        label_kw["s"] = label_2
    elif label is not None:
        label_kw["s"] = label
    elif len(args) >= 1:
        label_kw["s"] = args[0]
    else:
        return None

    # Determine font and other settings
    label_fp = multi_get_copy(["shared_xlabel_fp", "xlabel_fp","label_fp"]
      + FP_KEYS, kwargs)
    label_fp_2 = multi_pop(["shared_xlabel_fp", "xlabel_fp","label_fp"]
      + FP_KEYS, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif label_fp is not None:
        label_kw["fontproperties"] = get_font(label_fp)
    label_kw["horizontalalignment"] = multi_pop(["horizontalalignment",
      "ha"], label_kw, "center")
    label_kw["verticalalignment"] = multi_pop(["verticalalignment",
      "va"], label_kw, "center")

    # x and y are specified in relative figure coordinates
    # top and bottom are specified in inches
    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges  = get_edges(figure)
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots
        figure = subplots.values()[0].get_figure()
        edges = get_edges(subplots)
    if "x" not in label_kw:
        label_kw["x"] = (edges["left"] + edges["right"]) / 2
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

    return set_text(figure, text_kw=label_kw, **kwargs)

def set_shared_ylabel(figure_or_subplots, *args, **kwargs):
    """
    Draws a y-axis label shared by multiple subplots.

    The vertical position of the shared y label is by default the
    center of the selected subplots, and the horizontal position is
    halfway between the leftmost subplot and the left edge of the
    figure.

    Arguments:
      figure_or_subplots (Figure, OrderedDict): Subplots to use to
        calculate label vertical position; if Figure, all subplots
        present on figure are used
      [shared_][y]label (str): Label text
      [shared_][y]label_fp (str, dict, FontProperties): Label font
      [shared_][y]label_kw (dict): Keyword arguments passed to
        :func:`set_text`
      left (float): Distance between left edge of figure and label
        (inches); if negative, distance between leftmost plot and label
      right (float): Distance between right edge of figure and label
        (inches); if negative, distance between rightmost plot and
        label; overrides ``left``
      x (float): X position within figure (proportion 0.0-1.0);
        overrides ``left`` and ``right``; default = halfway between
        leftmost subplot and left edge of figure
      y (float): Y position within figure (proportion 0.0-1.0); default
        = center of selected subplots

    Returns:
      (Text): Y axis label
    """
    import matplotlib
    from . import (FP_KEYS, get_edges, get_font, multi_get,
                   multi_get_copy, multi_pop)

    # Determine label and keyword arguments
    label_kw = multi_get_copy(["shared_ylabel_kw", "ylabel_kw", "label_kw"],
                 kwargs, {})
    label = multi_get_copy(["shared_ylabel", "ylabel", "label"], kwargs)
    label_2 = multi_pop(["shared_ylabel", "ylabel", "label", "s"], label_kw)
    if label_2 is not None:
        label_kw["s"] = label_2
    elif label is not None:
        label_kw["s"] = label
    elif len(args) >= 1:
        label_kw["s"] = args[0]
    else:
        return None

    # Determine font and other settings
    label_fp = multi_get_copy(["shared_ylabel_fp", "ylabel_fp","label_fp"]
      + FP_KEYS, kwargs)
    label_fp_2 = multi_pop(["shared_ylabel_fp", "ylabel_fp","label_fp"]
      + FP_KEYS, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif label_fp is not None:
        label_kw["fontproperties"] = get_font(label_fp)
    label_kw["horizontalalignment"] = multi_pop(["horizontalalignment",
      "ha"], label_kw, "center")
    label_kw["verticalalignment"] = multi_pop(["verticalalignment",
      "va"], label_kw, "center")
    label_kw["rotation"] = label_kw.pop("rotation", 90)

    # Determine location
    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        edges = get_edges(figure)
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots
        figure = subplots.values()[0].get_figure()
        edges = get_edges(subplots)

    # x and y are specified in relative figure coordinates
    # left and right are specified in inches
    if "x" not in label_kw:
        fig_width = figure.get_figwidth()
        if "left" in label_kw:
            left = label_kw.pop("left")
            if left < 0:
                label_kw["x"] = (((edges["left"] * fig_width) + left)
                              / fig_width)
            else:
                label_kw["x"] = left / fig_width
        elif "right" in label_kw:
            right = label_kw.pop("right")
            if right < 0:
                label_kw["x"] = (((edges["right"] * fig_width) - right)
                              / fig_width)
            else:
                label_kw["x"] = (fig_width - right) / fig_width
        else:
            label_kw["x"] = edges["left"] / 2

    if "y" not in label_kw:
        label_kw["y"] = (edges["bottom"] + edges["top"]) / 2

    return set_text(figure, text_kw=label_kw, **kwargs)

def set_label(subplot, *args, **kwargs):
    from . import (FP_KEYS, get_edges, get_font, multi_get, multi_get_copy,
                   multi_pop)

    # Determine label and keyword arguments
    label_kw = multi_get_copy("label_kw", kwargs, {})
    label = multi_get_copy("label", kwargs)
    label_2 = multi_pop(["label", "s"], label_kw)
    if label_2 is not None:
        label_kw["s"] = label_2
    elif label is not None:
        label_kw["s"] = label
    elif len(args) >= 1:
        label_kw["s"] = args[0]
    else:
        return None

    # Determine font and other settings
    label_fp = multi_get_copy("label_fp", kwargs)
    label_fp_2 = multi_pop(["label_fp"] + FP_KEYS, label_kw)
    if label_fp_2 is not None:
        label_kw["fontproperties"] = get_font(label_fp_2)
    elif label_fp is not None:
        label_kw["fontproperties"] = get_font(label_fp)

    # x and y are specified in data, proportional, or absolute coordinates
    if "x" in label_kw and "y" in label_kw:
        pass
    elif "xpro" in label_kw and "ypro" in label_kw:
        label_kw["x"] = label_kw.pop("xpro")
        label_kw["y"] = label_kw.pop("ypro")
        kwargs["transform"] = subplot.transAxes
    elif "xabs" in label_kw and "yabs" in label_kw:
        edges = get_edges(subplot, absolute=True)
        xabs = label_kw.pop("xabs")
        yabs = label_kw.pop("yabs")
        if xabs > 0:
            label_kw["x"] = xabs / edges["width"]
        else:
            label_kw["x"] = (edges["width"] + xabs) / edges["width"]
        if yabs > 0:
            label_kw["y"] = yabs / edges["height"]
        else:
            label_kw["y"] = (edges["height"] + yabs) / edges["height"]
        kwargs["transform"] = subplot.transAxes

    if "border_lw" in label_kw:
        kwargs["border_lw"] = label_kw.pop("border_lw")
    return set_text(subplot, text_kw=label_kw, **kwargs)

def set_text(figure_or_subplot, *args, **kwargs):
    """
    Prints text on a figure or subplot.

    Arguments:
      figure_or_subplot (Figure, Axes): Object on which to draw
      text (str): Text
      text_fp (str, dict, FontProperties): Text font
      text_kw (dict): Keyword arguments passed to ``text()``

    Returns:
      (Text): Text
    """
    import matplotlib
    from  matplotlib import patheffects
    from . import (FP_KEYS, get_colors, get_font, multi_get, multi_get_copy,
                   multi_pop)

    # Determine text and keyword arguments
    text_kw = multi_get_copy("text_kw", kwargs, {})
    get_colors(text_kw)
    text = multi_get_copy(["text", "s"], kwargs)
    text_2 = multi_pop(["text", "s"], text_kw)
    if text_2 is not None:
        text_kw["s"] = text_2
    elif text is not None:
        text_kw["s"] = text
    elif len(args) >= 1:
        text_kw["s"] = args[0]
    else:
        return None

    # Determine font settings
    text_fp = multi_get_copy(["text_fp"] + FP_KEYS, kwargs)
    text_fp_2 = multi_pop(["text_fp"] + FP_KEYS, text_kw)
    if text_fp_2 is not None:
        text_kw["fontproperties"] = get_font(text_fp_2)
    elif text_fp is not None:
        text_kw["fontproperties"] = get_font(text_fp)

    # x and y
    x = multi_get_copy("x", kwargs)
    if x is not None and not "x" in text_kw:
        text_kw["x"] = x
    y = multi_get_copy("y", kwargs)
    if y is not None and not "y" in text_kw:
        text_kw["y"] = y

    # Transform
    if "transform" in kwargs:
        text_kw["transform"] = kwargs.pop("transform")

    # Draw text
    text = figure_or_subplot.text(**text_kw)

    # Draw border
    border_lw = multi_get_copy("border_lw", kwargs)
    if border_lw is not None:
        text.set_path_effects(
          [patheffects.Stroke(linewidth=border_lw,
           foreground="w"), patheffects.Normal()])
    return text
