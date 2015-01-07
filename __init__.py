#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.__init__.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec on 15-01-06
"""
General functions

.. todo:
    - Check types vs. six
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys, types
import six
import numpy
################################## FUNCTIONS ###################################
def get_yaml(input):
    """
    Generates an object provided from an input in one of three forms.

    If *input* is a dictionary, returns *input*; If *input* is a path
    to a file, loads object from *input* file using yaml and returns.
    If *input* is a string but not a path to a file, load object from
    *input* string using yaml and returns.

    **Argument:**
        :*input*: Input object, path to file, or yaml string

    **Returns:**
        :*object*: Object specified by input
    """
    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        import yaml

        if os.path.isfile(input):
            with file(input, "r") as infile:
                return yaml.load(infile)
        else:
            return yaml.load(input)
    else:
        raise TypeError("get_yaml does not understand input of type " +
          "{0}".format(type(input)))

def merge_dicts(dict1, dict2):
    """
    Recursively merges two dictionaries.

    **Arguments:**
        :*dict1*: First dictionary
        :*dict2*: Second dictionary; values for keys shared by both
                  dictionaries are drawn from *dict2*

    **Returns:**
        :*merged*: Merged dictionary
    """
    def merge(dict1, dict2):
        """
        Generator used to recursively merge two dictionaries

        **Arguments:**
            :*dict1*: First dictionary
            :*dict2*: Second dictionary; values for keys shared by both
                      dictionaries are drawn from *dict2*

        **Yields:**
            :*(key, value)*: Merged key value pair
        
        """
        for key in set(dict1.keys()).union(dict2.keys()):
            if key in dict1 and key in dict2:
                if  (isinstance(dict1[key], dict)
                and  isinstance(dict2[key], dict)):
                    yield (key, dict(merge(dict1[key], dict2[key])))
                else:
                    yield (key, dict2[key])
            elif key in dict1:
                yield (key, dict1[key])
            else:
                yield (key, dict2[key])

    return dict(merge(dict1, dict2))

def gen_color(color):
    """
    Generates a color

    **Arguments:**
        :*color*: May be a string "red", "blue", etc. corresponding to
                  a default color; a string "pastel.red", "pastel.blue"
                  corresponding to a palette and color, a list of
                  three floating point numbers corresponding to red,
                  green, and blue values, or a single floating point
                  number corresponding to a grayscale color
    .. todo:
        - Support mode = {"RGB", "HSV", "HSB"} as argument
        - For RGB, HSV, or HSB values, if value is greater than 1
          divide by 255
    """
    colors = dict(
      default = dict(
        blue   = [0.298, 0.447, 0.690],
        green  = [0.333, 0.659, 0.408],
        red    = [0.769, 0.306, 0.321],
        purple = [0.506, 0.447, 0.698],
        yellow = [0.800, 0.725, 0.455],
        cyan   = [0.392, 0.710, 0.804]),
      pastel   = dict(
        blue   = [0.573, 0.776, 1.000],
        green  = [0.592, 0.941, 0.667],
        red    = [1.000, 0.624, 0.604],
        purple = [0.816, 0.733, 1.000],
        yellow = [1.000, 0.996, 0.639],
        cyan   = [0.690, 0.878, 0.902]),
      muted    = dict(
        blue   = [0.282, 0.471, 0.812],
        green  = [0.416, 0.800, 0.396],
        red    = [0.839, 0.373, 0.373],
        purple = [0.706, 0.486, 0.780],
        yellow = [0.769, 0.678, 0.400],
        cyan   = [0.467, 0.745, 0.859]),
      deep     = dict(
        blue   = [0.298, 0.447, 0.690],
        green  = [0.333, 0.659, 0.408],
        red    = [0.769, 0.306, 0.322],
        purple = [0.506, 0.447, 0.698],
        yellow = [0.800, 0.725, 0.455],
        cyan   = [0.392, 0.710, 0.804]),
      dark     = dict(
        blue   = [0.000, 0.110, 0.498],
        green  = [0.004, 0.459, 0.090],
        red    = [0.549, 0.035, 0.000],
        purple = [0.463, 0.000, 0.631],
        yellow = [0.722, 0.525, 0.043],
        cyan   = [0.000, 0.388, 0.455]))

    if isinstance(color, str):
        try:
            color = float(color)
            return [color, color, color]
        except:
            pass
        if "." in color:
            palette, color = color.split(".")
            return colors[palette][color]
        elif color in colors["default"]:
            return colors["default"][color]
        else:
            return color
    elif (isinstance(color, list)
    or    isinstance(color, numpy.ndarray)):
        return color
    elif   isinstance(color, float):
        return [color, color, color]

def multi_kw(keywords, default, kwargs):
    """
    Function to allow arguments to be set by one of several potential
    keyword arguments. For example, the keyword argument *s*
    represeting a string might be set using *s*, *text*, *label*, or if
    none of these are present, a default value. Note that *kwargs*
    should not be passed to this function using the ** syntax.

    **Arguments:**
        :*keywords*: List of acceptable keyword arguments in order of
                     priority; first match is used and other are deleted
        :*default*:  Default value to use if none of *keywords* are
                     present in *kwargs*
        :*kwargs*:   Dictionary of keyword arguments to be tested

    **Returns:**
        :*value*:    Value from *kwargs* of first matching keyword in
                     *keywords*, or *default* if none are present
    """
    value = None
    for kw in [kw for kw in keywords if kw in kwargs]:
        if value is None:
            value = kwargs.pop(kw)
        else:
            del kwargs[kw]
    if value is not None:
        return value
    else:
        return default
    # edited

def pad_zero(ticks, digits = None, **kwargs):
    """
    Returns a list of tick labels, each with the same number of digits
    after the decimal

    **Arguments:**
        :*ticks*:       List or numpy array of ticks
        :*digits*:      Number of digits to include after the decimal

    **Returns:**
        :*tick_labels*: Tick labels, each with the same number of
                        digits after the decimal
    """
    # If the number of digits to include has not been specified, use the
    #   largest number of digits in the provided ticks
    if digits is None:
        digits = 0
        for tick in ticks:
            if '.' in str(tick):
                digits = max(digits, len(str(tick).split('.')[1]))
    if digits  == 0:
        return ["{0:d}".format(tick) for tick in map(int, ticks)]
    else:
    
        return ["{0:.{1}f}".format(tick, digits) for tick in ticks]

############################# MATPLOTLIB FUNCTIONS #############################
def get_edges(figure_or_subplots, **kwargs):
    """
    **Arguments:**
        :*figure_or_subplots*: <Figure> of dictionary of <Axes> on which
                               to act

    **Returns:**
        :*edges*: Dictionary; keys are 'x' and 'y', values are numpy
                  arrays with dimensions (axis, min...max)

    .. todo:
        - Should this instead return a numpy record array instead?
          Format seems strange
    """
    import matplotlib

    if   isinstance(figure_or_subplots, matplotlib.figure.Figure):
        subplots = figure_or_subplots.axes
    elif isinstance(figure_or_subplots, types.DictType):
        subplots = figure_or_subplots.values()
    return {"x": numpy.array([[subplot.get_position().xmin,
                 subplot.get_position().xmax] for subplot in subplots]),
            "y": numpy.array([[subplot.get_position().ymin,
                 subplot.get_position().ymax] for subplot in subplots])}

def gen_font(fp = None, **kwargs):
    """
    **Arguments:**
        :*fp*: Font properties

    **Behavior:**
        | If *fp* is <FontProperties>, acts as a pass-through, returns
        |   *fp* argument
        | If *fp* is a String of form '##L', makes new <FontProperties>
        |   object for which '##' = size; 'L' = {'r': regular,
        |   'b' bold}
        | If *fp* is a Dict, makes new <FontProperties> using given
        |    keyword arguments

    **Returns:**
        :*fp*: <FontProperties> object to given specifications
    """
    import matplotlib.font_manager

    if   isinstance(fp, matplotlib.font_manager.FontProperties):
        return fp
    elif isinstance(fp, six.types.StringTypes):
        if not "fname" in kwargs:
            kwargs["family"] = kwargs.get("family", "Arial")
        kwargs["size"]       = kwargs.get("size",   int(fp[:-1]))
        kwargs["weight"]     = kwargs.get("weight", {"r":"regular",
            "b":"bold"}[fp[-1]])
    elif isinstance(fp, dict):
        kwargs.update(fp)
    return matplotlib.font_manager.FontProperties(**kwargs)

def gen_figure_subplots(nrows = 1, ncols = 1, verbose = False, **kwargs):
    """
    Generates a figure and subplots to specifications

    Differs from matplotlib's built-in functions in that it:
        - Accepts input in inches rather that relative figure
          coordinates
        - Optionally calculates figure dimensions from provided subplot
          dimensions, rather than the reverse
        - Returns subplots in an OrderedDict
        - Smoothly adds additional subplots to a previously-generated
          figure (i.e. can be called multiple times)

    **Arguments:**
        :*nrows*:      Number of rows of subplots
        :*ncols*:      Number of columns of subplots
        :*sub_width*:  Width of subplot(s)
        :*sub_height*: Height of subplot(s)
        :*top*:        Distance between top of figure and highest
                       subplot
        :*bottom*:     Distance between bottom of figure and lowest
                       subplot
        :*right*:      Distance between right side of figure and
                       rightmost subplot
        :*left*:       Distance between left side of figure and
                       leftmost subplots
        :*hspace*:     Vertical distance between adjacent subplots
        :*wspace*:     Horizontal distance between adjacent subplots
        :*fig_width*:  Width of figure; by default calculated from
                       above arguments
        :*fig_height*: Height of figure, by default calculated from
                       above arguments
 
    **Returns:**
        :*figure*:   <Figure>
        :*subplots*: OrderedDict of subplots

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
        fig_width  = kwargs.get("fig_width",
          left + (sub_width  * ncols) + (wspace * (ncols - 1)) + right)
        fig_height = kwargs.get("fig_height",
           top  + (sub_height * nrows) + (hspace * (nrows - 1)) + bottom)
        figure     = plt.figure(figsize = [fig_width, fig_height])
    if "subplots" in kwargs:
        subplots   = kwargs.pop("subplots")
        if len(subplots) == 0:
            i = 0
        else:
            i = max([i for i in subplots.keys() if str(i).isdigit()]) + 1
    else:
        subplots = OrderedDict()
        i        = 0
    # Generate figure and subplots, or add to existing figure and
    #   subplots if provided
    i_max    = i + nsubplots
    breaking = False
    for j in range(nrows - 1, -1, -1):
        if breaking: break
        for k in range(0, ncols, 1):
            subplots[i] = matplotlib.axes.Axes(figure, rect = [
              (left   + k * sub_width  + k * wspace) / fig_width,  # Left
              (bottom + j * sub_height + j * hspace) / fig_height, # Bottom
              sub_width  / fig_width,                              # Width
              sub_height / fig_height],                            # Height
              autoscale_on = False)
            figure.add_axes(subplots[i])
            i += 1
            if i >= i_max:
                breaking = True
                break

    if verbose:
        print("Figure is {0:6.3f} inches wide and {1:6.3f} tall".format(
          figure.get_figwidth(), figure.get_figheight()))
    return figure, subplots

def identify(subplots, **kwargs):
    """
    Identifies index of each subplot with inset text

    **Arguments:**
        :*subplots*: OrderedDict of subplots

    """
    from .text import set_inset

    for i, subplot in subplots.items():
        set_inset(subplot, text = i, xpos = 0.5, ypos = 0.5, ha = "center",
          va = "center", **kwargs)


