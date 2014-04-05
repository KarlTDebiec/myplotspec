#!/usr/bin/python
#   plot_toolkit.__init__.py
#   Written by Karl Debiec on 12-10-22
#   Last updated by Karl Debiec 14-04-04
"""
Standard functions for plotting
"""
####################################################### MODULES ########################################################
import os, sys, warnings, types
import numpy as np
from   collections import OrderedDict
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.cm as cm
import matplotlib.colors as cl
from   matplotlib.backends.backend_pdf import PdfPages
################################################## GENERAL FUNCTIONS ###################################################
def abs_listdir(directory, **kwargs):
    """
    **Arguments:**
        :*directory*:   directory whose contents to list

    **Yields:**
        Full path to each file

    .. todo::
        - Why is this a generator? This should be able to just return a list.
    """
    for dirpath, _, filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
def hsl_to_rgb(h, s, l, **kwargs):
    """
    **Arguments:**
        :*h*:   hue (0.0 - 1.0)
        :*s*:   saturation (0.0 - 1.0)
        :*l*:   luminescence (0.0 - 1.0)

    **Returns:**
        :*rgb*: Numpy array of equivalent red, green, blue

    .. todo::
        - Should smoothly accept separate h, s, l variables or list or numpy array of length 3
    """
    c   = (1. - abs(2. * l - 1.)) * s
    hp  = h * 6
    i   = c * (1. - abs(hp % 2. - 1.))
    m   = l - 0.5 * c
    if   hp >= 0. and hp <  1.: return np.array([c,  i,  0.]) + m
    elif hp >= 1. and hp <  2.: return np.array([i,  c,  0.]) + m
    elif hp >= 2. and hp <  3.: return np.array([0., c,   i]) + m
    elif hp >= 3. and hp <  4.: return np.array([0., i,   c]) + m
    elif hp >= 4. and hp <  5.: return np.array([i,  0.,  c]) + m
    elif hp >= 5. and hp <= 6.: return np.array([c,  0.,  i]) + m
def pad_zero(ticks, **kwargs):
    """
    **Arguments:**
        :*ticks*:           List or numpy array of ticks

    **Returns:**
        :*tick_labels*:     Tick labels, each with the same number of trailing zeros
    """
    n_zeros = 0
    for tick in ticks:
        if '.' in str(tick):    n_zeros = max(n_zeros, len(str(tick).split('.')[1]))
    if n_zeros  == 0:   return np.array(ticks, dtype = np.int)
    else:               return ["{0:.{1}f}".format(tick, n_zeros) for tick in ticks]
def gen_font(fp, **kwargs):
    """
    **Arguments:**
        :*fp*:  String of form '##L' in which '##' is the font size and 'L' is 'r' for regular or 'b' for bold

    **Returns:**
        :*fp*:  <matplotlib.font_manager.FontProperties> object to given specifications

    .. todo::
        - Should accept additional kwargs to pass to FontProperties
    """
    return fm.FontProperties(family = "Arial", size = int(fp[:-1]), weight = {"r":"regular","b":"bold"}[fp[-1]])
def get_edges(figure, **kwargs):
    """
    **Arguments:**
        :*figure*:  <matplotlib.figure.Figure> on which to act

    **Returns:**
        :*edges*:   Dictionary; keys are 'x' and 'y', values are numpy arrays with dimensions (axis, min...max)
    """
    return {"x": np.array([[ax.get_position().xmin, ax.get_position().xmax] for ax in figure.axes]),
            "y": np.array([[ax.get_position().ymin, ax.get_position().ymax] for ax in figure.axes])}
def gen_contour_levels(I, cutoff = 0.9875, include_negative = False, **kwargs):
    """
    **Arguments:**
        :*I*:                   Intensity
        :*cutoff*:              Proportion of data below minimum level (0.0-1.0)
        :*include_negative*:    Return levels for negative intensity as well as positive

    **Returns:**
        :*levels*:              Numpy array of levels

    .. todo::
        - Should allow number of levels to be set
        - Should allow minimum level and maximum level to be set manually
        - Needs partner function to analyze amino acid sequence, estimate number of peaks, and choose appropriate cutoff
        - Double check overall; probably could be considerably improved
    """
    I_flat      = np.sort(I.flatten())
    min_level   = I_flat[int(I_flat.size * cutoff)]
    max_level   = I_flat[-1]
    exp_int     = (max_level ** (1.0 / 9.0)) / (min_level ** (1.0 / 9.0))
    p_levels    = np.array([min_level * exp_int ** a for a in range(0, 10, 1)][:-1], dtype = np.int)
    if include_negative:
        I_flat      = I_flat[I_flat < 0]
        min_level   = -1 * I_flat[0]
        max_level   = -1 * I_flat[int(I_flat.size * (1 - cutoff))]
        exp_int     = (max_level ** (1.0 / 9.0)) / (min_level ** (1.0 / 9.0))
        m_levels    = -1 * np.array([min_level * exp_int ** a for a in range(0, 10, 1)][:-1], dtype = np.int)
        return        np.append(m_levels, p_levels)
    else:
        return p_levels
