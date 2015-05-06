# -*- coding: utf-8 -*-
#   myplotspec.__init__.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
General functions.

.. todo:
  - Decide how to manage the specification of sizes, positions, etc. in
    real-world units (inches or centimeters)
  - Support setting rcParams in YAML file
  - Check compatibility with seaborn
  - Consider supporting figure and subplot specs as lists rather than
    exclusively an integer indexed dictionary
  - Make 'debug' and 'verbose' more useful
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## VARIABLES ##################################
FP_KEYS = ["fp", "font_properties", "fontproperties", "prop"]
################################## FUNCTIONS ##################################
def get_yaml(input):
    """
    Generates a data structure from YAML input.

    If ``input`` is a string, tests whether or not it is a path to a YAML file.
    If it is, the file is loaded using yaml; if it is not, the string itself is
    loaded using YAML. If ``input`` is a dict, it is returned without
    modification.

    Arguments:
      input (str, dict): YAML input

    Returns:
      (*dict*): Data structure specified by input

    Raises:
      TypeError: Input file type not understood.
    """
    import six

    if six.PY2:
        open_yaml = file
    else:
        open_yaml = open

    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        from os.path import isfile
        import yaml

        if isfile(input):
            with open_yaml(input, "r") as infile:
                return yaml.load(infile)
        else:
            output = yaml.load(input)
            if isinstance(output, six.string_types):
                raise OSError("yaml has loaded a simple string: "
                  "'{0}'; ".format(input) +
                  "if this was intended as an infile, it was not found; "
                  "input to get_yaml() function may be a path to a yaml "
                  "file, a string containing yaml-format data, or a "
                  "dict")
            return output
    else:
        raise TypeError("get_yaml does not understand input of type " +
          "{0}".format(type(input)))

def merge_dicts(dict_1, dict_2):
    """
    Recursively merges two dictionaries.

    Arguments:
      dict_1 (dict): First dictionary
      dict_2 (dict): Second dictionary; values for keys shared by both
        dictionaries are drawn from dict_2

    Returns:
      (*dict*): Merged dictionary
    """
    def merge(dict_1, dict_2):
        """
        Generator used to recursively merge two dictionaries

        Arguments:
          dict_1 (dict): First dictionary
          dict_2 (dict): Second dictionary; values for keys shared by
            both dictionaries are drawn from dict_2

        Yields:
          (*tuple*): Merged (key, value) pair

        """
        for key in set(dict_1.keys()).union(dict_2.keys()):
            if key in dict_1 and key in dict_2:
                if (isinstance(dict_1[key], dict)
                and isinstance(dict_2[key], dict)):
                    yield (key, dict(merge(dict_1[key], dict_2[key])))
                else:
                    yield (key, dict_2[key])
            elif key in dict_1:
                yield (key, dict_1[key])
            else:
                yield (key, dict_2[key])

    return dict(merge(dict_1, dict_2))

