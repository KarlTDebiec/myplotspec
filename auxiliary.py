#!/usr/bin/python
#   plot_toolkit.auxiliary.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-09
####################################################### MODULES ########################################################
import os, sys
import numpy as np
from   collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.cm as cm
import matplotlib.colors as cl
################################################## GENERAL FUNCTIONS ###################################################
def abs_listdir(directory, **kwargs):
    """
    **Arguments:**
        :*directory*:   directory whose contents to list

    **Yields:**
        :*file*:        Full path to each file

    .. todo::
        - Why is this a generator? This should be able to just return a list.
    """
    for dirpath, _, filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

def hsl_to_rgb(h, s, l, **kwargs):
    """
    **Arguments:**
        :*h*:   hue          (0.0 - 1.0)
        :*s*:   saturation   (0.0 - 1.0)
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

def rgb_to_hsl(r, g, b):
    """
    **Arguments:**
        :*r*:   red   (0.0 - 1.0)
        :*g*:   green (0.0 - 1.0)
        :*b*:   blue  (0.0 - 1.0)

    **Returns:**
        :*hsl*: Numpy array of equivalent hue, saturation, luminescence

    .. todo::
        - Should smoothly accept separate r, g, b variables or list or numpy array of length 3
    """
    x   = max(r, g, b)
    n   = min(r, g, b)
    c   = x - n
    l   = 0.5 * (x + n)
    if   c == 0.: h = 0.
    elif x == r:  h = (((g - b) / c) % 6.) / 6.
    elif x == g:  h = (((b - r) / c) + 2.) / 6.
    elif x == b:  h = (((r - g) / c) + 4.) / 6.
    if   c == 0:  s = 0.
    else:         s = c / (1. - np.abs(2. * l - 1.))
    return np.array([h, s, l])

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

################################################# MATPLOTLIB FUNCTIONS #################################################
def get_edges(figure, **kwargs):
    """
    **Arguments:**
        :*figure*:  <matplotlib.figure.Figure> on which to act

    **Returns:**
        :*edges*:   Dictionary; keys are 'x' and 'y', values are numpy arrays with dimensions (axis, min...max)
    """
    return {"x": np.array([[ax.get_position().xmin, ax.get_position().xmax] for ax in figure.axes]),
            "y": np.array([[ax.get_position().ymin, ax.get_position().ymax] for ax in figure.axes])}

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


