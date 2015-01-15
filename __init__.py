#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.__init__.py
#   Written:    Karl Debiec     12-10-22
#   Updated:    Karl Debiec     15-01-12
"""
General functions
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
import six
if six.PY2:
    open_yaml = file
else:
    open_yaml = open
################################## VARIABLES ##################################
fp_keys = ["fp", "font_properties", "fontproperties", "prop"]
################################## FUNCTIONS ##################################
def get_yaml(input):
    """
    Generates an object provided from an input in one of three forms.

    If *input* is a dictionary, returns *input*; If *input* is a path to
    a file, loads object from *input* file using yaml and returns.  If
    *input* is a string but not a path to a file, load object from
    *input* string using yaml and returns.

    **Argument:**
        :*input*: Input object, path to file, or yaml string

    **Returns:**
        :*object*: Object specified by input
    """
    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        from os.path import isfile
        import yaml

        if isfile(input):
            with open_yaml(input, "r") as infile:
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

def get_color(color):
    """
    Generates a color

    **Arguments:**
        :*color*: May be a string "red", "blue", etc. corresponding to
                  a default color; a string "pastel.red", "pastel.blue"
                  corresponding to a palette and color, a list of three
                  floating point numbers corresponding to red, green,
                  and blue values, or a single floating point number
                  corresponding to a grayscale color

    .. todo:
        - Support mode = {"RGB", "HSV", "HSB"} as argument
        - For RGB, HSV, or HSB values, if value is greater than 1
          divide by 255

    """
    import numpy as np

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
    or    isinstance(color, np.ndarray)):
        return color
    elif   isinstance(color, float):
        return [color, color, color]

def multi_kw(keys, dictionary):
    """
    Scans *dictionary* for *keys*, returns first matching value (or None
    if none are present), and deletes *keys* from *dictionary*

    This is not really ideal, but is appropriate here due to the
    inconsistency of the names of some of matplotlib's arguments, in
    particular fontproperties, font_properties, fp, and sometimes prop.

    **Arguments:**
        :*keys*:       List of acceptable keyword arguments in order of
                       priority; first match is used and other are
                       deleted
        :*dictionary*: Dictionary of keyword arguments to be tested
        :*default*:    Value to return if not found

    **Returns:**
        :*value*: Value from *dictionary* of first matching keyword in
                  *keys*, or None if none are present

    """
    value = None
    for key in [key for key in keys if key in dictionary]:
        if value is None:
            value = dictionary.pop(key)
        else:
            del dictionary[key]
    return value

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

def get_edges(figure_or_subplots, **kwargs):
    """
    Finds the outermost edges of a set of subplots on a figure

    **Arguments:**
        :*figure_or_subplots*: <Figure> or list or dictionary of <Axes>
                               on which to act

    **Returns:**
        :*edges*: dictionary of edges; keys are 'left', 'right', 'top',
                  and 'bottom'
    """
    import matplotlib

    if   isinstance(figure_or_subplots, matplotlib.figure.Figure):
        subplots = figure_or_subplots.axes
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots.values()
    return dict(
      left   = min([subplot.get_position().xmin for subplot in subplots]),
      right  = max([subplot.get_position().xmax for subplot in subplots]),
      top    = max([subplot.get_position().ymax for subplot in subplots]),
      bottom = min([subplot.get_position().ymin for subplot in subplots]))

def get_font(fp = None, **kwargs):
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
    elif isinstance(fp, six.string_types):
        kwargs["size"]       = kwargs.get("size",   int(fp[:-1]))
        kwargs["weight"]     = kwargs.get("weight", {"r":"regular",
            "b":"bold"}[fp[-1]])
    elif isinstance(fp, dict):
        kwargs.update(fp)
    return matplotlib.font_manager.FontProperties(**kwargs)

def get_figure_subplots(figure = None, subplots = None, nrows = None,
    ncols = None, nsubplots = None, left = None, sub_width = None,
    wspace = None, right = None, top = None, sub_height = None, hspace = None,
    bottom = None, fig_width = None, fig_height = None, figsize = None,
    verbose = False, debug = False, **kwargs):
    """
    Generates a figure and subplots to specifications

    Differs from matplotlib's built-in functions in that it:
        - Accepts subplot dimensions is inches rather than proportional
          figure coordinates
        - Optionally calculates figure dimensions from provided subplot
          dimensions, rather than the reverse
        - Returns subplots in an OrderedDict
        - Smoothly adds additional subplots to a previously-generated
          figure (i.e. can be called multiple times)

    **Arguments:**
        :*figure*:     Figure, if adding subplots to a
                       previously-existing figure
        :*subplots*:   OrderedDict of subplots, if adding subplots to
                       a previously-existing figure
        :*nrows*:      Number of rows of subplots
        :*ncols*:      Number of columns of subplots
        :*nsubplots*:  Number of subplots to add; if less than
                       nrows*ncols (e.g. 2 cols and 2 rows but only
                       three subplots)
        :*sub_width*:  Width of subplot(s)
        :*sub_height*: Height of subplot(s)
        :*left*:       Margin between left side of figure and leftmost
                       subplots
        :*right*:      Margin between right side of figure and
                       rightmost subplot
        :*top*:        Margin between top of figure and highest subplot
        :*bottom*:     Margin between bottom of figure and lowest
                       subplot
        :*wspace*:     Horizontal margin between adjacent subplots
        :*hspace*:     Vertical margin between adjacent subplots
        :*fig_width*:  Width of figure; may be determined from above
        :*fig_height*: Height of figure, may be determined from above
        :*figsize*:    Equivalent to [fig_width, fig_height]
        :*figure_kw*:  Keyword arguments passed to figure()
        :*subplot_kw*: Keyword arguments passed to Axes()
        :*axes_kw*:    Alias to subplot_kw
        :*verbose*:    Enable verbose output
        :*debug*:      Enable debug output

    **Returns:**
        :*figure*:   <Figure>
        :*subplots*: OrderedDict of subplots
    """
    from collections import OrderedDict
    import matplotlib 
    import matplotlib.pyplot as pyplot
    from . import multi_kw

    # Manage margins
    if ncols  is None:  ncols  = 1
    if left   is None:  left   = matplotlib.rcParams["figure.subplot.left"]
    if wspace is None:  wspace = matplotlib.rcParams["figure.subplot.wspace"]
    if right  is None:  right  = matplotlib.rcParams["figure.subplot.right"]
    if nrows  is None:  nrows  = 1
    if top    is None:  top    = matplotlib.rcParams["figure.subplot.top"]
    if hspace is None:  hspace = matplotlib.rcParams["figure.subplot.hspace"]
    if bottom is None:  bottom = matplotlib.rcParams["figure.subplot.bottom"]

    # Manage figure and subplot dimensions
    if figure is not None:
        fig_height = figure.get_figheight()
        fig_width  = figure.get_figwidth()
        figsize = [fig_width, fig_height]
    if  ((sub_width is None or sub_height is None)
    and ((fig_width is None or fig_height is None) and figsize is None)):
        # Lack subplot and figure dimensions
        figsize = matplotlib.rcParams["figure.figsize"]
        if fig_width is None:
            fig_width = figsize[0]
        if fig_height is None:
            fig_height = figsize[1]
        figsize = [fig_width, fig_height]
        if sub_width is None:
            sub_width  = fig_width  - left - (wspace * (ncols - 1)) - right
        if sub_height is None:
            sub_height = fig_height - top  - (hspace * (nrows - 1)) - bottom
    elif      ((sub_width is None or sub_height is None)
    and   not ((fig_width is None or fig_height is None) and figsize is None)):
        # Lack sublot dimensions, but have figure dimensions
        if figsize is not None:
            fig_width, fig_height = figsize
        figsize = [fig_width, fig_height]
        if sub_width is None:
            sub_width  = fig_width  - left - (wspace * (ncols - 1)) - right
        if sub_height is None:
            sub_height = fig_height - top  - (hspace * (nrows - 1)) - bottom
    elif (not (sub_width is None or sub_height is None)
    and      ((fig_width is None or fig_height is None) and figsize is None)):
        # Have subplot dimensions, but lack figure dimensions
        if fig_width is None:
            fig_width  = left+(sub_width*ncols)+(wspace*(ncols-1))+right
        if fig_height is None:
            fig_height = top+(sub_height*nrows)+(hspace*(nrows-1))+bottom
        figsize    = [fig_width, fig_height]
    elif (not  (sub_width is None or sub_height is None)
    and   not ((fig_width is None or fig_height is None) and figsize is None)):
        # Have subplot and figure dimensions
        figsize = [fig_width, fig_height]

    # Manage figure
    if figure is None:
        figure_kw = kwargs.get("figure_kw", {})
        figure = pyplot.figure(figsize = figsize, **figure_kw)

    # Manage subplots
    subplot_kw = kwargs.get("subplot_kw", kwargs.get("axes_kw", {}))
    if subplots is not None:
        if len(subplots) == 0:
            i = 0
        else:
            i = max([i for i in subplots.keys() if str(i).isdigit()]) + 1
    else:
        subplots = OrderedDict()
        i = 0

    # Generate figure and subplots, or add to existing figure and
    #   subplots if provided
    if nsubplots is None:
        nsubplots = ncols * nrows
    i_max    = i + nsubplots
    breaking = False
    for j in range(nrows - 1, -1, -1):
        if breaking:
            break
        for k in range(0, ncols, 1):
            subplots[i] = matplotlib.axes.Axes(figure, rect = [
              (left   + k * sub_width  + k * wspace) / fig_width,   # Left
              (bottom + j * sub_height + j * hspace) / fig_height,  # Bottom
              sub_width  / fig_width,                               # Width
              sub_height / fig_height],                             # Height
              **subplot_kw)
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
    Identifies key of each subplot with inset text

    **Arguments:**
        :*subplots*: OrderedDict of subplots

    """
    from .text import set_inset

    for i, subplot in subplots.items():
        set_inset(subplot, text = i, xpos = 0.5, ypos = 0.5, ha = "center",
          va = "center", **kwargs)
