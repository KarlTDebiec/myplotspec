# -*- coding: utf-8 -*-
#   myplotspec.__init__.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
General functions.

.. todo:
  - Implement multi_get_merged and multi_pop_merged
  - Is OrderedSet ever used?
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

################################## VARIABLES ##################################
FP_KEYS = ["fp", "font_properties", "fontproperties", "prop"]


################################## FUNCTIONS ##################################
def wiprint(text, width=80, subsequent_indent="  ", **kwargs):
    """
    Prints wrapped text.

    Arguments:
      text (str): Text to wrap
      width (int): Width of formatted text
      subsequent_indent (str): Text with which to prepend lines after
        the first
      kwargs (dict): Additional keyword arguments passed to
        :func:`TextWrapper`
    """
    import re
    from textwrap import TextWrapper

    tw = TextWrapper(width=width, subsequent_indent=subsequent_indent,
        **kwargs)
    print(tw.fill(re.sub(r"\s+", " ", text)))


def sformat(text, **kwargs):
    """
    Formats whitespace in text.

    Arguments:
      text (str): Text to format
    Returns:
      str: *text* with all whitespace replaced with single spaces
    """
    import re

    return (re.sub(r"\s+", " ", text))


def load_dataset(cls=None, dataset_cache=None, loose=False, **kwargs):
    """
    Loads a dataset, or reloads a previously-loaded dataset from a
    cache.

    Datasets are stored in `dataset_cache`, a dictionary containing
    copies of previously loaded datasets keyed by tuples containing
    the class and arguments used to instantiate the dataset.

    In order to support caching, a class must implement the static
    method :meth:`Dataset.Dataset.get_cache_key`, which generates the
    hashable tuple key. Only arguments that influence the resulting
    dataset should be included in the key (e.g. `infile` should be
    included, but `verbose` and `debug` should not). If the function
    accepts arguments that are not hashable or convertable into a
    hashable form, :meth:`Dataset.Dataset.get_cache_key` should return
    None, causing :func:`load_dataset` to reload the dataset.

    Cachable dataset classes may also implement the method
    :meth:`Dataset.Dataset.get_cache_message` which returns a message to
    display when the dataset is loaded from the cache.

    Arguments:
      cls (class, str): Dataset class; may be either class object itself
        or name of class in form of 'package.module.class'; if None,
        will be set to :class:`Dataset.Dataset`; if '__nocls_',
        function will return None
      dataset_cache (dict, optional): Cache of previously-loaded
        datasets
      loose (bool): Check only `infile` when reloading from cache; this
        may be used to reload a previously-loaded dataset without
        specifiying every argument every time.
      verbose (int): Level of verbose output
      kwargs (dict): Keyword arguments passed to
        :meth:`Dataset.Dataset.get_cache_key` and
        :meth:`Dataset.Dataset.cls`

    Returns:
      object: Dataset, either newly initialized or copied from cache

    .. todo:
      - Handling of errors remains extremely frustrating in python
        2.7; may not be worth bothering to improve
      - Understand copying better and select appropriate behavior
      - May be better to keep argument names in cache keys, so that dict
        may be recapitulated; this may help with 'loose'
    """
    from os.path import expandvars
    import six

    # Process arguments
    verbose = kwargs.get("verbose", 1)

    # Enable 'loose' loading of previously-loaded datasets using
    # infile path only
    if loose:
        if dataset_cache is not None:
            loose_keys = {key[1]: key for key in dataset_cache.keys()}
            infile = kwargs.get("infile")
            if infile is not None:
                if isinstance(infile, str):
                    infile = expandvars(infile)
                    if infile in loose_keys:
                        dataset = dataset_cache[loose_keys[infile]]
                        cls = type(dataset)
                        cache_key = cls.get_cache_key(**kwargs)
                        if hasattr(cls, "get_cache_message"):
                            wiprint(cls.get_cache_message(cache_key))
                        else:
                            wiprint("Previously loaded")
                        return dataset

    if cls == "__nocls_":
        return None
    if cls is None:
        from .Dataset import Dataset
        cls = Dataset
    elif isinstance(cls, six.string_types):
        mod_name = ".".join(cls.split(".")[:-1])
        clsname = cls.split(".")[-1]
        mod = __import__(mod_name, fromlist=[clsname])
        cls = getattr(mod, clsname)

    if dataset_cache is not None and hasattr(cls, "get_cache_key"):
        cache_key = cls.get_cache_key(**kwargs)
        if cache_key is None:
            return cls(dataset_cache=dataset_cache, **kwargs)
        if cache_key in dataset_cache:
            if verbose >= 1:
                if hasattr(cls, "get_cache_message"):
                    wiprint(cls.get_cache_message(cache_key))
                else:
                    wiprint("Previously loaded")
            return dataset_cache[cache_key]
        else:
            dataset_cache[cache_key] = cls(dataset_cache=dataset_cache,
                **kwargs)
            return dataset_cache[cache_key]
    else:
        return cls(**kwargs)


