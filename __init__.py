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
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## VARIABLES ##################################
FP_KEYS = ["fp", "font_properties", "fontproperties", "prop"]
################################## FUNCTIONS ##################################
def get_yaml(input):
    """
    Generates a data structure from yaml input. 

    Arguments:
      input (str, dict): yaml input; if str, tests whether or not it is
        a path to a yaml file. If it is, the file is loaded using yaml;
        if it is not a file, the string itself is loaded using yaml. If
        dict, returned without modification

    Returns:
      output: Data structure specified by input

    Warns:
      UserWarning: Loaded data structure is a string; occurs if input
        file is a path to a yaml file that is not found

    Raises:
      TypeError: Input is not str or dict

    .. todo:
      - Should this bounce back other input types (e.g. list) as it does
        dict?
    """
    from os.path import isfile
    from warnings import warn
    import yaml
    import six

    if six.PY2:
        open_yaml = file
    else:
        open_yaml = open

    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        if isfile(input):
            with open_yaml(input, "r") as infile:
                return yaml.load(infile)
        else:
            output = yaml.load(input)
            if isinstance(output, str):
                warn("myplotspec.get_yaml() has loaded input "
                "'{0}' as a string rather than a dictionary ".format(input) +
                "or other data structure; if input was intended as an infile "
                "it was not found.")
            return output
    else:
        raise TypeError("myplotspec.get_yaml() does not support input of type "
          "{0}; ".format(input.__class__.__name__) +
          "input may be a string path to a yaml file, a yaml-format string, "
          "or a dictionary.")

def merge_dicts(dict_1, dict_2):
    """
    Recursively merges two dictionaries.

    Arguments:
      dict_1 (dict): First dictionary
      dict_2 (dict): Second dictionary; values for keys shared by both
        dictionaries are drawn from dict_2

    Returns:
      (dict): Merged dictionary

    .. todo:
      - Consider options to override, concatenate, or merge list
        values within dictionaries
    """
    def merge(dict_1, dict_2):
        """
        Generator used to recursively merge two dictionaries

        Arguments:
          dict_1 (dict): First dictionary
          dict_2 (dict): Second dictionary; values for keys shared by
            both dictionaries are drawn from dict_2

        Yields:
          (tuple): Merged (key, value) pair
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
    'default' set is used. If list or ndarray, should contain three
    floating point numbers corresponding to red, green, and blue values.
    If these numbers are greater than 1, they will be divided by 255. If
    float, should correspond to a grayscale shade, if greater than 1
    will be divided by 255.

    Arguments:
      color (str, list, ndarray, float): color

    Returns:
      (list): [red, green, blue] on interval 0.0-1.0

    .. todo:
        - Useful error messages
        - Support dict format to specify mode,
          e.g.: get_color(color = {RGB: [0.1, 0.2, 0.3]})
        - Probably just use seaborn now that it is known to be
          compatible and easy to use
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
        color = np.array(color, dtype=np.float)
        if np.any(color[0] > 1):
            color /= 255
        return color
    elif isinstance(color, float):
        if color > 1:
            color /= 255
        return [color, color, color]

def multi_kw(keys, dictionary, value=None):
    """
    Scans dict for keys; returns first value and deletes others.

    Arguments:
      keys (list): Acceptable keys in order of decreasing priority
      dictionary (dict): dict to be tested
      value: Default to be returned if not found

    Returns:
      value: Value from first matching key; or None if not found
    """
    found = False
    for key in [key for key in keys if key in dictionary]:
        if not found:
            value = dictionary.pop(key)
            found = True
        else:
            del dictionary[key]
    return value

def multi_get(*args, **kwargs):
    """
    Scans dict for keys; returns first value.

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested
      value: Default to be returned if not found

    Returns:
      value: Value from first matching key; or None if not found
    """
    return _multi_get_pop(pop=False, *args, **kwargs)

def multi_get_copy(*args, **kwargs):
    """
    Scans dict for keys; returns copy of first value.

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested
      value: Default to be returned if not found

    Returns:
      value: Value from first matching key; or None if not found
    """
    return _multi_get_pop(pop=False, copy=True, *args, **kwargs)

def multi_pop(*args, **kwargs):
    """
    Scans dict for keys; returns first value and deletes others.

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested
      value: Default to be returned if not found

    Returns:
      value: Value from first matching key; or None if not found
    """
    return _multi_get_pop(pop=True, *args, **kwargs)

def _multi_get_pop(keys, dictionary, value=None, pop=False, copy=False):
    """
    Scans dict for keys; returns first value or a copy of first value,
    and optionally deletes others.

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested
      value: Default to be returned if not found
      pop (bool): Delete all matching *keys* from *dictionary*; may not
        be used with *copy*
      copy (bool): Return copy of value; may not be used with *pop*

    Returns:
      value: Value from first matching key; or None if not found

    .. todo:
      - Error messages
      - Smoothly support optional plurality
      - Support merging of dict or list values
    """
    from copy import deepcopy
    import six

    if isinstance(keys, six.string_types):
        keys = [keys]
    elif not hasattr(keys, "__iter__"):
        raise TypeError()

    if not isinstance(dictionary, dict):
        raise TypeError()

    if pop and copy:
        raise TypeError()

    found = False
    for key in [key for key in keys if key in dictionary]:
        if not found:
            if copy:
                value = deepcopy(dictionary.get(key))
            else:
                value = dictionary.get(key)
            found = True
        if pop:
            del dictionary[key]
    return value

def pad_zero(ticks, digits=None, **kwargs):
    """
    Prepares list of tick labels, each with the same precision.

    Arguments:
      ticks (list, ndarray): ticks
      digits (int, optional): Precision; by default uses largest
        provided

    Returns:
      (list): Tick labels, each with the same number of digits after
        the decimal point
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
      (dict): Edges; keys are 'left', 'right', 'top', and 'bottom'

    .. todo:
      - What are the units here? Probably relative but should be
        documented or possible an option
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

    *fp* may be a string of form '##L' in which '##' is the font size
    and L is 'r' for regular or 'b' for bold. fp may also be a dict of
    keyword arguments to pass to FontProperties. *fp* may also be a
    FontProperties, in which case it is returned without modification.

    Arguments:
        fp (str, dict, FontProperties): Font specifications

    Returns:
        (FontProperties): Font with given specifications
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
    fig_width=None, fig_height=None, figsize=None, verbose=1,
    debug=0, **kwargs):
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
      verbose (int): Level of verbose output
      debug (int): Level of debug output
      kwargs (dict): Additional keyword arguments

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
        nsubplots = nrows * ncols
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

    if verbose >= 1:
        print("Figure is {0:6.3f} inches wide and {1:6.3f} tall".format(
          figure.get_figwidth(), figure.get_figheight()))
    return figure, subplots

