# -*- coding: utf-8 -*-
#   myplotspec.YSpecDataset.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Processes and represents data

  .. note:
    - pandas' MultiIndex only supports dtype of 'object'. It does not appear
      to be possible to force pandas to use a 32 bit float or integer for a
      MultiIndex. _read_hdf5 and _write_hdf5 must behave accordingly
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec")
    import myplotspec
import h5py
import numpy as np
import pandas as pd
from .yspec.YSpecConstructor import YSpecConstructor
################################### CLASSES ###################################
class YSpecDataset(YSpecConstructor):
    """
    Processes and represents data
    """
    from collections import OrderedDict
    from .yspec.plugins.InitializePlugin import InitializePlugin
    from .yspec.plugins.DefaultsPlugin import DefaultsPlugin
    from .yspec.plugins.PresetsPlugin import PresetsPlugin
    from .yspec.plugins.ManualPlugin import ManualPlugin
    from .yspec.plugins.CLArgumentPlugin import CLArgumentPlugin
    from .yspec.plugins.SortPlugin import SortPlugin
    available_plugins = OrderedDict([
      ("initialize", InitializePlugin),
      ("defaults", DefaultsPlugin),
      ("presets", PresetsPlugin),
      ("manual", ManualPlugin),
      ("clargument", CLArgumentPlugin),
      ("sort", SortPlugin)])
    default_plugins = ["initialize", "defaults", "presets", "manual",
                       "clargument", "sort"]
    indexed_levels = """"""
    plugin_config = dict(
      defaults = """
        defaults:
          h5_address: /
          h5_kw:
            chunks: True
            compression: gzip
      """,
      clargument = """
        exclude:
          - constructor
          - source_spec
          - verbose
          - debug
          - interactive
      """,
      sort = """
        header:
          - presets
      """)

    @classmethod
    def construct_argparser(class_, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Intentionally does not call out to parent YSpecConstructor's
        equivalent method

        Arguments:
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser or subparser
        """

        # Process arguments
        parser = class_.get_parser(**kwargs)
        if parser.get_default("class_") is None:
            parser.set_defaults(class_=class_)
        arg_groups = {ag.title: ag for ag in parser._action_groups}
        input_group = arg_groups.get("input",
          parser.add_argument_group("input"))
        action_group = arg_groups.get("action",
          parser.add_argument_group("action"))
        output_group = arg_groups.get("output",
          parser.add_argument_group("output"))

        # Standard arguments
        verbosity = class_.add_mutually_exclusive_argument_group(parser,
          "verbosity")
        class_.add_argument(verbosity,
          "-v", "--verbose",
          action   = "count",
          default  = 1,
          help     = "enable verbose output, may be specified more than once")
        class_.add_argument(verbosity,
          "-q", "--quiet",
          action   = "store_const",
          const    = 0,
          default  = 1,
          dest     = "verbose",
          help     = "disable verbose output")
        class_.add_argument(parser,
          "-d", "--debug",
          action   = "count",
          default  = 1,
          help     = "enable debug output, may be specified more than once")
        class_.add_argument(parser,
          "-I", "--interactive",
          action   = "store_true",
          help     = """enable interactive ipython terminal after loading and
                     processing data""")

        # Input arguments
        class_.add_argument(input_group,
          "-infiles",
          dest     = "infiles",
          metavar  = "INFILE",
          nargs    = "+",
          type     = str,
          help     = """file(s) from which to load data; may be text or hdf5;
                     may contain environment variables and wildcards""")
        class_.add_argument(input_group,
          "-spec",
          dest     = "source_spec",
          metavar  = "SPEC",
          type     = str,
          help     = "file from which to load source spec")

        # Output arguments
        class_.add_argument(output_group,
          "-outfile",
          required = False,
          type     = str,
          help     = """text or hdf5 file to which processed DataFrame will be
                     output; may contain environment variables""")

        # Plugins
        if len(class_.available_plugins) > 0:
            if (hasattr(class_, "default_plugins")
            and len(class_.default_plugins) > 0):
                parser.description += \
                  "\ndefault plugin order:\n  {0}\n\n".format(
                  " → ".join( class_.default_plugins))
            parser.description += "available plugins:\n"
            for name, plugin in class_.available_plugins.items():
                plugin.add_arguments(parser, constructor=class_)

        return parser

    @classmethod
    def construct_spec(class_, source_spec=None, plugins=None, **kwargs):
        """
        Arguments:
          source_spec (str): Path to source spec infile
          plugins (list, optional): Sequence of plugins with which to
            prepare spec
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments

        Returns:
          CommentedMap: Spec
        """
        from ruamel.yaml.comments import CommentedMap
        from .yspec import yaml_load, yaml_dump

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        if source_spec is None:
            source_spec = {}
        else:
            source_spec = yaml_load(source_spec)
        if plugins is None:
            plugins = class_.default_plugins

        # Prepare spec
        spec = CommentedMap()
        for plugin_name in plugins:
            plugin = class_.available_plugins[plugin_name](
                       constructor=class_, **kwargs)
            spec = plugin(spec, source_spec, **kwargs)
            # Output intermediate spec
            if verbose >= 3:
                print("\nSpec after running {0} plugin:".format(plugin_name))
                print(yaml_dump(spec))

        # Output spec
        if verbose >= 2:
            print("\nFinal spec:")
            print(yaml_dump(spec))

        return spec

    @classmethod
    def main(class_):
        """
        """
        parser = class_.construct_argparser()
        kwargs = vars(parser.parse_args())
        kwargs.pop("class_")
        spec = class_.construct_spec(**kwargs)
        return class_(**spec)

#    @classmethod
#    def get_cache_key(class_, infile=None, **kwargs):
#        """
#        Generates tuple of arguments to be used as key for dataset
#        cache.
#
#        .. todo:
#          - Verify that keyword arguments passed to pandas may be safely
#            converted to hashable tuple, and if they cannot throw a
#            warning and load dataset without caching
#        """
#        from os.path import expandvars
#
#        if infile is None:
#            return None
#        read_csv_kw = []
#        for key, value in kwargs.get("read_csv_kw", {}).items():
#            if isinstance(value, list):
#                value = tuple(value)
#            read_csv_kw.append((key, value))
#        return (class_, expandvars(infile), tuple(read_csv_kw))


#    @staticmethod
#    def get_cache_message(cache_key):
#        """
#        Generates message to be used when reloading previously-loaded
#        dataset.
#
#        Arguments:
#          cache_key (tuple): key with which dataset object is stored in
#            dataset cache
#
#        Returns:
#          str: message to be used when reloading previously-loaded
#          dataset
#
#        """
#        return sformat("""Dataset previously loaded from
#          '{0}'""".format(cache_key[1]))
#
#    @staticmethod
#    def add_shared_args(parser, **kwargs):
#        """
#        Adds command line arguments shared by all subclasses.
#
#        Arguments:
#          parser (ArgumentParser): Nascent argument parser to which to
#            add arguments
#          kwargs (dict): Additional keyword arguments
#        """
#        pass
#
#    @staticmethod
#    def process_infiles(**kwargs):
#        """
#        Processes a list of infiles, expanding environment variables and
#        wildcards.
#
#        Arguments:
#          infile{s} (str, list): Paths to infile(s), may contain
#            environment variables and wildcards
#
#        Returns:
#          list: Paths to infiles with environment variables and
#          wildcards expanded
#
#        .. todo:
#          - handle hdf5 addresses smoothly
#        """
#        from glob import glob
#        from os.path import expandvars
#        from . import multi_get_merged
#
#        # Process arguments
#        infiles = multi_get_merged(["infile", "infiles"], kwargs)
#
#        processed_infiles = []
#        for infile in infiles:
#            matching_infiles = sorted(glob(expandvars(infile)))
#            processed_infiles.extend(matching_infiles)
#
#        return processed_infiles
#
#    def __init__(self, infile, address=None, dataset_cache=None,
#        **kwargs):
#        """
#        Initializes dataset.
#
#        Arguments:
#          infile (str): Path to input file, may contain environment
#            variables
#          address (str): Address within hdf5 file from which to load
#            dataset (hdf5 only)
#          slice (slice): Slice to load from hdf5 dataset (hdf5 only)
#          dataframe_kw (dict): Keyword arguments passed to
#            pandas.DataFrame(...) (hdf5 only)
#          read_csv_kw (dict): Keyword arguments passed to
#            pandas.read_csv(...) (text only)
#          verbose (int): Level of verbose output
#          debug (int): Level of debug output
#          kwargs (dict): Additional keyword arguments
#
#        .. todo:
#          - Support loading from pandas format hdf5 (h5_mode?)
#          - Support other pandas input file formats
#          - Implement 'targets' other than pandas DataFrame?
#        """
#        from os.path import expandvars
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        self.dataset_cache = dataset_cache
#
#        # Load dataset
#        if verbose >= 1:
#            wiprint("loading from '{0}'".format(expandvars(infile)))
#        target = "pandas"
#        if target == "pandas":
#
#            if infile.endswith("h5") or infile.endswith("hdf5"):
#                h5_mode = "h5py"
#                if h5_mode == "h5py":
#
#                    dataframe_kw = kwargs.get("dataframe_kw", {})
#                    with h5py.File(expandvars(infile)) as h5_file:
#                        if address is None:
#                            address = sorted(list(h5_file.keys()))[0]
#                        if "slice" in kwargs:
#                            slc = kwargs.pop("slice")
#                            if not isinstance(slc, slice):
#                                slc = slice(*kwargs["slice"])
#                            data = np.array(h5_file[address][slc])
#                        else:
#                            data = np.array(h5_file[address])
#                        attrs = dict(h5_file[address].attrs)
#                        if "fields"  in dataframe_kw:
#                            dataframe_kw["columns"] = \
#                              dataframe_kw.pop("fields")
#                        elif "columns" in dataframe_kw:
#                            pass
#                        elif "fields" in attrs:
#                            dataframe_kw["columns"] = list(attrs["fields"])
#                        elif "columns" in attrs:
#                            dataframe_kw["columns"] = list(attrs["columns"])
#                        self.dataframe = pd.DataFrame(data=data, **dataframe_kw)
#                else:
#                    raise()
#            else:
#                read_csv_kw = dict(index_col=0, delimiter="\s\s+")
#                read_csv_kw.update(kwargs.get("read_csv_kw", {}))
#                if ("delimiter"        in read_csv_kw
#                and "delim_whitespace" in read_csv_kw):
#                    del(read_csv_kw["delimiter"])
#                self.dataframe = pd.read_csv(expandvars(infile), **read_csv_kw)
#                if (self.dataframe.index.name is not None
#                and self.dataframe.index.name.startswith("#")):
#                    self.dataframe.index.name = \
#                      self.dataframe.index.name.lstrip("#")
#
#    def _read_hdf5(self, infile, **kwargs):
#        """
#        Reads DataFrame from hdf5.
#
#        Arguments:
#          infile (str): Path to input hdf5 file and (optionally) address
#            within the file in the form
#            ``/path/to/file.h5:/address/within/file``; may contain
#            environment variables
#          dataframe_kw (dict): Keyword arguments passed to
#            :class:`DataFrame<pandas:pandas.DataFrame>`
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#
#        Returns:
#          DataFrame: DataFrame
#        """
#        from os.path import expandvars
#        import re
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        re_h5 = re.match(
#          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
#          infile, flags=re.UNICODE)
#        path    = expandvars(re_h5.groupdict()["path"])
#        address = re_h5.groupdict()["address"]
#        dataframe_kw = kwargs.get("dataframe_kw", {})
#
#        # Read DataFrame
#        with h5py.File(path) as h5_file:
#            if address is None or address == "":
#                if hasattr(self, "default_hdf5_address"):
#                    address = self.default_hdf5_address
#                else:
#                    address = "/"
#            if verbose >= 1:
#                wiprint("""Reading DataFrame from '{0}:{1}'
#                        """.format(path, address))
#            if ("{0}/values".format(address) in h5_file
#            and "{0}/index".format(address) in h5_file):
#                values = np.array(h5_file["{0}/values".format(address)])
#                index  = np.array(h5_file["{0}/index".format(address)])
#            else:
#                if len(h5_file.keys()) >= 1:
#                    address = sorted(list(h5_file.keys()))[0]
#                values = np.array(h5_file[address])
#                index = np.arange(values.shape[0])
#
#            attrs = dict(h5_file[address].attrs)
#
#            # Read columns from attribute; alternatively may be set
#            # manually in dataframe_kw; previous name was 'fields',
#            # which is retained here for convenience
#            if "fields"  in dataframe_kw:
#                dataframe_kw["columns"] = dataframe_kw.pop("fields")
#            elif "columns" in dataframe_kw:
#                pass
#            elif "fields" in attrs:
#                dataframe_kw["columns"] = list(attrs["fields"])
#            elif "columns" in attrs:
#                dataframe_kw["columns"] = list(attrs["columns"])
#            if "columns" in dataframe_kw:
#                columns = dataframe_kw.pop("columns")
#                if np.array([isinstance(c, np.ndarray) for c in columns]).all():
#                    columns = pd.MultiIndex.from_tuples(map(tuple, columns))
#                if np.array([isinstance(c, tuple) for c in columns]).all():
#                    columns = pd.MultiIndex.from_tuples(columns)
#                dataframe_kw["columns"] = columns
#            if len(index.shape) == 1:
#                df = pd.DataFrame(data=values, index=index, **dataframe_kw)
#                if "index_name" in attrs:
#                    df.index.name = attrs["index_name"]
#            else:
#                index = pd.MultiIndex.from_tuples(map(tuple, index))
#                df = pd.DataFrame(data=values, index=index, **dataframe_kw)
#                if "index_name" in attrs:
#                    df.index.names = attrs["index_name"]
#
#        return df
#
#    def _read_text(self, infile, **kwargs):
#        """
#        Reads DataFrame from text.
#
#        Arguments:
#          infile (str): Path to input file; may contain environment
#            variables
#          read_csv_kw (dict): Keyword arguments passed to
#            :func:`read_csv<pandas.read_csv>`
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#
#        Returns:
#          DataFrame: DataFrame
#        """
#        from os.path import expandvars
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        infile = expandvars(infile)
#        read_csv_kw = dict(index_col=0, delimiter="\s\s+")
#        read_csv_kw.update(kwargs.get("read_csv_kw", {}))
#        if ("delimiter"        in read_csv_kw
#        and "delim_whitespace" in read_csv_kw):
#            del(read_csv_kw["delimiter"])
#
#        # Read DataFrame
#        if verbose >= 1:
#            wiprint("""Reading DataFrame from '{0}' """.format(infile))
#        df = pd.read_csv(infile, **read_csv_kw)
#        if (df.index.name is not None and df.index.name.startswith("#")):
#            df.index.name = df.index.name.lstrip("#")
#
#        return df
#
#    def _write_hdf5(self, outfile, **kwargs):
#        """
#        Writes DataFrame to hdf5.
#
#        Arguments:
#          d{ata}f{rame} (DataFrame): DataFrame to write
#          outfile (str): Path to output hdf5 file and (optionally)
#            address within the file in the form
#            ``/path/to/file.h5:/address/within/file``; may contain
#            environment variables
#          hdf5_kw (dict): Keyword arguments passed to
#            :meth:`create_dataset<h5py:Group.create_dataset>`
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#        """
#        from os.path import expandvars
#        import re
#        import six
#        from . import multi_get
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        df = multi_get(["dataframe", "df"], kwargs)
#        if df is None:
#            if hasattr(self, "dataframe"):
#                df = self.dataframe
#            else:
#                raise Exception("Cannot find DataFrame to write")
#        re_h5 = re.match(
#          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
#          outfile, flags=re.UNICODE)
#        path    = expandvars(re_h5.groupdict()["path"])
#        address = re_h5.groupdict()["address"]
#        if (address is None or address == ""
#        and hasattr(self, "default_h5_address")):
#            address = self.default_h5_address
#        if hasattr(self, "default_h5_kw"):
#            h5_kw = self.default_h5_kw
#        else:
#            h5_kw = {}
#        h5_kw.update(kwargs.get("h5_kw", {}))
#
#        # Write DataFrame
#        if verbose >= 1:
#            print("Writing DataFrame to '{0}'".format(outfile))
#        with h5py.File(path) as hdf5_file:
#            hdf5_file.create_dataset("{0}/values".format(address),
#              data=df.values, dtype=df.values.dtype, **h5_kw)
#            if df.index.values.dtype == object:
#                if type(df.index.values[0]) == tuple:
#                    index = np.array(map(list, df.index.values))
#                else:
#                    index = np.array(map(str, df.index.values))
#            else:
#                index = df.index.values
#
#            hdf5_file.create_dataset("{0}/index".format(address),
#              data=index, dtype=index.dtype, **h5_kw)
#
#            # Process and store columns as an attribute
#            columns = df.columns.tolist()
#            if (np.array([isinstance(c, six.string_types)
#                for c in columns]).all()):
#                # String columns; must make sure all strings are strings
#                #   and not unicode
#                columns = map(str, columns)
#            elif np.array([isinstance(c, tuple) for c in columns]).all():
#                # MultiIndex columns; must make sure all strings are
#                #   strings and not unicode
#                new_columns = []
#                for column in columns:
#                    new_column = []
#                    for c in column:
#                        if isinstance(c, six.string_types):
#                            new_column.append(str(c))
#                        else:
#                            new_column.append(c)
#                    new_columns.append(tuple(new_column))
#                columns = new_columns
#            hdf5_file[address].attrs["columns"] = columns
#
#            # Process and store index name as an attribute
#            if df.index.name is not None:
#                hdf5_file[address].attrs["index_name"] = str(df.index.name)
#            else:
#                hdf5_file[address].attrs["index_name"] = \
#                  map(str, df.index.names)
#
#    def _write_text(self, outfile, **kwargs):
#        """
#        Writes DataFrame to hdf5
#
#        Arguments:
#          d{ata}f{rame} (DataFrame): DataFrame to write
#          outfile (str): Path to output file; may contain environment
#            variables
#          to_string_kw (dict): Keyword arguments passed to
#            :func:`to_string<pandas.DataFrame.to_string>`
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#        """
#        from os.path import expandvars
#        from . import multi_get
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        df = multi_get(["dataframe", "df"], kwargs)
#        if df is None:
#            if hasattr(self, "dataframe"):
#                df = self.dataframe
#            else:
#                raise()
#        outfile = expandvars(outfile)
#        to_string_kw = dict(col_space=12, sparsify=False)
#        to_string_kw.update(kwargs.get("to_string_kw", {}))
#
#        # Write DataFrame
#        if verbose >= 1:
#            print("Writing DataFrame to '{0}'".format(outfile))
#        with open(outfile, "w") as text_file:
#            text_file.write(df.to_string(**to_string_kw))
#
#    def read(self, **kwargs):
#        """
#        Reads data from one or more *infiles* into a DataFrame.
#
#        If more than on *infile* is provided, the resulting DataFrame
#        will consist of their merged data.
#
#        If an *infile* is an hdf5 file path and (optionally) address
#        within the file in the form
#        ``/path/to/file.h5:/address/within/file``, the corresponding
#        DataFrame's values will be loaded from
#        ``/address/within/file/values``, its index will be loaded from
#        ``/address/within/file/index``, its column names will be loaded
#        from the 'columns' attribute of ``/address/within/file`` if
#        present, and index name will be loaded from the 'index_name'
#        attribute of ``/address/within/file`` if present. Additional
#        arguments provided in *dataframe_kw* will be passes to
#        :class:`DataFrame<pandas:pandas.DataFrame>`.
#
#        If an *infile* is the path to a text file, the corresponding
#        DataFrame will be loaded using
#        :func:`read_csv<pandas.read_csv>`, including additional
#        arguments provided in *read_csv_kw*.
#
#        After generating the DataFrame from *infiles*, the index may be
#        set by loading a list of residue names and numbers in the form
#        ``XAA:#`` from *indexfile*. This is useful when loading data
#        from files that do not specify residue names.
#
#        Arguments:
#          infile[s] (str): Path(s) to input file(s); may contain
#            environment variables and wildcards
#          dataframe_kw (dict): Keyword arguments passed to
#            :class:`DataFrame<pandas.DataFrame>` (hdf5 only)
#          read_csv_kw (dict): Keyword arguments passed to
#            :func:`read_csv<pandas.read_csv>` (text only)
#          indexfile (str): Path to index file; may contain environment
#            variables
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#
#        Returns:
#          DataFrame: Sequence DataFrame
#        """
#        import re
#        from . import multi_pop_merged
#
#        # Process arguments
#        infile_args = multi_pop_merged(["infile", "infiles"], kwargs)
#        infiles = self.infiles = self.process_infiles(infiles=infile_args)
#        if len(infiles) == 0:
#            raise Exception(sformat("""No infiles found matching
#            '{0}'""".format(infile_args)))
#        re_h5 = re.compile(
#          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
#          flags=re.UNICODE)
#
#        # Load Data
#        dfs = []
#        for infile in infiles:
#            if re_h5.match(infile):
#                df = self._read_hdf5(infile, **kwargs)
#            else:
#                df = self._read_text(infile, **kwargs)
#            dfs.append(df)
#        df = dfs.pop(0)
#        for df_i in dfs:
#            df = df.merge(df_i, how="outer", left_index=True, right_index=True)
#
#        # Apply dtype
#        if kwargs.get("dtype") is not None:
#            df = df.astype(kwargs.get("dtype"))
#
#        return df
#
#    def write(self, outfile, **kwargs):
#        """
#        Writes DataFrame to text or hdf5.
#
#        If *outfile* is an hdf5 file path and (optionally) address
#        within the file in the form
#        ``/path/to/file.h5:/address/within/file``, DataFrame's values
#        will be written to ``/address/within/file/values``, index will
#        be written to ``/address/within/file/index``, column names will
#        be written to the 'columns' attribute of
#        ``/address/within/file``, and index name will be written to the
#        'index.name' attribute of ``/address/within/file``.
#
#        If *outfile* is the path to a text file, DataFrame will be
#        written using :meth:`to_string<pandas.DataFrame.to_string>`,
#        including additional arguments provided in *read_csv_kw*.
#
#        Arguments:
#          outfile (str): Path to output file; may be path to text file
#            or path to hdf5 file in the form
#            '/path/to/hdf5/file.h5:/address/within/hdf5/file'; may
#            contain environment variables
#          hdf5_kw (dict): Keyword arguments passed to
#            :meth:`create_dataset<h5py:Group.create_dataset>` (hdf5
#            only)
#          read_csv_kw (dict): Keyword arguments passed to
#            :meth:`to_string<pandas.DataFrame.to_string>` (text only)
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#        """
#        from os.path import expandvars
#        import re
#
#        # Process arguments
#        outfile = expandvars(outfile)
#        re_h5 = re.match(
#          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
#          outfile, flags=re.UNICODE)
#
#        # Write DataFrame
#        if re_h5:
#            self._write_hdf5(outfile=outfile, **kwargs)
#        else:
#            self._write_text(outfile=outfile, **kwargs)
#
#    @staticmethod
#    def calc_pdist(df, columns=None, mode="kde", bandwidth=None, grid=None,
#        **kwargs):
#        """
#        Calcualtes probability distribution over DataFrame.
#
#        Arguments:
#          df (DataFrame): DataFrame over which to calculate probability
#            distribution of each column over rows
#          columns (list): Columns for which to calculate probability
#            distribution
#          mode (ndarray, str, optional): Method of calculating
#            probability distribution; eventually will support 'hist' for
#            histogram and 'kde' for kernel density estimate, though
#            presently only 'kde' is implemented
#          bandwidth (float, dict, str, optional): Bandwidth to use for
#            kernel density estimates; may be a single float that will be
#            applied to all columns or a dictionary whose keys are column
#            names and values are floats corresponding to the bandwidth
#            for each column; for any column for which *bandwidth* is not
#            specified, the standard deviation will be used
#          grid (list, ndarray, dict, optional): Grid on which to
#            calculate kernel density estimate; may be a single ndarray
#            that will be applied to all columns or a dictionary whose
#            keys are column names and values are ndarrays corresponding
#            to the grid for each column; for any column for which *grid*
#            is not specified, a grid of 1000 points between the minimum
#            value minus three times the standard deviation and the
#            maximum value plots three times the standard deviation will
#            be used
#          kde_kw (dict, optional): Keyword arguments passed to
#            :function:`sklearn.neighbors.KernelDensity`
#          verbose (int): Level of verbose output
#          kwargs (dict): Additional keyword arguments
#
#        Returns:
#          OrderedDict: Dictionary whose keys are columns in *df* and
#          values are DataFrames whose indexes are the *grid* for that
#          column and contain a single column 'probability' containing
#          the normalized probability at each grid point
#
#        .. todo:
#            - Implement flag to return single dataframe with single grid
#        """
#        from collections import OrderedDict
#        import six
#        from sklearn.neighbors import KernelDensity
#
#        # Process arguments
#        verbose = kwargs.get("verbose", 1)
#        if verbose >= 1:
#            wiprint("""Calculating probability distribution over DataFrame""")
#        if columns is None:
#            columns = [a for a in df.columns.values
#                       if str(df[a].dtype).startswith("float")]
#        elif isinstance(columns, six.string_types):
#            columns = [columns]
#
#        if mode == "kde":
#
#            # Prepare bandwidths
#            if bandwidth is None:
#                all_bandwidth = None
#                bandwidth = {}
#            elif isinstance(bandwidth, float):
#                all_bandwidth = bandwidth
#                bandwidth = {}
#            elif isinstance(bandwidth, dict):
#                all_bandwidth = None
#            else:
#                raise Exception()
#            for column, series in df.iteritems():
#                if column in bandwidth:
#                    bandwidth[column] = float(bandwidth[column])
#                elif all_bandwidth is not None:
#                    bandwidth[column] = all_bandwidth
#                else:
#                    bandwidth[column] = series.std()
#
#            # Prepare grids
#            if grid is None:
#                all_grid = None
#                grid = {}
#            elif isinstance(grid, list) or isinstance(grid, np.ndarray):
#                all_grid = np.array(grid)
#                grid = {}
#            elif isinstance(grid, dict):
#                all_grid = None
#            for column, series in df.iteritems():
#                if column in grid:
#                    grid[column] = np.array(grid[column])
#                elif all_grid is not None:
#                    grid[column] = all_grid
#                else:
#                    grid[column] = np.linspace(
#                      series.min() - 3 * series.std(),
#                      series.max() + 3 * series.std(), 1000)
#
#            # Calculate probability distributions
#            kde_kw = kwargs.get("kde_kw", {})
#            pdist = OrderedDict()
#            for column, series in df.iteritems():
#                if verbose >= 1:
#                   wiprint("calculating probability distribution of "
#                    "{0} using a kernel density estimate".format(column))
#                kde = KernelDensity(bandwidth=bandwidth[column], **kde_kw)
#                kde.fit(series[:, np.newaxis])
#                pdf = np.exp(kde.score_samples(grid[column][:, np.newaxis]))
#                pdf /= pdf.sum()
#                series_pdist = pd.DataFrame(pdf, index=grid[column],
#                  columns=["probability"])
#                series_pdist.index.name = column
#                pdist[column] = series_pdist
#        else:
#            raise Exception(sformat("""only kernel density estimation is
#                                    currently supported"""))
#
#        return pdist
#
#    def load_dataset(self, class_=None, **kwargs):
#        """
#        Loads a dataset, or reloads a previously-loaded dataset from a
#        cache
#
#        Arguments:
#          class_ (class, str): Dataset class; may be either class object
#            itself or name of class in form of 'package.module.class';
#            if None, will be set to self.__class__; if '__noclass__',
#            function will return None
#
#        Returns:
#          object: Dataset, either newly initialized or copied from cache
#        """
#        from . import load_dataset
#
#        if class_ is None:
#            class_ = type(self)
#        return load_dataset(class_=class_,
#                 dataset_cache=self.dataset_cache, **kwargs)

#################################### MAIN #####################################
if __name__ == "__main__":
    YSpecDataset.main()
