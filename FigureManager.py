#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.FigureManager.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Generates one or more figures to specifications provided in a YAML file.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
import matplotlib
matplotlib.use("agg")
if __name__ == "__main__":
    __package__ = str("myplotspec")
    import myplotspec
################################### CLASSES ###################################
class FigureManager(object):
    """
    Manages the generation of figures.

    Attributes:
      defaults (str, dict): Default arguments to :func:`draw_report`,
        :func:`draw_figure`, :func:`draw_subplot`, and
        :func:`draw_dataset` functions, in yaml format. Outer level (of
        indentation or keys) provides function names, and inner level
        provides default arguments to each function::

          defaults = \"\"\"
              method_1:
                method_1_arg_1: 1000
                method_1_arg_2: abcd
              method_2
                method_2_arg_1: 2000
                method_2_arg_2: efgh
              ...
          \"\"\"

      available_presets (str, dict): Available sets of preset arguments to
        :func:`draw_report`, :func:`draw_figure`, :func:`draw_subplot`,
        and :func:`draw_dataset` functions, in yaml format. Outer level
        (of indentation or keys) provides preset names, middle level
        provides function names, and inner level provides arguments to
        pass to each function when preset is active::

          availabe_presets = \"\"\"
            preset_1:
              method_1:
                method_1_arg_1: 1001
                method_1_arg_2: abcde
              method_2
                method_2_arg_1: 2001
                method_2_arg_2: efghi
            preset_2:
              method_1:
                method_1_arg_1: 1002
                method_1_arg_2: abcdef
              method_2
                method_2_arg_1: 2002
                method_2_arg_2: efghij
          \"\"\"

        Each preset may additionally contain the keys 'help', 'extends'
        and 'inherits'. 'help' may contain a short help message
        displayed with the help text of the script. 'extends' may
        contain the name of another preset within the class from which
        the preset will inherit (and optionally override) all arguments.
        Subclasses of this base FigureManager class may also include the
        keyword 'inherits' which may contain the name of a preset of
        FigureManager (listed below) from which it will inherit (and
        optionally override) all arguments.

    .. todo:
      - Accept presets from file, e.g. --preset-file /path/to/file.yaml
      - Support mutually exclusive presets that may smoothly and
        verbosely override one another
      - More advanced preset and overall specification help
      - Intermediate level of debug output
      - Bring documentation up to date
      - Better examples
      - Improved dataset caching
      - Dataset base class with caching support
      - 2D indexing of subplots
      - Support slicing for passage of arguments to multiple figures,
        subplots, or datasets
      - Clean up multi_kw or come up with reasonable alternative
      - Consider making spec keys case-insensitive
      - Be more careful (less wasteful) about use of copy()
      - Decide how to manage the specification of sizes, positions, etc.
        in real-world units (inches or centimeters)
      - Improve support for seaborn colors
      - Clean up docstring return values
    """
    from .manage_defaults_presets import manage_defaults_presets
    from .manage_kwargs import manage_kwargs
    from .manage_output import manage_output

    available_presets = """
      letter:
        help: Letter (width ≤ 6.5", height ≤ 9.0")
        draw_figure:
          fig_width:  9.00
          fig_height: 6.50
          title_fp: 16b
          label_fp: 16b
        draw_subplot:
          title_fp:  16b
          label_fp:  16b
          tick_fp:   14r
          legend_fp: 14r
      notebook:
        help: Notebook (width ≤ 6.5", height ≤ 9.0")
        draw_figure:
          title_fp:  10b
          label_fp:  10b
          legend_fp: 10b
        draw_subplot:
          title_fp: 10b
          label_fp: 10b
          tick_fp:   8r
          legend_fp: 8r
          tick_params:
            length: 2
            pad: 6
        draw_dataset:
          plot_kw:
            lw: 1
      poster:
        help: Poster
        draw_subplot:
          title_fp: 36r
          label_fp: 36r
          tick_fp:  24r
          tick_params:
            length: 3
            width: 1
            pad: 10
          lw: 2
        draw_dataset:
          plot_kw:
            lw: 2
      presentation:
        help: 4:3 presentation (width = 10.24", height = 7.68")
        draw_figure:
          fig_width:  10.24
          fig_height:  7.68
          title_fp:  24b
          label_fp:  24b
          legend_fp: 16r
        draw_subplot:
          title_fp: 18r
          label_fp: 18r
          tick_fp:  14r
          tick_params:
            length: 3
            width: 1
            pad: 6
          legend_fp: 14r
          lw: 2
        draw_dataset:
          plot_kw:
            lw:  2
      presentation_wide:
        help: 16:9 presentation (width = 19.20", height = 10.80")
        draw_figure:
          fig_width:  19.20
          fig_height: 10.80
          title_fp:  24b
          label_fp:  24b
          legend_fp: 24r
        draw_subplot:
          title_fp: 24b
          label_fp: 24b
          tick_fp:  20r
          tick_params:
            length: 6
            width: 2
            pad: 10
          lw: 3
        draw_dataset:
          plot_kw:
            lw: 3
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes.

        Arguments:
          defaults (string, dict): Default arguments; may be a yaml
            string, path to a yaml file, or a dictionary
          args (tuple): Additional positional arguments
          kwargs (dict): Additional keyword arguments
        """
        from . import get_yaml

        defaults = get_yaml(kwargs.get("defaults",
          self.defaults if hasattr(self, "defaults") else {}))
        self.defaults = defaults

        available_presets = self.initialize_presets(*args, **kwargs)
        self.available_presets = available_presets

        self.dataset_cache = {}

        super(FigureManager, self).__init__(*args, **kwargs)

    def initialize_presets(self, *args, **kwargs):
        """
        Initializes presets.

        Arguments:
          available_presets (string, dict): Available presets; may be a
            yaml string, path to a yaml file, or a dictionary
          args (tuple): Additional positional arguments
          kwargs (dict): Additional keyword arguments

        .. todo:
            - Debug output
            - Mutual exclusivity (does this go here?)
        """
        from . import get_yaml, merge_dicts

        available_presets = get_yaml(kwargs.get("available_presets",
          self.available_presets if hasattr(self, "available_presets")
          else {}))
        super_presets = get_yaml(super(self.__class__, self).available_presets
          if hasattr(super(self.__class__, self), "available_presets") else {})
        for preset_name, preset in available_presets.items():
            if "inherits" in preset:
                parent_name = preset["inherits"]
                if parent_name in super_presets:
                    available_presets[preset_name] = merge_dicts(
                      super_presets[parent_name], preset)
        for preset_name, preset in available_presets.items():
            if "extends" in preset:
                parent_name = preset["extends"]
                if parent_name in available_presets:
                    available_presets[preset_name] = merge_dicts(
                      available_presets[parent_name], preset)
        return available_presets

    def __call__(self, *args, **kwargs):
        """
        When called as a function, calls :func:`draw_report`.

        Arguments:
          args (tuple): Passed to :func:`draw_report`
          kwargs (dict): Passed to :func:`draw_report`
        """
        self.draw_report(*args, **kwargs)

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_report(self, verbose=1, debug=0, **in_kwargs):
        """
        Draws one or more figures based on provided specifications.

        Figure specs are provided in a dict structured as follows::

            figures = {
                'all': {
                    'shared_xlabel': 'Time',
                    'shared_ylabel': 'Measurement',
                    'shared_legend': True,
                    ...
                },
                '0': {
                    'title': 'Trial 1',
                    'subplots': {
                        ...
                    },
                    ...
                },
                '1': {
                    'title': 'Trial 2',
                    'subplots': {
                        ...
                    },
                    ...
                },
                '2': {
                    'title': 'Trial 3',
                    'subplots': {
                        ...
                    },
                    ...
                },
                ...
            }

        The values stored at each (0-indexed) integer key provide the
        arguments to be passed to :func:`draw_figure` for each of a
        series of figures. Values stored at 'all' are passed to each
        figure, but overridden by values specific to that figure.

        Arguments:
          figures (dict): Figure specifications
          preset (str, list): Selected preset(s)
          yaml_spec (str, dict): Argument data structure; may be yaml
            string, path to yaml file, or dict
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          in_kwargs (dict): Additional keyword arguments

        Note:
          This function is one of two responsible for managing the
          output of figures to pdf files, if specified. While other
          output formats are single-page, pdf files may be multi-page.
          In order to allow multiple figures to be output to multiple
          pdfs, this function maintains a dict outfiles containing
          references to a PdfPages object for each specified pdf
          outfile. :func:`draw_figure`'s decorator
          :class:`~.manage_output.manage_output` adds new PdfPages
          objects as requested, or adds pages to existing ones. Once all
          figures have been drawn, this function closes each PdfPages.
        """
        from copy import copy
        import six
        from . import multi_kw

        # Load spec and prepare outfiles
        figure_specs = multi_kw(["figures", "figure"], in_kwargs, {})
        figure_indexes = sorted([int(i) for i in figure_specs.keys()
                           if str(i).isdigit()])
        outfiles = {}

        # Configure and plot figures
        for i in figure_indexes:
            # Load the spec for this figure
            if isinstance(figure_specs[i], dict):
                out_kwargs = copy(figure_specs[i])
            elif figure_specs[i] is None:
                out_kwargs = {}
            else:
                raise TypeError()

            # Output settings from spec override inherited settings
            if "verbose" not in out_kwargs:
                out_kwargs["verbose"] = verbose
            if "debug" not in out_kwargs:
                out_kwargs["debug"] = debug

            # Presets from spec have priority over inherited presets
            out_presets = multi_kw(["presets", "preset"], out_kwargs, [])
            if isinstance(out_presets, six.string_types):
                out_presets = [out_presets]
            elif out_presets is None:
                out_presets = []
            in_presets = multi_kw(["presets", "preset"], copy(in_kwargs), [])
            if isinstance(in_presets, six.string_types):
                in_presets = [in_presets]
            elif in_presets is None:
                in_presets = []
            for in_preset in reversed(in_presets):
                if not in_preset in out_presets:
                    out_presets.insert(0, in_preset)
            out_kwargs["presets"] = out_presets

            # Build list of keys from which to load from spec dict
            out_kwargs["yaml_spec"] = copy(in_kwargs.get("yaml_spec", {}))
            out_kwargs["yaml_keys"] = [["figures", "all"], ["figures", i]]

            out_kwargs["outfiles"] = outfiles
            self.draw_figure(**out_kwargs)

        # Clean up
        for outfile in outfiles.values():
            outfile.close()

    @manage_defaults_presets()
    @manage_kwargs()
    @manage_output()
    def draw_figure(self, title=None, shared_xlabel=None,
        shared_ylabel=None, shared_legend=None, multiplot=False, verbose=1,
        debug=0, **in_kwargs):
        """
        Draws a figure.

        Figure will typically contain one or more subplots, whose
        specifications are provided in a dict structured as follows::

            subplots = {
                'all': {
                    'legend': True,
                    ...
                },
                '0': {
                    'title':    'Subplot 1',
                    'datasets': {
                        ...
                    },
                    ...
                },
                '1': {
                    'title':    'Subplot 2',
                    'datasets': {
                        ...
                    },
                    ...
                },
                '2': {
                    'title':    'Subplot 3',
                    'datasets': {
                        ...
                    },
                    ...
                },
                ...
            }

        The values stored at each integer key (0-indexed) provide the
        arguments to be passed to :func:`draw_subplot` for each of a
        series of subplots. Values stored at 'all' are passed to each
        subplot, but overridden by values specific to that subplot.

        Figure may be annotated by drawing a title, shared x axis label,
        shared y axis label, or shared legend. Title and shared axis
        labels are (by default) centered on all subplots present on the
        figure, Shared legend is drawn on an additional subplot created
        after those specified in subplots, using the arguments provided
        in 'shared_legend'.

        Arguments:
          outfile (str): Output filename
          subplots (dict): Subplot specifications
          preset (str, list): Selected preset(s)
          title (str, optional): Figure title
          shared_xlabel (str, optional): X label to be shared among
            subplots
          shared_ylabel (str, optional): Y label to be shared among
            subplots
          shared_legend (bool, optional): Generate a legend shared 
            between subplots
          shared_legend_kw (dict, optional): Keyword arguments to be
            used to generate shared legend
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          in_kwargs (dict): Additional keyword arguments

        Returns:
          (*Figure*): Figure
        """
        from collections import OrderedDict
        from copy import copy, deepcopy
        import six
        from . import get_figure_subplots, multi_kw
        from .legend import set_shared_legend
        from .text import set_title, set_shared_xlabel, set_shared_ylabel

        # Load spec and prepare figure and subplots
        subplot_specs = multi_kw(["subplots", "subplot"], in_kwargs, {})
        subplot_indexes = sorted([int(i) for i in subplot_specs.keys()
                            if str(i).isdigit()])
        figure, subplots = get_figure_subplots(verbose=verbose,
          debug=debug, **in_kwargs)
        self.figure = figure
        self.subplots = subplots

        # Format Figure
        if title is not None:
            set_title(figure, title=title, **in_kwargs)
        if shared_xlabel is not None:
            set_shared_xlabel(figure, xlabel=shared_xlabel, **in_kwargs)
        if shared_ylabel is not None:
            set_shared_ylabel(figure, ylabel=shared_ylabel, **in_kwargs)
        if shared_legend is not None:
            shared_handles = OrderedDict()

        if multiplot:
            nrows = in_kwargs.get("nrows", 1)
            ncols = in_kwargs.get("ncols", 1)
            nsubplots = in_kwargs.get("nsubplots", nrows * ncols)
            multi_xticklabels = in_kwargs.get("multi_xticklabels")
            multi_yticklabels = in_kwargs.get("multi_yticklabels")

        # Configure and plot subplots
        for i in subplot_indexes:
            if i not in subplots:
                continue
            # Load the spec for this subplot
            if isinstance(subplot_specs[i], dict):
                out_kwargs = copy(subplot_specs[i])
            elif subplot_specs[i] is None:
                out_kwargs = {}
            else:
                raise TypeError()

            # Include reference to figure and subplots
            out_kwargs["figure"] = figure
            out_kwargs["subplots"] = subplots

            # Output settings from spec override inherited settings
            if "verbose" not in out_kwargs:
                out_kwargs["verbose"] = verbose
            if "debug" not in out_kwargs:
                out_kwargs["debug"] = debug

            # Presets from spec have priority over inherited presets
            out_presets = multi_kw(["presets", "preset"], out_kwargs, [])
            if isinstance(out_presets, six.string_types):
                out_presets = [out_presets]
            elif out_presets is None:
                out_presets = []
            in_presets = multi_kw(["presets", "preset"], copy(in_kwargs), [])
            if isinstance(in_presets, six.string_types):
                in_presets = [in_presets]
            elif in_presets is None:
                in_presets = []
            for in_preset in reversed(in_presets):
                if not in_preset in out_presets:
                    out_presets.insert(0, in_preset)
            out_kwargs["presets"] = out_presets

            # Build list of keys from which to load from spec dict
            out_kwargs["yaml_spec"] = copy(in_kwargs.get("yaml_spec", {}))
            out_kwargs["yaml_keys"] = [key
              for key2 in [[key3 + ["subplots", "all"],
                            key3 + ["subplots", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]

            if shared_legend is not None:
                out_kwargs["shared_handles"] = shared_handles

            if multiplot:
                if multi_xticklabels is not None:
                    if (nrows - 1) * ncols - 1 < i < nsubplots - 1:
                        if not "xticklabels" in out_kwargs:
                            out_kwargs["xticklabels"] = multi_xticklabels[:-1]
                    elif i != nsubplots - 1:
                        if not "xticklabels" in out_kwargs:
                            out_kwargs["xticklabels"] = []
                        if not "xlabel" in out_kwargs:
                            out_kwargs["xlabel"] = None
                if multi_yticklabels is not None:
                    if i % ncols == 0 and i != 0:
                        if not "yticklabels" in out_kwargs:
                            out_kwargs["yticklabels"] = multi_yticklabels[:-1]
                    elif i != 0:
                        if not "yticklabels" in out_kwargs:
                            out_kwargs["yticklabels"] = []
                        if not "ylabel" in out_kwargs:
                            out_kwargs["ylabel"] = None

            self.draw_subplot(subplot=subplots[i], **out_kwargs)

        # Draw legend
        if shared_legend is not None and shared_legend is not False:
            set_shared_legend(figure, subplots, handles=shared_handles,
              **shared_legend)

        # Return results
        return figure

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_subplot(self, subplot, title=None, legend=None,
        partner_subplot=False, shared_handles=None, visible=True,verbose=1,
        debug=0, **in_kwargs):
        """
        Draws a subplot.

        Subplot will typically plot one or more datasets, whose
        specifications are provided in a dict structured as follows::

            datasets = {
                'all': {
                    'lw': 2,
                    ...
                },
                '0': {
                    'label':  'Dataset 1',
                    'infile': '/path/to/dataset_1.txt',
                    'color':  'red',
                    ...
                },
                '1': {
                    'label':  'Dataset 2',
                    'infile': '/path/to/dataset_2.txt',
                    'color':  'green',
                    ...
                },
                '2': {
                    'label':  'Dataset 3',
                    'infile': '/path/to/dataset_3.txt',
                    'color':  'blue',
                    ...
                },
                ...
            }

        The values stored at each integer key (0-indexed) provide the
        arguments to be passed to :func:`draw_dataset` for each of a
        series of datasets. Values stored at 'all' are passed to each
        dataset, but overridden by values specific to that dataset.

        Subplot may be formatted by adjusting or labeling the x and y
        axes, or drawing a title or a legend.

        Arguments:
          subplot (Axes): Axes on which to act
          datasets (dict): Dataset specifications
          preset (str, list): Selected preset(s)
          title (str, optional): Subplot title
          legend (bool, optional): Draw legend on subplot
          shared_handles (OrderedDict, optional): Nascent OrderedDict of
            [labels]:handles shared among subplots of host figure; used
            to draw shared legend
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          in_kwargs (dict): Additional keyword arguments
        """
        from collections import OrderedDict
        from copy import copy
        import six
        from . import multi_kw
        from .axes import set_xaxis, set_yaxis, add_partner_subplot
        from .legend import set_legend
        from .text import set_title

        # Format
        set_xaxis(subplot, **in_kwargs)
        set_yaxis(subplot, **in_kwargs)
        if title is not None:
            set_title(subplot, title=title, **in_kwargs)
        if partner_subplot:
            add_partner_subplot(subplot, **in_kwargs)

        # Configure and plot datasets
        handles = OrderedDict()
        dataset_specs = multi_kw(["datasets", "dataset"], in_kwargs, {})
        if dataset_specs is None:
            dataset_specs = {}
        dataset_indexes = sorted([int(i) for i in dataset_specs.keys()
                           if str(i).isdigit()])

        # Configure and plot datasets
        for i in dataset_indexes:
            # Load the spec for this dataset
            if isinstance(dataset_specs[i], dict):
                out_kwargs = copy(dataset_specs[i])
            elif dataset_specs[i] is None:
                out_kwargs = {}
            else:
                raise TypeError()

            # Include reference to figure and subplots
            out_kwargs["figure"] = in_kwargs["figure"]
            out_kwargs["subplots"] = in_kwargs["subplots"]

            # Output settings from spec override inherited settings
            if "verbose" not in out_kwargs:
                out_kwargs["verbose"] = verbose
            if "debug" not in out_kwargs:
                out_kwargs["debug"] = debug

            # Presets from spec have priority over inherited presets
            out_presets = multi_kw(["presets", "preset"], out_kwargs, [])
            if isinstance(out_presets, six.string_types):
                out_presets = [out_presets]
            elif out_presets is None:
                out_presets = []
            in_presets = multi_kw(["presets", "preset"], copy(in_kwargs), [])
            if isinstance(in_presets, six.string_types):
                in_presets = [in_presets]
            elif in_presets is None:
                in_presets = []
            for in_preset in reversed(in_presets):
                if not in_preset in out_presets:
                    out_presets.insert(0, in_preset)
            out_kwargs["presets"] = out_presets

            # Build list of keys from which to load from spec dict
            out_kwargs["yaml_spec"] = copy(in_kwargs.get("yaml_spec", {}))
            out_kwargs["yaml_keys"] = [key
              for key2 in [[key3 + ["datasets", "all"],
                            key3 + ["datasets", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]

            self.draw_dataset(subplot=subplot, handles=handles,
              **out_kwargs)

        # Draw subplot legend
        if legend is not None and legend is not False:
            set_legend(subplot, handles=handles, **in_kwargs)

        # Manage shared legend
        if shared_handles is not None:
            for label, handle in handles.items():
                if label not in shared_handles:
                    shared_handles[label] = handle

        if not visible:
            subplot.set_visible(False)
            subplot.set_frame_on(False)
            if hasattr(subplot, "_mps_y2"):
                subplot._mps_y2.set_visible(False)

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_dataset(self, subplot, infile, label=None, handles=None,
        verbose=1, debug=0, **kwargs):
        """
        Draws a dataset on a subplot.

        Arguments:
          subplot (Axes): Axes on which to draw
          infile (str): Path to input text file; first column is x,
            second is y
          label (str, optional): Dataset label
          color (str, list, ndarray, float, optional): Dataset color
          plot_kw (dict, optional): Additional keyword arguments passed
            to subplot.plot()
          handles (OrderedDict, optional): Nascent OrderedDict of
            [labels]: handles on subplot
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments
        """
        from . import get_color
        import numpy as np

        # Configure plot settings
        plot_kw = kwargs.get("plot_kw", {})
        if "color" in plot_kw:
            plot_kw["color"] = get_color(plot_kw.pop("color"))
        elif "color" in kwargs:
            plot_kw["color"] = get_color(kwargs.pop("color"))
        if label is not None:
            plot_kw["label"] = label

        # Load data
        dataset = np.loadtxt(infile)
        x = dataset[:,0]
        y = dataset[:,1]

        # Plot
        handle = subplot.plot(x, y, **plot_kw)[0]
        if handles is not None and label is not None:
            handles[label] = handle

    def load_dataset(self, cls, *args, **kwargs):
        """
        Loads a dataset, or reloads a previously-loaded dataset.

        Datasets are stored in FigureManager's dataset_cache instance
        variable, a dictionary containing copies of previously
        loaded datasets keyed by tuples containing the class and
        arguments used to instantiate the dataset.

        In order to support caching, a class must implement the static
        method 'get_cache_key', which generates the tuple key. Only
        arguments that affect the resulting dataset should be included
        in the key (e.g. 'infile' should be included, but 'verbose' and
        'debug' should not).

        Cachable dataset classes may also implement the method
        'get_cache_message' which returns a message to display when the
        dataset is loaded from the cache.

        Arguments:
          cls (class): Dataset class
          args (tuple): Positional arguments passed to
            cls.get_cache_key() and cls()
          kwargs (dict): Keyword arguments passed to cls.get_cache_key()
            and cls()

        Returns:
          dataset (cls): Dataset, either initialized new or copied from
            cache
        """
        verbose = kwargs.get("verbose", 1)
        debug = kwargs.get("debug", 0)

        if hasattr(cls, "get_cache_key"):
            try:
                cache_key = cls.get_cache_key(*args, **kwargs)
            except TypeError:
                return None
            if cache_key is None:
                return cls(*args, **kwargs)
            if cache_key in self.dataset_cache:
                if verbose >= 1:
                    if hasattr(cls, "get_cache_message"):
                        print(cls.get_cache_message(cache_key))
                    else:
                        print("previously loaded")
                return self.dataset_cache[cache_key]
            else:
                self.dataset_cache[cache_key] = cls(
                  dataset_cache=self.dataset_cache, *args, **kwargs)
                return self.dataset_cache[cache_key]
        else:
            return cls(*args, **kwargs)

    def main(self, parser=None):
        """
        Provides command-line functionality.

        Arguments:
          parser (ArgumentParser): Argparse argument parser; allos
            sublass to instantiate parser and add arguments (optional)
        """
        import argparse
        from inspect import getmodule
        from textwrap import wrap

        full_preset_names = sorted(
          [k for k, v in self.available_presets.items() if "extends" not in v])
        if len(full_preset_names) == 0:
            epilog = None
        else:
            epilog = "available presets:\n"
            for preset_name in full_preset_names:
                preset = self.available_presets[preset_name]
                extension_names = sorted(
                  [k for k, v in self.available_presets.items()
                    if "extends" in v and v["extends"] == preset_name])
                n_extensions = len(extension_names)
                symbol = "│" if n_extensions > 0 else " "
                if "help" in preset:
                    wrapped = wrap(preset["help"], 54)
                    if len(preset_name) > 20:
                        epilog += "  {0}\n".format(preset_name)
                        epilog += "   {0} {1:19}".format(symbol, " ")
                    else:
                        epilog += "  {0:22s}".format(preset_name)
                    epilog += "{0}\n".format(wrapped.pop(0))
                    for line in wrapped:
                        epilog += "   {0} {1:21}{2}\n".format(symbol, " ",
                                    line)
                else:
                    epilog += "  {0}\n".format(preset_name)
                for i, extension_name in enumerate(extension_names, 1):
                    symbol = "└" if i == n_extensions else "├"
                    extension = self.available_presets[extension_name]
                    if "help" in extension:
                        wrapped = wrap(extension["help"], 52)
                        if len(extension_name) > 18:
                            epilog += "   {0} {1}\n".format(symbol,
                                        extension_name)
                            symbol = "│" if i != n_extensions else " "
                            epilog += "   {0} {1:19}".format(symbol, " ")
                        else:
                            epilog += "   {0} {1:19}".format(symbol,
                                         extension_name)
                        epilog += "{0}\n".format(wrapped.pop(0))
                        symbol = "│" if i != n_extensions else " "
                        for line in wrapped:
                            epilog += "   {0} {1:21}{2}\n".format(symbol, " ",
                                        line)
                    else:
                        epilog += "   {0} {1}\n".format(symbol,
                                    extension_name)
        if parser is None:
            parser = argparse.ArgumentParser(
              description     = getmodule(self.__class__).__doc__,
              formatter_class = argparse.RawTextHelpFormatter,
              epilog          = epilog)
        else:
            parser.epilog = epilog

        parser.add_argument(
          "-yaml",
          type     = str,
          required = True,
          dest     = "yaml_spec",
          metavar  = "/PATH/TO/YAML.yml",
          help     = "YAML configuration file")

        parser.add_argument(
          "-preset", "-presets",
          type     = str,
          action   = "append",
          metavar  = "PRESET",
          default  = [],
          help     = "Selected preset(s)")

        seaborn = parser.add_mutually_exclusive_group()

        seaborn.add_argument(
          "-S",
          "--seaborn",
          action   = "store_const",
          const    = 2,
          default  = 0,
          help     = "Enable seaborn, overriding matplotlib defaults")

        seaborn.add_argument(
          "-s",
          "--seaborn-apionly",
          action   = "store_const",
          const    = 1,
          default  = 0,
          dest     = "seaborn",
          help     = "Enable seaborn without overriding matplotlib defaults")

        verbosity = parser.add_mutually_exclusive_group()

        verbosity.add_argument(
          "-v",
          "--verbose",
          action   = "count",
          default  = 1,
          help     = "Enable verbose output, may be specified more than once")

        verbosity.add_argument(
          "-q",
          "--quiet",
          action   = "store_const",
          const    = 0,
          default  = 1,
          dest     = "verbose",
          help     = "Disable verbose output")

        parser.add_argument(
          "-d",
          "--debug",
          action   = "count",
          default  = 0,
          help     = "Enable debug output, may be specified more than once")

        arguments = vars(parser.parse_args())

        if arguments["seaborn"] == 2:
            import seaborn
        elif arguments["seaborn"] == 1:
            import seaborn.apionly

        if arguments["debug"] >= 1:
            from os import environ
            from .debug import db_s, db_kv

            db_s("Environment variables")
            for key in sorted(environ):
                db_kv(key, environ[key], 1)

            db_s("Command-line arguments")
            for key in sorted(arguments.keys()):
                db_kv(key, arguments[key], 1)

        self(**arguments)

#################################### MAIN #####################################
if __name__ == "__main__":
    FigureManager().main()
