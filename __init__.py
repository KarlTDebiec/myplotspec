#!/usr/bin/python
#   plot_toolkit.__init__.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-05-03
"""
General functions used for various tasks

..todo:
    - Consider moving some import statements to functions
    - Write wrapper or subclass of PdfPages that supports 'with' syntax
    - Do not force 'Agg' backend
"""
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys, types
import numpy as np
################################################## GENERAL FUNCTIONS ###################################################
def multi_kw(keywords, default, kwargs):
    """
    Function to allow arguments to be set by one of several potential keyword arguments. For example, the keyword
    argument *s* represeting a string might be set using *s*, *text*, *label*, or if none of these are present, a
    default value. Note that *kwargs* should not be passed to this function using the ** syntax.

    **Arguments:**
        :*keywords*: List of acceptable keyword arguments; first match is used and other are deleted
        :*default*:  Default value to use if none of *keywords* are present in *kwargs*
        :*kwargs*:   Dictionary of keyword arguments to be tested

    **Returns:**
        :*value*:    Value from *kwargs* of first matching keyword in *keywords*, or *default* if none are present
    """
    value = None
    for kw in [kw for kw in keywords if kw in kwargs]:
        if value is None:
            value = kwargs.pop(kw)
        else:
            del kwargs[kw]
    return default

def pad_zero(ticks, digits = None, **kwargs):
    """
    Returns a list of tick labels, each with the same number of digits after the decimal

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
        return ["{0:d}".format(tick) for tick in map(int, ticks)]
    else:
        return ["{0:.{1}f}".format(tick, digits) for tick in ticks]

################################################# MATPLOTLIB FUNCTIONS #################################################
def get_edges(figure, **kwargs):
    """
    **Arguments:**
        :*figure*:  <Figure> on which to act

    **Returns:**
        :*edges*:   Dictionary; keys are 'x' and 'y', values are numpy arrays with dimensions (axis, min...max)

    .. todo:
        - Should this instead return a numpy record array?
    """
    return {"x": np.array([[ax.get_position().xmin, ax.get_position().xmax] for ax in figure.axes]),
            "y": np.array([[ax.get_position().ymin, ax.get_position().ymax] for ax in figure.axes])}

def gen_font(fp = None, **kwargs):
    """
    **Arguments:**
        :*fp*:              Font settings

    **Behavior:**
        If *fp* is:
        | <FontProperties>: Act as a pass-through, return *fp* argument
        | String:           Make new <FontProperties> from string, '##L'; '##' = size; 'L' = {'r': regular, 'b' bold}
        | Dict:             Make new <FontProperties> using given keyword arguments

    **Returns:**
        :*fp*:  <FontProperties> object to given specifications
    """
    import matplotlib.font_manager

    if   isinstance(fp, matplotlib.font_manager.FontProperties):
        return fp
    elif isinstance(fp, types.StringTypes):
        if not "fname" in kwargs:
            kwargs["family"] = kwargs.get("family", "Arial")
        kwargs["size"]       = kwargs.get("size",   int(fp[:-1]))
        kwargs["weight"]     = kwargs.get("weight", {"r":"regular", "b":"bold"}[fp[-1]])
    elif isinstance(fp, types.DictType):
        kwargs.update(fp)
    return matplotlib.font_manager.FontProperties(**kwargs)

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
    import matplotlib.colors as cl
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

def gen_figure_subplots(nrows = 1, ncols = 1, verbose = True, **kwargs):
    """
    Generates a figure and subplots to specifications

    Differs from matplotlib's built-in functions in that it:
        - Accepts input in inches rather that relative figure coordinates
        - Calculates figure dimensions from provided subplot dimensions, rather than the reverse
        - Returns subplots in an OrderedDict
        - Smoothly adds additional subplots to a previously-generated figure (i.e. can be called multiple times)

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
        :*figure*:   <Figure>
        :*subplots*: OrderedDict of subplots (1-indexed)

    .. todo:
        - More intelligent default dimensions based on *nrows* and *ncols*
        - Support centimeters?
    """
    from collections import OrderedDict
    import matplotlib
    import matplotlib.pyplot as plt

    # Parse arguments
    nsubplots  = kwargs.get("nsubplots",  nrows * ncols)
    sub_width  = kwargs.get("sub_width",  1.00)
    sub_height = kwargs.get("sub_height", 1.00)
    top        = kwargs.get("top",        0.20)
    bottom     = kwargs.get("bottom",     0.40)
    right      = kwargs.get("right",      0.20)
    left       = kwargs.get("left",       0.40)
    hspace     = kwargs.get("hspace",     0.20)
    wspace     = kwargs.get("wspace",     0.20)
    if "figure" in kwargs:
        figure     = kwargs.pop("figure")
        fig_height = figure.get_figheight()
        fig_width  = figure.get_figwidth()
    else:
        fig_width  = kwargs.get("fig_width",  left + (sub_width  * ncols) + (wspace * (ncols - 1)) + right)
        fig_height = kwargs.get("fig_height", top  + (sub_height * nrows) + (hspace * (nrows - 1)) + bottom)
        figure     = plt.figure(figsize = [fig_width, fig_height])
    if "subplots" in kwargs:
        subplots   = kwargs.pop("subplots")
        i          = max([i for i in subplots.keys() if str(i).isdigit()]) + 1
    else:
        subplots   = OrderedDict()
        i          = 1

    # Generate figure and subplots, or add to existing figure and subplots if provided
    i_max    = i + nsubplots
    for j in range(nrows - 1, -1, -1):
        for k in range(0, ncols, 1):
            subplots[i] = matplotlib.axes.Axes(figure, rect = [
              (left   + k * sub_width  + k * wspace) / fig_width,  # Left
              (bottom + j * sub_height + j * hspace) / fig_height, # Bottom
              sub_width  / fig_width,                              # Width
              sub_height / fig_height],                            # Height
              autoscale_on = False)
            figure.add_axes(subplots[i])
            i += 1
            if i >= i_max: break

    if verbose:
        print("Figure is {0:6.3f} inches wide and {1:6.3f} tall".format(figure.get_figwidth(), figure.get_figheight()))
    return figure, subplots

def identify(subplots, **kwargs):
    """
    Identifies index of each subplot with inset text

    :*Arguments*: OrderedDict of subplots

    """
    from .text import set_inset

    for i, subplot in subplots.items():
        set_inset(subplot, text = i, xpos = 0.5, ypos = 0.5, ha = "center", va = "center", **kwargs)