################################### CLASSES ###################################
class OrderedSet(object):
    """
    """
    def __init__(self, iterable=None):
        self.items = []
        if iterable is not None:
            for item in iterable:
                if item not in self.items:
                    self.items.append(item)
    def __len__(self):
        return len(self.items)
    def __contains__(self, key):
        return key in self.items
    def __getitem__(self, index):
        """
        .. todo:
          - implement slicing
        """
        import six

        if not isinstance(index, six.integer_types):
            raise TypeError("OrderedSet index must be integer, "
              "not {0}".format(index.__class__.__name__))
        if index < len(self.items):
            return self.items[index]
        else:
            raise IndexError("OrderedSet index out of range")
    def __repr__(self):
        if not self:
            return "{0}()".format(self.__class__.__name__)
        return "{0}({1})".format(self.__class__.__name__, list(self))
    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def add(self, key):
        if key not in self.items:
            self.items.append(key)

    def append(self, key):
        if key in self.items:
            self.items.remove(key)
        if key not in self.items:
            self.items.append(key)

    def insert(self, index, key):
        if key in self.items:
            self.items.remove(key)
        self.items.insert(index,key)

    def remove(self, key):
        if key in self.items:
            self.items.remove(key)
        else:
            raise ValueError("OrderedSet.remove(x): x not in OrderedSet")

    def index(self, key):
        if key in self.items:
            return self.items.index(key)
        else:
            raise ValueError("{0} is not in OrderedSet".format(key))

    def pop(self, index=None):
        import six

        if len(self.items) == 0:
            raise KeyError("pop from an empty OrderedSet")
        elif not (isinstance(index, six.integer_types) or index is None):
            raise TypeError("OrderedSet index must be integer, "
              "not {0}".format(index.__class__.__name__))
        if index is None:
            index = len(self.items) - 1

        if index < len(self.items):
            return self.items.pop(index)
        else:
            raise IndexError("OrderedSet index out of range")