def get_cmap(color, **kwargs):
    """
    Generates a colormap of uniform `color`.

    Arguments:
      color (str, list, ndarray, float): Color; passed through
        :func:`get_color`

    Returns:
      LinearSegmentedColormap: Color map
    """
    from matplotlib.colors import LinearSegmentedColormap
    from . import get_color

    r, g, b = get_color(color)

    cdict = {"red": ((0, r, r), (1, r, r)), "green": ((0, g, g), (1, g, g)),
        "blue": ((0, b, b), (1, b, b))}
    return LinearSegmentedColormap("cmap", cdict, 256)


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
                     "'{0}' as a string rather than a dictionary ".format(
                    input) + "or other data structure; if input was intended "
                             "as an "
                             "infile it was not found.")
            return output
    elif input is None:
        warn("myplotspec.get_yaml() has been asked to load input 'None', and "
             "will return an empty dictionary.")
        return {}
    else:
        raise TypeError("myplotspec.get_yaml() does not support input of type "
                        "{0}; ".format(
            input.__class__.__name__) + "input may be a string path to a "
                                        "yaml file, a yaml-format string, "
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

    Raises:
      AttributeError: Either `dict_1` or `dict_2` lacks 'keys' function

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
                if (isinstance(dict_1[key], dict) and isinstance(dict_2[key],
                    dict)):
                    yield (key, dict(merge(dict_1[key], dict_2[key])))
                else:
                    yield (key, dict_2[key])
            elif key in dict_1:
                yield (key, dict_1[key])
            else:
                yield (key, dict_2[key])

    if not isinstance(dict_1, dict) or not isinstance(dict_2, dict):
        raise AttributeError(
            "Function myplotspec.merge_dict() requires " + "arguments "
                                                           "'dict_1' and "
                                                           "'dict_2' to be "
                                                           "dictionaries; "
            + "arguments of types " + "'{0}' and '{1}' provided".format(
                dict_1.__class__.__name__, dict_2.__class__.__name__))

    return dict(merge(dict_1, dict_2))


def get_color(color):
    """
    Converts color from a format understood by myplotspec to a format
    understood by matplotlib

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
        - Probably just use seaborn now that it is known to be
          compatible and easy to use
    """
    import numpy as np

    colors = dict(
        default=dict(black=[0.000, 0.000, 0.000], blue=[0.298, 0.447, 0.690],
            green=[0.333, 0.659, 0.408], red=[0.769, 0.306, 0.321],
            purple=[0.506, 0.447, 0.698], yellow=[0.800, 0.725, 0.455],
            cyan=[0.392, 0.710, 0.804]),
        pastel=dict(blue=[0.573, 0.776, 1.000], green=[0.592, 0.941, 0.667],
            red=[1.000, 0.624, 0.604], purple=[0.816, 0.733, 1.000],
            yellow=[1.000, 0.996, 0.639], cyan=[0.690, 0.878, 0.902]),
        muted=dict(blue=[0.282, 0.471, 0.812], green=[0.416, 0.800, 0.396],
            red=[0.839, 0.373, 0.373], purple=[0.706, 0.486, 0.780],
            yellow=[0.769, 0.678, 0.400], cyan=[0.467, 0.745, 0.859]),
        deep=dict(blue=[0.298, 0.447, 0.690], green=[0.333, 0.659, 0.408],
            red=[0.769, 0.306, 0.322], purple=[0.506, 0.447, 0.698],
            yellow=[0.800, 0.725, 0.455], cyan=[0.392, 0.710, 0.804]),
        dark=dict(blue=[0.000, 0.110, 0.498], green=[0.004, 0.459, 0.090],
            red=[0.549, 0.035, 0.000], purple=[0.463, 0.000, 0.631],
            yellow=[0.722, 0.525, 0.043], cyan=[0.000, 0.388, 0.455]))

    if isinstance(color, str):
        if color.startswith("#"):
            from matplotlib.colors import hex2color
            return hex2color(color)
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
    elif (isinstance(color, list) or isinstance(color,
        np.ndarray) or isinstance(color, tuple)):
        color = np.array(color, dtype=np.float)
        if np.any(color[0] > 1):
            color /= 255
        return tuple(color)
    elif isinstance(color, float):
        if color > 1:
            color /= 255
        return (color, color, color)


def get_colors(dict_1, *args, **kwargs):
    """
    Convers color variables in a dict from formats understood by
    myplotspec to formats understood by matplotlib

    This function is intended to process dictionaries of keyword
    arguments including colors  before passing them on to matplotlib's
    plotting functions. 
    For each name of color argument provided in  *color_keys*, the
    function searches through *dict_1* and processes each using
    :func:`get_color`. If the argument is not found in *dict_1*, it then
    searches through each additional dictionary provided in *args*.

    Arguments:
      dict_1 (dict): Target and first source of keys
      color_keys (list): Names of keys
      *args (tuple): Additional dictionary sources of keys
      **kwargs (additional keyword arguments
      keys (list): Acceptable keys in order of decreasing priority
    """
    from . import get_color

    color_keys = kwargs.get("color_keys",
        ["c", "color", "mec", "markeredgecolor", "mfc", "markerfacecolor"])
    for color_key in color_keys:
        if color_key in dict_1:
            dict_1[color_key] = get_color(dict_1[color_key])
        else:
            for arg in args:
                if color_key in arg:
                    dict_1[color_key] = get_color(arg[color_key])


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


def multi_get_merged(keys, dictionary):
    """
    Scans dict for keys; returns list of values for all matches

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested

    Returns:
      value: Values for all matching keys
    """
    values = []
    for key in [key for key in keys if key in dictionary]:
        if isinstance(dictionary[key], list):
            values.extend(dictionary[key])
        else:
            values.append(dictionary[key])

    return values


def multi_pop_merged(keys, dictionary):
    """
    Scans dict for keys; returns list of values for all matches

    Arguments:
      keys (str, list): Acceptable key(s) in order of decreasing
        priority
      dictionary (dict): dict to be tested

    Returns:
      value: Values for all matching keys
    """
    values = []
    for key in [key for key in keys if key in dictionary]:
        if isinstance(dictionary[key], list):
            values.extend(dictionary[key])
        else:
            values.append(dictionary[key])
        del (dictionary[key])

    return values


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
    Scans dict for keys; returns first value and deletes it and others.

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
        raise TypeError("Argument 'keys' must be a string or iterable")

    if not isinstance(dictionary, dict):
        raise TypeError("Argument 'dictionary' must be a dict")

    if pop and copy:
        raise TypeError("Argument seetings 'pop' and 'copy' may not be used "
                        "simultaneously; if the value is to be removed from "
                        "the source "
                        "dictionary making a copy of it is not appropriate.")

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
      tick_labels (list): Tick labels, each with the same number of
      digits after the decimal point
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


def get_edges(figure_or_subplots, absolute=False, **kwargs):
    """
    Finds the outermost edges of a set of subplots on a figure.

    Arguments:
      figure_or_subplots (Figure, list, dict): Axes whose edges to
        get; if Figure, use all Axes

    Returns:
      (dict): Edges; keys are 'left', 'right', 'top', and 'bottom'

    .. todo:
      - What are the units here? Probably relative but should be
        documented or possibly an option
    """
    import matplotlib

    if isinstance(figure_or_subplots, matplotlib.figure.Figure):
        figure = figure_or_subplots
        subplots = figure.axes
        if len(subplots) == 0:
            edges = dict(left=0.5, right=0.5, top=0.5, bottom=0.5)
        else:
            edges = dict(left=min([s.get_position().xmin for s in subplots]),
                right=max([s.get_position().xmax for s in subplots]),
                top=max([s.get_position().ymax for s in subplots]),
                bottom=min([s.get_position().ymin for s in subplots]))
    elif isinstance(figure_or_subplots, dict):
        subplots = figure_or_subplots.values()
        figure = subplots[0].get_figure()
        if len(subplots) == 0:
            edges = dict(left=0.5, right=0.5, top=0.5, bottom=0.5)
        else:
            edges = dict(left=min([s.get_position().xmin for s in subplots]),
                right=max([s.get_position().xmax for s in subplots]),
                top=max([s.get_position().ymax for s in subplots]),
                bottom=min([s.get_position().ymin for s in subplots]))
    elif isinstance(figure_or_subplots, matplotlib.axes.Axes):
        subplot = figure_or_subplots
        figure = subplot.get_figure()
        edges = dict(left=subplot.get_position().xmin,
            right=subplot.get_position().xmax, top=subplot.get_position().ymax,
            bottom=subplot.get_position().ymin)
    edges["width"] = edges["right"] - edges["left"]
    edges["height"] = edges["top"] - edges["bottom"]

    if absolute:
        fig_height = figure.get_figheight()
        fig_width = figure.get_figwidth()
        edges["left"] *= fig_width
        edges["right"] *= fig_width
        edges["width"] *= fig_width
        edges["top"] *= fig_height
        edges["bottom"] *= fig_height
        edges["height"] *= fig_height

    return edges


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
        kwargs["weight"] = kwargs.get("weight",
            {"r": "regular", "b": "bold"}[fp[-1]])
    elif isinstance(fp, dict):
        kwargs.update(fp)
    else:
        raise TypeError(
            "Function myplotspec.get_font() does not support" + "input of "
                                                                "type {"
                                                                "0}".format(
                fp.__class__.__name__))
    return FontProperties(**kwargs)


def get_figure_subplots(figure=None, subplots=None, index=None, nrows=None,
        ncols=None, nsubplots=None, left=None, sub_width=None, wspace=None,
        right=None, bottom=None, sub_height=None, hspace=None, top=None,
        fig_width=None, fig_height=None, figsize=None, verbose=1, debug=0,
        **kwargs):
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
    if ((sub_width is None or sub_height is None) and (
        (fig_width is None or fig_height is None) and figsize is None)):
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
    elif ((sub_width is None or sub_height is None) and not (
        (fig_width is None or fig_height is None) and figsize is None)):
        # Lack sublot dimensions, but have figure dimensions
        if figsize is not None:
            fig_width, fig_height = figsize
        figsize = [fig_width, fig_height]
        if sub_width is None:
            sub_width = fig_width - left - (wspace * (ncols - 1)) - right
        if sub_height is None:
            sub_height = fig_height - top - (hspace * (nrows - 1)) - bottom
    elif (not (sub_width is None or sub_height is None) and (
        (fig_width is None or fig_height is None) and figsize is None)):
        # Have subplot dimensions, but lack figure dimensions
        if fig_width is None:
            fig_width = left + (sub_width * ncols) + (
            wspace * (ncols - 1)) + right
        if fig_height is None:
            fig_height = top + (sub_height * nrows) + (
            hspace * (nrows - 1)) + bottom
        figsize = [fig_width, fig_height]
    elif (not (sub_width is None or sub_height is None) and not (
        (fig_width is None or fig_height is None) and figsize is None)):
        # Have subplot and figure dimensions
        figsize = [fig_width, fig_height]

    # Manage figure
    if figure is None:
        figure_kw = kwargs.get("figure_kw", {})
        figure = pyplot.figure(figsize=figsize, **figure_kw)

    # Manage subplots
    subplot_kw = kwargs.get("subplot_kw", kwargs.get("axes_kw", {}))
    if subplots is not None:
        if len(subplots) == 0:
            i = 0
        elif index is not None:
            i = index
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
            subplots[i] = matplotlib.axes.Axes(figure,
                rect=[(left + k * sub_width + k * wspace) / fig_width,  # Left
                    (bottom + j * sub_height + j * hspace) / fig_height,
                    # Bottom
                    sub_width / fig_width,  # Width
                    sub_height / fig_height],  # Height
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
        self.items.insert(index, key)

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
