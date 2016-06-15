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
################################### CLASSES ###################################
class Dataset(object):
    """
    Manages datasets and implements caching.
    """

    @classmethod
    def get_cache_key(cls, infile=None, *args, **kwargs):
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
            cache_key (tuple): key with which dataset object is stored
              in dataset cache

        Returns:
            cache_message (str): message to be used when reloading
              previously-loaded dataset
        """
        return "Dataset previously loaded from '{0}'".format(cache_key[1])

    def load_dataset(self, **kwargs):
        """
        """
        from . import load_dataset

        return load_dataset(cls=type(self),
                 dataset_cache=self.dataset_cache, **kwargs)

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

        verbose = kwargs.get("verbose", 1)
        self.dataset_cache = dataset_cache

        # Load dataset
        if verbose >= 1:
            print("loading from '{0}'".format(expandvars(infile)))
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
                read_csv_kw = kwargs.get("read_csv_kw", {})
                self.dataframe = pd.read_csv(expandvars(infile), **read_csv_kw)
                if (self.dataframe.index.name is not None
                and self.dataframe.index.name.startswith("#")):
                    self.dataframe.index.name = \
                      self.dataframe.index.name.lstrip("#")
