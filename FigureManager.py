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
    Manages the generation of figures using matplotlib.

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

      presets (str, dict): Available sets of preset arguments to
        :func:`draw_report`, :func:`draw_figure`, :func:`draw_subplot`,
        and :func:`draw_dataset` functions, in yaml format. Outer level
        (of indentation or keys) provides preset names, middle level
        provides function names, and inner level provides arguments to
        pass to each function when preset is active::

          presets = \"\"\"
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

    .. todo:
      - Accept presets from file, e.g. --preset-file /path/to/file.yaml
      - Support mutual exclusivity between presets
      - Support nested preset extensions
      - Set subplot's autoscale_on to false in draw_subplot?
      - Support quiet argument in addition to verbose
        (default verbose=1)
    """
    from .manage_defaults_presets import manage_defaults_presets
    from .manage_kwargs import manage_kwargs
    from .manage_output import manage_output

    defaults = """
        function:
          argument:     value
    """
    presets = """
      letter:
        help: Letter (width ≤ 6.5", height ≤ 8")
        draw_figure:
          fig_width:     9.00
          fig_height:    6.50
          title_fp:     16b
          label_fp:     16b
        draw_subplot:
          title_fp:     16b
          label_fp:     16b
          tick_fp:      14r
          legend_fp:    14r
      notebook:
        help: Notebook (width ≤ 6.5", height ≤ 8")
        draw_figure:
          title_fp:     10b
          label_fp:     10b
          legend_fp:    10b
        draw_subplot:
          title_fp:     10b
          label_fp:     10b
          tick_fp:      8r
          legend_fp:    8r
          tick_params:
            length:     2
            pad:        6
        draw_dataset:
          plot_kw:
            lw:         1
      poster:
        help: Poster
        draw_subplot:
          title_fp:     36r
          label_fp:     36r
          tick_fp:      24r
          tick_params:
            length:     3
            width:      1
            pad:        10
          lw:           2
        draw_dataset:
          plot_kw:
            lw:         2
      presentation:
        help: 4:3 presentation (width = 10.24", height = 7.68")
        draw_figure:
          fig_width:    10.24
          fig_height:    7.68
          title_fp:     24b
          label_fp:     24b
          legend_fp:    16r
        draw_subplot:
          title_fp:     18r
          label_fp:     18r
          tick_fp:      14r
          tick_params:
            length:     3
            width:      1
            pad:        6
          legend_fp:    14r
          lw:           2
        draw_dataset:
          plot_kw:
            lw:         2
      presentation_wide:
        help: 16:9 presentation (width = 19.20", height = 10.80")
        draw_figure:
          fig_width:    19.20
          fig_height:   10.80
          title_fp:     24b
          label_fp:     24b
          legend_fp:    24r
        draw_subplot:
          title_fp:     24b
          label_fp:     24b
          tick_fp:      20r
          tick_params:
            length:     6
            width:      2
            pad:        10
          lw:           3
        draw_dataset:
          plot_kw:
            lw:         3
    """

    def __init__(self, *args, **kwargs):
        """
        """
        from . import get_yaml

        defaults = get_yaml(kwargs.get("defaults",
          self.defaults if hasattr(self, "defaults") else {}))
        self.defaults = defaults

        presets = self.initialize_presets(*args, **kwargs)
        self.presets = presets

        super(FigureManager, self).__init__(*args, **kwargs)

    def initialize_presets(self, *args, **kwargs):
        """
        """
        from . import get_yaml, merge_dicts

        presets = get_yaml(kwargs.get("presets",
          self.presets if hasattr(self, "presets") else {}))
        if hasattr(super(self.__class__, self), "presets"):
            super_presets = get_yaml(super(self.__class__, self).presets)
        else:
            super_presets = {}
        for preset_name, preset in presets.items():
            if "inherits" in preset:
                parent_name = preset["inherits"]
                if parent_name in super_presets:
                    presets[preset_name] = merge_dicts(
                      super_presets[parent_name], preset)
        for preset_name, preset in presets.items():
            if "extends" in preset:
                parent_name = preset["extends"]
                if parent_name in presets:
                    presets[preset_name] = merge_dicts(presets[parent_name],
                    preset)
        return presets

    def __call__(self, *args, **kwargs):
        """
        When called as function, calls :func:`draw_report`.

        Arguments:
          args (tuple): Passed to :func:`draw_report`
          kwargs (dict): Passed to :func:`draw_report`
        """
        self.draw_report(*args, **kwargs)

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_report(self, **in_kwargs):
        """
        Draws a series of figures based on provided specifications.

        Figure specifications are provided in a dict structured as
        follows::

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
        figure_specs = in_kwargs.pop("figures", {})
        figure_indexes = sorted([i for i in figure_specs.keys()
                           if str(i).isdigit()])
        outfiles = {}

        # Configure and plot figures
        for i in figure_indexes:
            out_kwargs = figure_specs[i].copy()
            out_kwargs["verbose"] = in_kwargs.get("verbose", False)
            out_kwargs["debug"] = in_kwargs.get("debug", False)
            out_kwargs["preset"] = in_kwargs.get("preset", [])[:]
            out_kwargs["yaml_dict"] = in_kwargs.get("yaml_dict", {})
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
        shared_ylabel=None, shared_legend=None, **in_kwargs):
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
        in ``shared_legend``.

        Arguments:
          outfile (str): Output filename
          subplots (dict): Subplot specifications
          title (str, optional): Figure title
          shared_xlabel (str, optional): X label to be shared among
            subplots
          shared_ylabel (str, optional): Y label to be shared among
            subplots
          shared_legend (dict, optional): Keyword arguments used to
            generate a legend shared among subplots, if provided
          in_kwargs (dict): Additional keyword arguments

        Returns:
          (*Figure*): Figure
        """
        from collections import OrderedDict
        from . import get_figure_subplots
        from .legend import set_shared_legend
        from .text import set_title, set_shared_xlabel, set_shared_ylabel

        # Prepare figure and subplots with specified dimensions
        subplot_specs = in_kwargs.pop("subplots", {})
        subplot_indexes = sorted([i for i in subplot_specs.keys()
                            if str(i).isdigit()])
        figure, subplots = get_figure_subplots(**in_kwargs)

        # Format Figure
        if title is not None:
            set_title(figure, title = title, **in_kwargs)
        if shared_xlabel is not None:
            set_shared_xlabel(figure, xlabel=shared_xlabel, **in_kwargs)
        if shared_ylabel is not None:
            set_shared_ylabel(figure, ylabel=shared_ylabel, **in_kwargs)
        if shared_legend is not None:
            shared_handles = OrderedDict()

        # Configure and plot subplots
        for i in subplot_indexes:
            out_kwargs = subplot_specs[i].copy()
            out_kwargs["verbose"] = in_kwargs.get("verbose", False)
            out_kwargs["debug"] = in_kwargs.get("debug", False)
            out_kwargs["preset"] = in_kwargs.get("preset", [])[:]
            out_kwargs["yaml_dict"] = in_kwargs.get("yaml_dict", {})
            out_kwargs["yaml_keys"] = [key
              for key2 in [[key3 + ["subplots", "all"],
                            key3 + ["subplots", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]
            if shared_legend is not None:
                out_kwargs["shared_handles"] = shared_handles
            if i in subplots:
                self.draw_subplot(subplot = subplots[i], **out_kwargs)

        # Draw legend
        if shared_legend is not None:
            set_shared_legend(figure, subplots, handles = shared_handles,
              **shared_legend)

        # Return results
        return figure

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_subplot(self, subplot, title=None, legend=None,
        shared_handles=None, **in_kwargs):
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
          title (str, optional): Subplot title
          legend (bool, optional): Draw legend on subplot
          shared_handles (OrderedDict, optional): Nascent OrderedDict of
            [labels]:handles shared among subplots of host figure; used
            to draw shared legend
          in_kwargs (dict): Additional keyword arguments
        """
        from collections import OrderedDict
        from .axes import set_xaxis, set_yaxis
        from .legend import set_legend
        from .text import set_title

        # Format
        set_xaxis(subplot, **in_kwargs)
        set_yaxis(subplot, **in_kwargs)
        if title is not None:
            set_title(subplot, title = title, **in_kwargs)

        # Configure and plot datasets
        handles = OrderedDict()
        dataset_specs = in_kwargs.pop("datasets", {})
        dataset_indexes = sorted([i for i in dataset_specs.keys()
                            if str(i).isdigit()])
        for i in dataset_indexes:
            out_kwargs = dataset_specs[i].copy()
            out_kwargs["verbose"] = in_kwargs.get("verbose", False)
            out_kwargs["debug"] = in_kwargs.get("debug", False)
            out_kwargs["preset"] = in_kwargs.get("preset", [])[:]
            out_kwargs["yaml_dict"] = in_kwargs.get("yaml_dict", {})
            out_kwargs["yaml_keys"] = [key
              for key2 in [[key3 + ["datasets", "all"],
                            key3 + ["datasets", i]]
              for key3 in in_kwargs.get("yaml_keys")]
              for key  in key2]
            self.draw_dataset(subplot = subplot, handles = handles,
              **out_kwargs)

        # Draw legend
        if legend is not None and legend is not False:
            set_legend(subplot, handles = handles, **in_kwargs)
        if shared_handles is not None:
            for label, handle in handles.items():
                if label not in shared_handles:
                    shared_handles[label] = handle

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_dataset(self, subplot, infile, label=None, handles=None,
        **kwargs):
        """
        Draws a dataset.

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

    def main(self):
        """
        Provides command-line functionality.
        """
        import argparse
        from inspect import getmodule
        from textwrap import wrap

        full_preset_names = sorted([k for k, v in self.presets.items()
                              if "extends" not in v])
        if len(full_preset_names) == 0:
            epilog = None
        else:
            epilog = "available presets:\n"
            for preset_name in full_preset_names:
                preset = self.presets[preset_name]
                extension_names = sorted([k for k, v in self.presets.items()
                                    if "extends" in v
                                    and v["extends"] == preset_name])
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
                    extension = self.presets[extension_name]
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
        parser = argparse.ArgumentParser(
          description     = getmodule(self.__class__).__doc__,
          formatter_class = argparse.RawTextHelpFormatter,
          epilog          = epilog)

        parser.add_argument(
          "-yaml",
          type     = str,
          required = True,
          dest     = "yaml_dict",
          metavar  = "/PATH/TO/YAML.yaml",
          help     = "YAML configuration file")

        parser.add_argument(
          "-preset",
          type     = str,
          action   = "append",
          metavar  = "PRESET",
          default  = [],
          help     = "Selected preset(s)")

        parser.add_argument(
          "-v",
          "--verbose",
          action   = "count",
          help     = "Enable verbose output, may be specified more than once")

        parser.add_argument(
          "-d",
          "--debug",
          action   = "count",
          help     = "Enable debug output, may be specified more than once")

        arguments = vars(parser.parse_args())

        if arguments["debug"]:
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
