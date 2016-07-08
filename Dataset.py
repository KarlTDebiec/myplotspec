# -*- coding: utf-8 -*-
#   myplotspec.Dataset.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages datasets and implements caching.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
import h5py
import numpy as np
import pandas as pd
from . import sformat, wiprint
################################### CLASSES ###################################
class Dataset(object):
    """
    Represents data.
    """

    default_h5_address = "dataset"

    @classmethod
    def get_cache_key(cls, infile=None, **kwargs):
        """
        Generates tuple of arguments to be used as key for dataset
        cache.

        .. todo:
          - Verify that keyword arguments passed to pandas may be safely
            converted to hashable tuple, and if they cannot throw a
            warning and load dataset without caching
        """
        from os.path import expandvars

        if infile is None:
            return None
        read_csv_kw = []
        for key, value in kwargs.get("read_csv_kw", {}).items():
            if isinstance(value, list):
                value = tuple(value)
            read_csv_kw.append((key, value))
        return (cls, expandvars(infile), tuple(read_csv_kw))

    @staticmethod
    def get_cache_message(cache_key):
        """
        Generates message to be used when reloading previously-loaded
        dataset.

        Arguments:
          cache_key (tuple): key with which dataset object is stored in
            dataset cache
          hand (stump): asdf asdf asdfasdf asdf asdf asd f asdf asdf asd
            fa sdfa sdf asd fafsd 

        Returns:
          str: message to be used when reloading previously-loaded
          dataset

        """
        return sformat("""Dataset previously loaded from
          '{0}'""".format(cache_key[1]))

    @staticmethod
    def add_shared_args(parser, **kwargs):
        """
        Adds command line arguments shared by all subclasses.

        Arguments:
          parser (ArgumentParser): Nascent argument parser to which to
            add arguments
          kwargs (dict): Additional keyword arguments
        """
        verbosity = parser.add_mutually_exclusive_group()
        verbosity.add_argument(
          "-v", "--verbose",
          action   = "count",
          default  = 1,
          help     = "enable verbose output, may be specified more than once")
        verbosity.add_argument(
          "-q", "--quiet",
          action   = "store_const",
          const    = 0,
          default  = 1,
          dest     = "verbose",
          help     = "disable verbose output")
        parser.add_argument(
          "-d", "--debug",
          action   = "count",
          default  = 1,
          help     = "enable debug output, may be specified more than once")
        parser.add_argument(
          "-I", "--interactive",
          action   = "store_true",
          help     = """enable interactive ipython terminal after loading and
                      processing data""")

    @staticmethod
    def process_infiles(**kwargs):
        """
        Processes a list of infiles, expanding environment variables and
        wildcards.

        Arguments:
          infile[s] (str, list): Paths to infile(s), may contain environment
            variables and wildcards

        Returns:
          processed_infiles (list): Paths to infiles with environment
            variables and wildcards expanded

        .. todo:
          - handle hdf5 addresses smoothly
        """
        from glob import glob
        from os.path import expandvars
        from . import multi_get_merged

        # Process arguments
        infiles = multi_get_merged(["infile", "infiles"], kwargs)

        processed_infiles = []
        for infile in infiles:
            matching_infiles = sorted(glob(expandvars(infile)))
            processed_infiles.extend(matching_infiles)

        return processed_infiles

    def __init__(self, infile, address=None, dataset_cache=None,
        **kwargs):
        """
        Initializes dataset.

        Arguments:
          infile (str): Path to input file, may contain environment
            variables
          address (str): Address within hdf5 file from which to load
            dataset (hdf5 only)
          slice (slice): Slice to load from hdf5 dataset (hdf5 only)
          dataframe_kw (dict): Keyword arguments passed to
            pandas.DataFrame(...) (hdf5 only)
          read_csv_kw (dict): Keyword arguments passed to
            pandas.read_csv(...) (text only)
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments

        .. todo:
          - Support loading from pandas format hdf5 (h5_mode?)
          - Support other pandas input file formats
          - Implement 'targets' other than pandas DataFrame?
        """
        from os.path import expandvars

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        self.dataset_cache = dataset_cache

        # Load dataset
        if verbose >= 1:
            wiprint("loading from '{0}'".format(expandvars(infile)))
        target = "pandas"
        if target == "pandas":

            if infile.endswith("h5") or infile.endswith("hdf5"):
                h5_mode = "h5py"
                if h5_mode == "h5py":

                    dataframe_kw = kwargs.get("dataframe_kw", {})
                    with h5py.File(expandvars(infile)) as h5_file:
                        if address is None:
                            address = sorted(list(h5_file.keys()))[0]
                        if "slice" in kwargs:
                            slc = kwargs.pop("slice")
                            if not isinstance(slc, slice):
                                slc = slice(*kwargs["slice"])
                            data = np.array(h5_file[address][slc])
                        else:
                            data = np.array(h5_file[address])
                        attrs = dict(h5_file[address].attrs)
                        if "fields"  in dataframe_kw:
                            dataframe_kw["columns"] = \
                              dataframe_kw.pop("fields")
                        elif "columns" in dataframe_kw:
                            pass
                        elif "fields" in attrs:
                            dataframe_kw["columns"] = list(attrs["fields"])
                        elif "columns" in attrs:
                            dataframe_kw["columns"] = list(attrs["columns"])
                        self.dataframe = pd.DataFrame(data=data, **dataframe_kw)
                else:
                    raise()
            else:
                read_csv_kw = dict(index_col=0, delimiter="\s\s+")
                read_csv_kw.update(kwargs.get("read_csv_kw", {}))
                if ("delimiter"        in read_csv_kw
                and "delim_whitespace" in read_csv_kw):
                    del(read_csv_kw["delimiter"])
                self.dataframe = pd.read_csv(expandvars(infile), **read_csv_kw)
                if (self.dataframe.index.name is not None
                and self.dataframe.index.name.startswith("#")):
                    self.dataframe.index.name = \
                      self.dataframe.index.name.lstrip("#")

    def _read_hdf5(self, infile, **kwargs):
        """
        Reads DataFrame from hdf5.

        Arguments:
          infile (str): Path to input hdf5 file and (optionally) address
            within the file in the form
            ``/path/to/file.h5:/address/within/file``; may contain
            environment variables
          dataframe_kw (dict): Keyword arguments passed to
            :class:`DataFrame<pandas:pandas.DataFrame>`
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments

        Returns:
          DataFrame: DataFrame
        """
        from os.path import expandvars
        import re

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        re_h5 = re.match(
          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
          infile, flags=re.UNICODE)
        path    = expandvars(re_h5.groupdict()["path"])
        address = re_h5.groupdict()["address"]
        dataframe_kw = kwargs.get("dataframe_kw", {})

        # Read DataFrame
        with h5py.File(path) as h5_file:
            if address is None or address == "":
                if hasattr(self, "default_hdf5_address"):
                    address = self.default_hdf5_address
                else:
                    address = sorted(list(h5_file.keys()))[0]
                if verbose >= 1:
                    wiprint("""Reading DataFrame from '{0}:{1}'
                            """.format(path, address))
                if ("{0}/values".format(address) in h5_file
                and "{0}/index".format(address) in h5_file):
                    values = np.array(h5_file["{0}/values".format(address)])
                    index  = np.array(h5_file["{0}/index".format(address)])
                else:
                    values = np.array(h5_file[address])
                    index = np.arange(values.shape[0])
                attrs  = dict(h5_file[address].attrs)
                if "fields"  in dataframe_kw:
                    dataframe_kw["columns"] = dataframe_kw.pop("fields")
                elif "columns" in dataframe_kw:
                    pass
                elif "fields" in attrs:
                    dataframe_kw["columns"] = list(attrs["fields"])
                elif "columns" in attrs:
                    dataframe_kw["columns"] = list(attrs["columns"])
                if "columns" in dataframe_kw:
                    columns = dataframe_kw.pop("columns")
                    columns = map(str, columns)
                    if np.array([isinstance(c, tuple) for c in columns]).all():
                        columns = pd.MultiIndex.from_tuples(columns)
                    dataframe_kw["columns"] = columns
                df = pd.DataFrame(data=values, index=index, **dataframe_kw)
                if "index_name" in attrs:
                    df.index.name = attrs["index_name"]

        return df

    def _read_text(self, infile, **kwargs):
        """
        Reads DataFrame from text.

        Arguments:
          infile (str): Path to input file; may contain environment
            variables
          read_csv_kw (dict): Keyword arguments passed to
            :func:`read_csv<pandas.read_csv>`
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments

        Returns:
          DataFrame: DataFrame
        """
        from os.path import expandvars

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        infile = expandvars(infile)
        read_csv_kw = dict(index_col=0, delimiter="\s\s+")
        read_csv_kw.update(kwargs.get("read_csv_kw", {}))
        if ("delimiter"        in read_csv_kw
        and "delim_whitespace" in read_csv_kw):
            del(read_csv_kw["delimiter"])

        # Read DataFrame
        if verbose >= 1:
            wiprint("""Reading DataFrame from '{0}' """.format(infile))
        df = pd.read_csv(infile, **read_csv_kw)
        if (df.index.name is not None and df.index.name.startswith("#")):
            df.index.name = df.index.name.lstrip("#")

        return df

    def _write_hdf5(self, outfile, **kwargs):
        """
        Writes DataFrame to hdf5.

        Arguments:
          df (DataFrame): DataFrame to write
          outfile (str): Path to output hdf5 file and (optionally)
            address within the file in the form
            ``/path/to/file.h5:/address/within/file``; may contain
            environment variables
          hdf5_kw (dict): Keyword arguments passed to
            :meth:`create_dataset<h5py:Group.create_dataset>`
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        from os.path import expandvars
        import re

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        df      = kwargs.get("df")
        if df is None:
            if hasattr(self, "dataframe"):
                df = self.dataframe
            else:
                raise()
        re_h5 = re.match(
          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
          outfile, flags=re.UNICODE)
        path    = expandvars(re_h5.groupdict()["path"])
        address = re_h5.groupdict()["address"]
        if (address is None or address == ""
        and hasattr(self, "default_hdf5_address")):
            address = self.default_hdf5_address
        if hasattr(self, "default_hdf5_kw"):
            h5_kw = self.default_hdf5_kw
        else:
            h5_kw = {}
        h5_kw.update(kwargs.get("hdf5_kw", {}))

        # Write DataFrame
        if verbose >= 1:
            print("Writing sequence DataFrame to '{0}'".format(outfile))
        with h5py.File(path) as hdf5_file:
            hdf5_file.create_dataset("{0}/values".format(address),
              data=df.values, **h5_kw)
            hdf5_file.create_dataset("{0}/index".format(address),
              data=np.array(df.index.values, np.str))
            hdf5_file[address].attrs["columns"] = \
              map(str, df.columns.tolist())
            hdf5_file[address].attrs["index_name"] = \
              str(df.index.name)

    def _write_text(self, outfile, **kwargs):
        """
        Writes DataFrame to hdf5

        Arguments:
          df (DataFrame): DataFrame to write
          outfile (str): Path to output file; may contain environment
            variables
          to_string_kw (dict): Keyword arguments passed to
            :func:`to_string<pandas.DataFrame.to_string>`
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        from os.path import expandvars

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        df      = kwargs.get("df")
        if df is None:
            if hasattr(self, "dataframe"):
                df = self.dataframe
            else:
                raise()
        outfile = expandvars(outfile)
        to_string_kw = dict(col_space=12, sparsify=False)
        to_string_kw.update(kwargs.get("to_string_kw", {}))

        # Write DataFrame
        if verbose >= 1:
            print("Writing sequence DataFrame to '{0}'".format(outfile))
        with open(outfile, "w") as text_file:
            text_file.write(df.to_string(**to_string_kw))

    def read(self, **kwargs):
        """
        Reads data from one or more *infiles* into a DataFrame.

        If more than on *infile* is provided, the resulting DataFrame
        will consist of their merged data.

        If an *infile* is an hdf5 file path and (optionally) address
        within the file in the form
        ``/path/to/file.h5:/address/within/file``, the corresponding
        DataFrame's values will be loaded from
        ``/address/within/file/values``, its index will be loaded from
        ``/address/within/file/index``, its column names will be loaded
        from the 'columns' attribute of ``/address/within/file`` if
        present, and index name will be loaded from the 'index_name'
        attribute of ``/address/within/file`` if present. Additional
        arguments provided in *dataframe_kw* will be passes to
        :class:`DataFrame<pandas:pandas.DataFrame>`.

        If an *infile* is the path to a text file, the corresponding
        DataFrame will be loaded using
        :func:`read_csv<pandas.read_csv>`, including additional
        arguments provided in *read_csv_kw*.

        After generating the DataFrame from *infiles*, the index may be
        set by loading a list of residue names and numbers in the form
        ``XAA:#`` from *indexfile*. This is useful when loading data
        from files that do not specify residue names.

        Arguments:
          infile[s] (str): Path(s) to input file(s); may contain
            environment variables and wildcards
          dataframe_kw (dict): Keyword arguments passed to
            :class:`DataFrame<pandas.DataFrame>` (hdf5 only)
          read_csv_kw (dict): Keyword arguments passed to
            :func:`read_csv<pandas.read_csv>` (text only)
          indexfile (str): Path to index file; may contain environment
            variables
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments

        Returns:
          DataFrame: Sequence DataFrame
        """
        import re
        from . import multi_pop_merged

        # Process arguments
        infile_args = multi_pop_merged(["infile", "infiles"], kwargs)
        infiles = self.infiles = self.process_infiles(infiles=infile_args)
        if len(infiles) == 0:
            raise Exception(sformat("""No infiles found matching
            '{0}'""".format(infile_args)))
        re_h5 = re.compile(
          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
          flags=re.UNICODE)

        # Load Data
        dfs = []
        for infile in infiles:
            if re_h5.match(infile):
                df = self._read_hdf5(infile, **kwargs)
            else:
                df = self._read_text(infile, **kwargs)
            dfs.append(df)
        df = dfs.pop(0)
        for df_i in dfs:
            df.merge(df_i)

        return df

    def write(self, outfile, **kwargs):
        """
        Writes DataFrame to text or hdf5.

        If *outfile* is an hdf5 file path and (optionally) address
        within the file in the form
        ``/path/to/file.h5:/address/within/file``, DataFrame's values
        will be written to ``/address/within/file/values``, index will
        be written to ``/address/within/file/index``, column names will
        be written to the 'columns' attribute of
        ``/address/within/file``, and index name will be written to the
        'index.name' attribute of ``/address/within/file``.

        If *outfile* is the path to a text file, DataFrame will be
        written using :meth:`to_string<pandas.DataFrame.to_string>`,
        including additional arguments provided in *read_csv_kw*.

        Arguments:
          outfile (str): Path to output file; may be path to text file
            or path to hdf5 file in the form
            '/path/to/hdf5/file.h5:/address/within/hdf5/file'; may
            contain environment variables
          hdf5_kw (dict): Keyword arguments passed to
            :meth:`create_dataset<h5py:Group.create_dataset>` (hdf5
            only)
          read_csv_kw (dict): Keyword arguments passed to
            :meth:`to_string<pandas.DataFrame.to_string>` (text only)
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        from os.path import expandvars
        import re

        # Process arguments
        outfile = expandvars(outfile)
        re_h5 = re.match(
          r"^(?P<path>(.+)\.(h5|hdf5))((:)?(/)?(?P<address>.+))?$",
          outfile, flags=re.UNICODE)

        # Write DataFrame
        if re_h5:
            self._write_hdf5(outfile=outfile, **kwargs)
        else:
            print(kwargs)
            self._write_text(outfile=outfile, **kwargs)

    def load_dataset(self, cls=None, **kwargs):
        """
        """
        from . import load_dataset

        if cls is None:
            cls = type(self)
        return load_dataset(cls=cls,
                 dataset_cache=self.dataset_cache, **kwargs)
