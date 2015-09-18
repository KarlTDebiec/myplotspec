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
      - Support multiple inheritance/extension for presets
      - Preset classes, such as 'target', 'content', 'appearance', etc.
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
      - Double-check verbose and debug support
      - Figure out how to write loose arguments (e.g. [x]tick[s]) in
        sphinx-compatible way
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
          defaults (string, dict, optional): Default arguments; may be a
            yaml string, path to a yaml file, or a dictionary; if not
            provided pulled from self.defaults
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
            yaml string, path to a yaml file, or a dictionary; if not
            provided pulled from self.available_presets
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
    def draw_report(self, verbose=1, debug=0, **kwargs):
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
          figure[s] (dict): Figure specifications
          preset[s] (str, list, optional): Selected preset(s); presets loaded
            from figure specification will take precedence over those passed as
            arguments
          yaml_spec (str, dict, optional): Argument data structure; may be
            string path to yaml file, yaml-format string, or dictionary
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments

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

        .. todo:
          - Support slicing for passage of arguments to multiple figures
          - Move preset handling to another function, alongside support for
            mutual exclusivity
        """
        from copy import deepcopy
        import six
        from . import multi_get, multi_get_copy, multi_pop

        # Load spec and prepare outfiles
        figure_specs = multi_pop(["figures", "figure"], kwargs, {})
        figure_indexes = sorted([int(i) for i in figure_specs.keys()
                           if str(i).isdigit()])
        outfiles = {}

        # Configure and plot figures
        for i in figure_indexes:

            # Load the spec for this figure
            if isinstance(figure_specs[i], dict):
                figure_spec = deepcopy(figure_specs[i])
            elif figure_specs[i] is None:
                figure_spec = {}
            else:
                raise TypeError("Figure {0} specification".format(i) +
                  "loaded as {0} ".format(figure_spec.__class__.__name__) +
                  "rather than expected dict.")

            # Output settings from spec override inherited settings
            if "verbose" not in figure_spec:
                figure_spec["verbose"] = verbose
            if "debug" not in figure_spec:
                figure_spec["debug"] = debug

            # Presets from spec have priority over presets from args
            spec_presets = multi_pop(["presets", "preset"], figure_spec, [])
            if isinstance(spec_presets, six.string_types):
                spec_presets = [spec_presets]
            elif spec_presets is None:
                spec_presets = []
            arg_presets = multi_get_copy(["presets", "preset"], kwargs, [])
            if isinstance(arg_presets, six.string_types):
                arg_presets = [arg_presets]
            elif arg_presets is None:
                arg_presets = []
            for arg_preset in reversed(arg_presets):
                if not arg_preset in spec_presets:
                    spec_presets.insert(0, arg_preset)
            figure_spec["presets"] = spec_presets

            # Build list of keys from which to load from spec dict
            figure_spec["yaml_spec"] = kwargs.get("yaml_spec", {})
            figure_spec["yaml_keys"] = [["figures", "all"], ["figures", i]]

            figure_spec["outfiles"] = outfiles
            self.draw_figure(**figure_spec)

        # Clean up
        for outfile in outfiles.values():
            outfile.close()

    @manage_defaults_presets()
    @manage_kwargs()
    @manage_output()
    def draw_figure(self, title=None, shared_xlabel=None,
        shared_ylabel=None, shared_legend=None, multiplot=False, verbose=1,
        debug=0, **kwargs):
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
          subplot[s] (dict): Subplot specifications
          preset[s] (str, list, optional): Selected preset(s); presets loaded
            from figure specification will take precedence over those passed as
            arguments
          title (str, optional): Figure title
          shared_xlabel (str, optional): X label to be shared among
            subplots
          shared_ylabel (str, optional): Y label to be shared among
            subplots
          shared_legend (bool, optional): Generate a legend shared 
            between subplots
          multiplot (bool, optional): 
          nrows (int, optional):
          ncols (int, optional):
          nsubplots (int, optional): 
          multi_xticklabels (list, optional): 
          multi_yticklabels (list, optional): 
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments

        Returns:
          (figure): Figure
        """
        from collections import OrderedDict
        from copy import deepcopy
        from warnings import warn
        import six
        from . import (get_figure_subplots, multi_get, multi_get_copy,
                       multi_pop)
        from .legend import set_shared_legend
        from .text import set_title, set_shared_xlabel, set_shared_ylabel

        # Load spec and prepare figure and subplots
        subplot_specs = multi_pop(["subplots", "subplot"], kwargs, {})
        if subplot_specs is None:
            subplot_specs = {}
        subplot_indexes = sorted([int(i) for i in subplot_specs.keys()
                            if str(i).isdigit()])
        figure, subplots = get_figure_subplots(verbose=verbose, debug=debug,
                             **kwargs)

        # Format Figure
        if title is not None:
            set_title(figure, title=title, **kwargs)
        if shared_xlabel is not None:
            set_shared_xlabel(figure, xlabel=shared_xlabel, **kwargs)
        if shared_ylabel is not None:
            set_shared_ylabel(figure, ylabel=shared_ylabel, **kwargs)
        if shared_legend is not None and shared_legend is not False:
            shared_handles = OrderedDict()

        # Load multiplot variables
        if multiplot:
            nrows = kwargs.get("nrows", 1)
            ncols = kwargs.get("ncols", 1)
            nsubplots = kwargs.get("nsubplots", nrows * ncols)
            multi_xticklabels = kwargs.get("multi_xticklabels")
            multi_yticklabels = kwargs.get("multi_yticklabels")

        # Configure and plot subplots
        for i in subplot_indexes:

            # Load the subplot and spec
            if i in subplots:
                subplot = subplots[i]
            else:
                warn("Specs provided for subplot {0}, ".format(i) +
                  "but only subplot indexes {0} ".format(subplots.keys()) +
                  "were created; check that nrows, ncols, and nsubplots "
                  "are appropriate; skipping subplots {0}.".format(i))
                continue
            if isinstance(subplot_specs[i], dict):
                subplot_spec = deepcopy(subplot_specs[i])
            elif subplot_specs[i] is None:
                subplot_spec = {}
            else:
                raise TypeError("Subplot {0} specification".format(i) +
                  "loaded as {0} ".format(subplot_spec.__class__.__name__) +
                  "rather than expected dict.")

            # Include reference to figure and subplots
            subplot_spec["figure"] = figure
            subplot_spec["subplots"] = subplots

            # Output settings from spec override inherited settings
            if "verbose" not in subplot_spec:
                subplot_spec["verbose"] = verbose
            if "debug" not in subplot_spec:
                subplot_spec["debug"] = debug

            # Presets from spec have priority over inherited presets
            spec_presets = multi_pop(["presets", "preset"], subplot_spec, [])
            if isinstance(spec_presets, six.string_types):
                spec_presets = [spec_presets]
            elif spec_presets is None:
                spec_presets = []
            arg_presets = multi_get_copy(["presets", "preset"], kwargs, [])
            if isinstance(arg_presets, six.string_types):
                arg_presets = [arg_presets]
            elif arg_presets is None:
                arg_presets = []
            for arg_preset in reversed(arg_presets):
                if not arg_preset in spec_presets:
                    spec_presets.insert(0, arg_preset)
            subplot_spec["presets"] = spec_presets

            # Build list of keys from which to load from spec dict
            subplot_spec["yaml_spec"] = kwargs.get("yaml_spec", {})
            subplot_spec["yaml_keys"] = [key
              for key2 in [[key3 + ["subplots", "all"],
                            key3 + ["subplots", i]]
              for key3 in kwargs.get("yaml_keys")]
              for key  in key2]

            if shared_legend is not None and shared_legend is not False:
                subplot_spec["shared_handles"] = shared_handles

            # Manage multiplot x and y labels
            if multiplot:
                if multi_xticklabels is not None:
                    if (nrows - 1) * ncols - 1 < i < nsubplots - 1:
                        if not "xticklabels" in subplot_spec:
                            subplot_spec["xticklabels"] = multi_xticklabels[:-1]
                    elif i != nsubplots - 1:
                        if not "xticklabels" in subplot_spec:
                            subplot_spec["xticklabels"] = []
                        if not "xlabel" in subplot_spec:
                            subplot_spec["xlabel"] = None
                if multi_yticklabels is not None:
                    if i % ncols == 0 and i != 0:
                        if not "yticklabels" in subplot_spec:
                            subplot_spec["yticklabels"] = multi_yticklabels[:-1]
                    elif i != 0:
                        if not "yticklabels" in subplot_spec:
                            subplot_spec["yticklabels"] = []
                        if not "ylabel" in subplot_spec:
                            subplot_spec["ylabel"] = None

            self.draw_subplot(subplot, **subplot_spec)

        # Draw legend
        if shared_legend is not None and shared_legend is not False:
            set_shared_legend(figure, subplots, handles=shared_handles,
              **kwargs)

        # Return results
        return figure

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_subplot(self, subplot, title=None, legend=None,
        partner_subplot=False, shared_handles=None, visible=True, verbose=1,
        debug=0, **kwargs):
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
          dataset[s] (dict): Dataset specifications
          preset[s] (str, list, optional): Selected preset(s); presets loaded
            from figure specification will take precedence over those passed as
            arguments
          title (str, optional): Subplot title
          legend (bool, optional): Draw legend on subplot
          partner_subplot (bool, optional): Add a parter subplot
          shared_handles (OrderedDict, optional): Nascent OrderedDict of
            [labels]:handles shared among subplots of host figure; used
            to draw shared legend on figure
          visible (bool, optional): Subplot visibility
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments
        """
        from collections import OrderedDict
        from copy import deepcopy
        import six
        from . import multi_get, multi_get_copy, multi_pop
        from .axes import set_xaxis, set_yaxis, add_partner_subplot
        from .legend import set_legend
        from .text import set_title

        # Format subplot
        set_xaxis(subplot, **kwargs)
        set_yaxis(subplot, **kwargs)
        if title is not None:
            set_title(subplot, title=title, **kwargs)
        if partner_subplot:
            add_partner_subplot(subplot, **kwargs)

        # Load spec
        dataset_specs = multi_get(["datasets", "dataset"], kwargs, {})
        if dataset_specs is None:
            dataset_specs = {}
        dataset_indexes = sorted([int(i) for i in dataset_specs.keys()
                           if str(i).isdigit()])
        handles = OrderedDict()

        # Configure and plot datasets
        for i in dataset_indexes:

            # Load the spec for this dataset
            if isinstance(dataset_specs[i], dict):
                dataset_spec = deepcopy(dataset_specs[i])
            elif dataset_specs[i] is None:
                dataset_spec = {}
            else:
                raise TypeError("Dataset {0} specification".format(i) +
                  "loaded as {0} ".format(subplot_spec.__class__.__name__) +
                  "rather than expected dict.")

            # Include reference to figure and subplots
            dataset_spec["figure"] = kwargs["figure"]
            dataset_spec["subplots"] = kwargs["subplots"]

            # Output settings from spec override inherited settings
            if "verbose" not in dataset_spec:
                dataset_spec["verbose"] = verbose
            if "debug" not in dataset_spec:
                dataset_spec["debug"] = debug

            # Presets from spec have priority over inherited presets
            spec_presets = multi_pop(["presets", "preset"], dataset_spec, [])
            if isinstance(spec_presets, six.string_types):
                spec_presets = [spec_presets]
            elif spec_presets is None:
                spec_presets = []
            arg_presets = multi_get_copy(["presets", "preset"], kwargs, [])
            if isinstance(arg_presets, six.string_types):
                arg_presets = [arg_presets]
            elif arg_presets is None:
                arg_presets = []
            for arg_preset in reversed(arg_presets):
                if not arg_preset in spec_presets:
                    spec_presets.insert(0, arg_preset)
            dataset_spec["presets"] = spec_presets

            # Build list of keys from which to load from spec dict
            dataset_spec["yaml_spec"] = kwargs.get("yaml_spec", {})
            dataset_spec["yaml_keys"] = [key
              for key2 in [[key3 + ["datasets", "all"],
                            key3 + ["datasets", i]]
              for key3 in kwargs.get("yaml_keys")]
              for key  in key2]

            self.draw_dataset(subplot=subplot, handles=handles,
              **dataset_spec)

        # Draw subplot legend
        if legend is not None and legend is not False:
            set_legend(subplot, handles=handles, **kwargs)

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