def get_color(color):
    """
    Generates a color.

    If color is a str, may be of form 'pastel.red', 'dark.blue', etc.
    corresponding to a color set and color; if no set is specified the
    'default' set is used. If list or ndarray, should contain three floating
    point numbers corresponding to red, green, and blue values If float, should
    correspond to a grayscale shade.

    Arguments:
      color (str, list, ndarray, float): color

    Returns:
      (*list*): [red, green, blue] on interval 0.0-1.0

    .. todo:
        - Useful error messages
        - Support dict format to specify mode,
          e.g.: get_color(color = {RGB: [0.1, 0.2, 0.3]})
        - For RGB, HSL, or alues, if values are greater than 1 divide by
          255
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
    elif isinstance(color, float):
        return [color, color, color]

def multi_kw(keys, dictionary):
    """
    Scans dict for keys; returns first value and deletes others.

    Arguments:
      keys (list): Acceptable keys in order of decreasing priority
      dictionary (dict): dict to be tested

    Returns:
      Value from first matching key; or None if not found
    """
    value = None
    for key in [key for key in keys if key in dictionary]:
        if value is None:
            value = dictionary.pop(key)
        else:
            del dictionary[key]
    return value

def pad_zero(ticks, digits=None, **kwargs):
    """
    Prepares list of tick labels, each with the same precision.

    Arguments:
      ticks (list, ndarray): ticks
      digits (int, optional): Precision; by default uses largest provided

    Returns:
      (*list*): Tick labels, each with the same number of digits after the
        decimal
    """
    if digits is None:
        digits = 0
        for tick in ticks:
            if '.' in str(tick):
                digits = max(digits, len(str(tick).split('.')[1]))
    if digits == 0:
        return ["{0:d}".format(tick) for tick in map(int, ticks)]
    else:

        return ["{0:.{1}f}".format(tick, digits) for tick in ticks]

def get_edges(figure_or_subplots, **kwargs):
    """
    Finds the outermost edges of a set of subplots on a figure.

    Arguments:
      figure_or_subplots (Figure, list, dict): Axes whose edges to
        get; if Figure, use all Axes

    Returns:
      (*dict*): Edges; keys are 'left', 'right', 'top', and 'bottom'
    """
    import matplotlib

    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        subplots = figure_or_subplots.axes
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots.values()
    return dict(
      left   = min([subplot.get_position().xmin for subplot in subplots]),
      right  = max([subplot.get_position().xmax for subplot in subplots]),
      top    = max([subplot.get_position().ymax for subplot in subplots]),
      bottom = min([subplot.get_position().ymin for subplot in subplots]))

def get_font(fp=None, **kwargs):
    """
    Generates font based on provided specification.

    fp may be a string of form '##L' in which '##' is the font size and L
    is 'r' for regular or 'b' for bold. fp may also be a dict of keyword
    arguments to pass to FontProperties. fp may also be a
    FontProperties, in which case it is returned without modification

    Arguments:
        fp (str, dict, FontProperties): Font specifications

    Returns:
        (*FontProperties*): Font with given specifications
    """
    import six
    from matplotlib.font_manager import FontProperties

    if isinstance(fp, FontProperties):
        return fp
    elif isinstance(fp, six.string_types):
        kwargs["size"] = kwargs.get("size", int(fp[:-1]))
        kwargs["weight"] = kwargs.get("weight", {"r":"regular",
            "b":"bold"}[fp[-1]])
    elif isinstance(fp, dict):
        kwargs.update(fp)
    else:
        raise TypeError("get_font does not understand input of type " +
          "{0}".format(type(fp)))
    return FontProperties(**kwargs)

def get_figure_subplots(figure=None, subplots=None, nrows=None,
    ncols=None, nsubplots=None, left=None, sub_width=None, wspace=None,
    right=None, bottom=None, sub_height=None, hspace=None, top=None,
    fig_width=None, fig_height=None, figsize=None, verbose=False,
    debug=False, **kwargs):
    """
    Generates a figure and subplots to provided specifications.

    Differs from matplotlib's built-in functions in that it:
      - Accepts subplot dimensions is inches rather than proportional
        figure coordinates
      - Optionally calculates figure dimensions from provided subplot
        dimensions, rather than the reverse
      - Returns subplots in an OrderedDict
      - Smoothly adds additional subplots to a previously-generated
        figure (i.e. can be called multiple times)

    Arguments:
      figure (Figure, optional): Figure, if adding subplots to a preexisting
        Figure
      subplots (OrderedDict, optional): Subplots, if adding subplots to a
        prevexisting Figure
      nrows (int): Number of rows of subplots to add
      ncols (int): Number of columns of subplots to add
      nsubplots (int, optional): Number of subplots to add; if less than
        nrows*ncols (e.g. 2 cols and 2 rows but only three subplots)
      sub_width (float): Width of subplot(s)
      sub_height (float): Height of subplot(s)
      left (float): Margin between left side of figure and leftmost
        subplot
      right (float): Margin between right side of figure and rightmost
        subplot
      top (float): Margin between top of figure and topmost subplot
      bottom (float): Margin between bottom of figure and bottommost
        subplot
      wspace (float): Horizontal margin between adjacent subplots
      hspace (float): Vertical margin between adjacent subplots
      fig_width (float): Width of figure; by default calculated from
        left, sub_width, wspace, right, and ncols
      fig_height (float): Height of figure, by default calculated from
        bottom, sub_height, hspace, top, and nrows
      figsize (list): Equivalent to [``fig_width``, ``fig_height``]
      figure_kw (dict): Additional keyword arguments passed to figure()
      subplot_kw (dict): Additional keyword arguments passed to Axes()
      axes_kw (dict): Alias to ``subplot_kw``
      verbose (bool): Enable verbose output
      debug (bool): Enable debug output

    Returns:
      (*Figure*, *OrderedDict*): Figure and subplots

    """
    from collections import OrderedDict
    import matplotlib
    import matplotlib.pyplot as pyplot
    from . import multi_kw

    # Manage margins
    if ncols is None:
        ncols = 1
    if left is None:
        left = matplotlib.rcParams["figure.subplot.left"]
    if wspace is None:
        wspace = matplotlib.rcParams["figure.subplot.wspace"]
    if right is None:
        right = matplotlib.rcParams["figure.subplot.right"]
    if nrows is None:
        nrows = 1
    if top is None:
        top = matplotlib.rcParams["figure.subplot.top"]
    if hspace is None:
        hspace = matplotlib.rcParams["figure.subplot.hspace"]
    if bottom is None:
        bottom = matplotlib.rcParams["figure.subplot.bottom"]

    # Manage figure and subplot dimensions
    if figure is not None:
        fig_height = figure.get_figheight()
        fig_width = figure.get_figwidth()
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
            sub_width = fig_width - left - (wspace * (ncols - 1)) - right
        if sub_height is None:
            sub_height = fig_height - top - (hspace * (nrows - 1)) - bottom
    elif      ((sub_width is None or sub_height is None)
    and   not ((fig_width is None or fig_height is None) and figsize is None)):
        # Lack sublot dimensions, but have figure dimensions
        if figsize is not None:
            fig_width, fig_height = figsize
        figsize = [fig_width, fig_height]
        if sub_width is None:
            sub_width = fig_width - left - (wspace * (ncols - 1)) - right
        if sub_height is None:
            sub_height = fig_height - top  - (hspace * (nrows - 1)) - bottom
    elif (not (sub_width is None or sub_height is None)
    and      ((fig_width is None or fig_height is None) and figsize is None)):
        # Have subplot dimensions, but lack figure dimensions
        if fig_width is None:
            fig_width = left+(sub_width*ncols)+(wspace*(ncols-1))+right
        if fig_height is None:
            fig_height = top+(sub_height*nrows)+(hspace*(nrows-1))+bottom
        figsize = [fig_width, fig_height]
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
    i_max = i + nsubplots
    breaking = False
    for j in range(nrows - 1, -1, -1):
        if breaking:
            break
        for k in range(0, ncols, 1):
            subplots[i] = matplotlib.axes.Axes(figure, rect = [
              (left + k * sub_width + k * wspace) / fig_width,      # Left
              (bottom + j * sub_height + j * hspace) / fig_height,  # Bottom
              sub_width / fig_width,                                # Width
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