def gen_cmap(color, **kwargs):
    """
    Returns colormap that is *color* over all values; not really useful for heatmaps but useful for countours

    **Arguments:**
        :*color*:   Tuple, list, or numpy array of red, green, and blue (0.0-1.0);
                    Alternatively, string of named matplotlib color
    **Returns:**
        :*cmap*:    <matplotlib.colors.LinearSegmentedColormap>

    .. todo::
        - Should accept matplotlib's 1-letter color codes
    """
    if isinstance(color, str):
        if   color == "blue":       r, g, b = [0.00, 0.00, 1.00]
        elif color == "red":        r, g, b = [1.00, 0.00, 0.00]
        elif color == "green":      r, g, b = [0.00, 0.50, 0.00]
        elif color == "cyan":       r, g, b = [0.00, 0.75, 0.75]
        elif color == "magenta":    r, g, b = [0.75, 0.00, 0.75]
        elif color == "yellow":     r, g, b = [0.75, 0.75, 0.00]
        elif color == "black":      r, g, b = [0.00, 0.00, 0.00]
    else: r, g, b = color
    cdict   = {"red": ((0, r, r), (1, r, r)), "green": ((0, g, g), (1, g, g)), "blue": ((0, b, b), (1, b, b))}
    return    cl.LinearSegmentedColormap("cmap", cdict, 256)
def gen_figure_subplots(**kwargs):
    """
    Generates figure and subplots according to selected format.

    **Arguments:**
        :*format*:      String of form 'L##' in which 'L' is 'l' for landscape or 'p' for portrait and '##' is the
                        number of subplots
        :*fig_w*:       Figure width
        :*fig_h*:       Figure height
        :*sub_w*:       Subplot width
        :*sub_h*:       Subplot height
        :*mar_t*:       Top margin
        :*mar_r*:       Right margin
        :*mar_w*:       Horizontal margin between subplots
        :*mar_h*:       Vertical margin between subplots

    **Returns:**
        :*figure*:      matplotlib.figure.Figure
        :*subplots*:    OrderedDict of <matplotlib.axes.AxesSubplot> (1-indexed)

    .. todo::
        Is there still a point to this? It ended up fairly similar to matplotlib.figure.subplots_adjust().
    """
    format = kwargs.get("format", "l1").lower()
    if   format == "l1":
        fig_w, fig_h    = kwargs.get("fig_w", 10.000), kwargs.get("fig_h",  7.500)  # Figure dimensions
        sub_w, sub_h    = kwargs.get("sub_w",  9.100), kwargs.get("sub_h",  6.500)  # Subplot dimensions
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)  # Outer margins
    elif format == "l4":
        fig_w, fig_h    = kwargs.get("fig_w", 10.000), kwargs.get("fig_h",  7.500)
        sub_w, sub_h    = kwargs.get("sub_w",  4.200), kwargs.get("sub_h",  3.000)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
        mar_w, mar_h    = kwargs.get("mar_w",  0.700), kwargs.get("mar_h",  0.500)  # Subplot margins
    elif format == "p1":
        fig_w, fig_h    = kwargs.get("fig_w",  7.500), kwargs.get("fig_h", 10.000)
        sub_w, sub_h    = kwargs.get("sub_w",  6.600), kwargs.get("sub_h",  4.700)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
    elif format == "p4":
        fig_w, fig_h    = kwargs.get("fig_w",  7.500), kwargs.get("fig_h", 10.000)
        sub_w, sub_h    = kwargs.get("sub_w",  2.950), kwargs.get("sub_h",  2.100)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
        mar_w, mar_h    = kwargs.get("mar_w",  0.700), kwargs.get("mar_h",  0.500)
    figure  = plt.figure(figsize = [fig_w, fig_h])
    subplots = OrderedDict()
    if   format.endswith("1"):
        subplots[1] = figure.add_subplot(1, 1, 1, autoscale_on = False)
        subplots[1].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,    # Left
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,    # Bottom
                                   sub_w                            / fig_w,    # Width
                                   sub_h                            / fig_h])   # Height
    elif format.endswith("4"):
        for i in [1,2,3,4]: subplots[i] = figure.add_subplot(2, 2, i, autoscale_on = False)
        subplots[1].set_position([(fig_w - mar_r - mar_w - 2*sub_w) / fig_w,
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[2].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[3].set_position([(fig_w - mar_r - mar_w - 2*sub_w) / fig_w,
                                  (fig_h - mar_t - mar_h - 2*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[4].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,
                                  (fig_h - mar_t - mar_h - 2*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
    return figure, subplots
########################################### MATPLOTLIB FORMATTING FUNCTIONS ############################################
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
    set_axis(subplot.set_xlabel, subplot.set_xbound, subplot.axvline, subplot.set_xticks, subplot.set_xticklabels,
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
    set_axis(subplot.set_ylabel, subplot.set_ybound, subplot.axhline, subplot.set_yticks, subplot.set_yticklabels,
             **kwargs)

def set_axis(set_label, set_bound, axline, set_ticks, set_ticklabels, ticks = range(11), ticklabels = range(11),
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
        - Should draw outline using setax[h,v]line, should set the spline width directly
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

def set_legend(subplot, handles = None, labels = None, fp = "8r", loc = 1, **kwargs):
    """
    Draws and formats a legend on *subplot*
    By default includes all series, or accepts manual lists of *handles* and *labels* for plotted series

    **Arguments:**
        :*subplot*: <matplotlib.axes.AxesSubplot> on which to act
        :*handles*: List of handles for plotted series (e.g. <matplotlib.lines.Line2D>)
        :*labels*:  List of labels for plotted series
        :*fp*:      Legend font in form of '##L'
        :*loc*:     Legend location
        :*kwargs*:  Keyword arguments to be passed to subplot.legend

    **Returns:**
        :*legend*:  matplotlib.legend.Legend

    .. todo::
        - Does *loc* need to be an argument to this function?
    """
    if handles is not None and labels is not None:
        return subplot.legend(handles, labels, loc = loc, prop = gen_font(fp), **kwargs)
    else:
        return subplot.legend(loc = loc, prop = gen_font(fp), **kwargs)

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


