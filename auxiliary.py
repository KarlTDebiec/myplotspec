#!/usr/bin/python
#   plot_toolkit.auxiliary.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-17
"""
Auxiliary functions used for various tasks

..todo:
    - Add function to identify subplots; accept subplot OrderedDict and print index in center of each plot
    - Consider moving some import statements to functions
"""
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys
import numpy as np
from collections import OrderedDict
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

def pad_zero(ticks, digits = None, **kwargs):
    """
    Generates a list of tick labels, each with the same number of digits after the decimal

    **Arguments:**
        :*ticks*:       List or numpy array of ticks
        :*digits*:      Number of digits to include after the decimal

    **Returns:**
        :*tick_labels*: Tick labels, each with the same number of digits after the decimal
    """
    # If the number of digits to include has not been specified, use the largest number of digits in the provided ticks
    if digits is None:
        digits = 0
        for tick in ticks:
            if '.' in str(tick):    digits = max(digits, len(str(tick).split('.')[1]))
    if digits  == 0:
        return np.array(ticks, dtype = np.int)
    else:
        return ["{0:.{1}f}".format(tick, digits) for tick in ticks]

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
    min_level   = kwargs.get("min_level", I_flat[int(I_flat.size * cutoff)])
    max_level   = kwargs.get("max_level", I_flat[-1])
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
    Returns colormap that is *color* over all values 

    Not useful for heatmaps; useful for countours

    **Arguments:**
        :*color*:   Tuple, list, or numpy array of red, green, and blue (0.0-1.0);
                    Alternatively, string of named matplotlib color
    **Returns:**
        :*cmap*:    <matplotlib.colors.LinearSegmentedColormap>
    """
    if isinstance(color, str):
        if   color in ["b", "blue"]:    r, g, b = [0.00, 0.00, 1.00]
        elif color in ["r", "red"]:     r, g, b = [1.00, 0.00, 0.00]
        elif color in ["g", "green"]:   r, g, b = [0.00, 0.50, 0.00]
        elif color in ["c", "cyan"]:    r, g, b = [0.00, 0.75, 0.75]
        elif color in ["m", "magenta"]: r, g, b = [0.75, 0.00, 0.75]
        elif color in ["y", "yellow"]:  r, g, b = [0.75, 0.75, 0.00]
        elif color in ["k", "black"]:   r, g, b = [0.00, 0.00, 0.00]
        elif color in ["w", "white"]:   r, g, b = [1.00, 1.00, 1.00]
        else:                           raise Exception("Unrecognized input to gen_cmap(): {0}".format(color))
    else: r, g, b = color
    cdict   = {"red": ((0, r, r), (1, r, r)), "green": ((0, g, g), (1, g, g)), "blue": ((0, b, b), (1, b, b))}
    return    cl.LinearSegmentedColormap("cmap", cdict, 256)

def quick_figure_subplots(nrows = 1, ncols = 1, verbose = True, **kwargs):
    """
    Generates a figure and subplots to specifications

    Differs from matplotlib's built-in functions in that it:
        - Supports input in inches rather that relative figure coordinates
        - Calculates figure dimensions from provided subplot dimensions, rather than the reverse
        - Returns subplots in an OrderedDict

    **Arguments:**
        :*nrows*:      Number of rows of subplots
        :*ncols*:      Number of columns of subplots
        :*sub_width*:  Width of subplot(s)
        :*sub_height*: Height of subplot(s)
        :*top*:        Distance between top of figure and highest subplot(s)
        :*bottom*:     Distance between bottom of figure and lowest subplot(s)
        :*right*:      Distance between right side of figure and rightmost subplot(s)
        :*left*:       Distance between left side of figure and leftmost subplots(s)
        :*hspace*:     Vertical distance between adjacent subplots
        :*wspace*:     Horizontal distance between adjacent subplots
        :*fig_width*:  Width of figure; by default calculated from above arguments
        :*fig_height*: Height of figure, by default calculated from above arguments
 
    **Returns:**
        :*figure*:   <matplotlib.figure.Figure>
        :*subplots*: OrderedDict of subplots (1-indexed)

    .. todo:
        - More intelligent default dimensions based on *nrows* and *ncols*
        - Support centimeters?
    """

    # Parse arguments
    sub_width  = kwargs.get("sub_width",  6.00)
    sub_height = kwargs.get("sub_height", 2.00)
    top        = kwargs.get("top",        0.20)
    bottom     = kwargs.get("bottom",     0.40)
    right      = kwargs.get("right",      0.20)
    left       = kwargs.get("left",       0.40)
    hspace     = kwargs.get("hspace",     0.20)
    wspace     = kwargs.get("wspace",     0.20)
    fig_width  = kwargs.get("fig_width",  left + (sub_width  * ncols) + (wspace * (ncols - 1)) + right)
    fig_height = kwargs.get("fig_height", top  + (sub_height * nrows) + (hspace * (nrows - 1)) + bottom)

    # Convert subplot dimensions from absolute inches to relative figure coordinates
    subplot_kwargs = dict(left   = left                / fig_width,
                          bottom = bottom              / fig_height,
                          right  = (fig_width - right) / fig_width,
                          top    = (fig_height - top)  / fig_height,
                          wspace = wspace              / fig_width,
                          hspace = hspace              / fig_height)

    # Generate figure and subplots
    figure, subplots = plt.subplots(nrows, ncols, squeeze = True, figsize = [fig_width, fig_height],
                       subplot_kw = dict(autoscale_on = False))
    if   nrows * ncols == 1:
        subplots     = [subplots]
    elif min(nrows, ncols) > 1:
        subplots     = [subplot for inner in subplots for subplot in inner]
    subplots         = OrderedDict([(i, subplot) for i, subplot in enumerate(subplots, 1)])

    # Apply adjustments and return
    figure.subplots_adjust(**subplot_kwargs)
    if verbose:
        print("Figure is {0:6.3f} inches wide and {1:6.3f} tall".format(fig_width, fig_height))
    return figure, subplots

