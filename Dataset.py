# -*- coding: utf-8 -*-
#   myplotspec.Dataset.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages datasets and implements caching.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class Dataset(object):
    """
    Manages datasets and implements caching.

    .. todo:
      - Support smooth reading of other pandas formats (e.g. hdf5)
    """

    @classmethod
    def get_cache_key(cls, infile, *args, **kwargs):
        """
        Generates tuple of arguments to be used as key for dataset
        cache.

        .. todo:
          - Verify that keyword arguments passed to pandas may be safely
            converted to hashable tuple, and if they cannot throw a
            warning and load dataset without memoization
        """
        from os.path import expandvars

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

    @staticmethod
    def load_dataset(cls=None, dataset_cache=None, **kwargs):
        """
        Loads a dataset, or reloads a previously-loaded dataset.

        Datasets are stored in `dataset_cache`, a dictionary containing
        copies of previously loaded datasets keyed by tuples containing
        the class and arguments used to instantiate the dataset.

        In order to support caching, a class must implement the static
        method 'get_cache_key', which generates the hashable tuple key.
        Only arguments that affect the resulting dataset should be
        included in the key (e.g. 'infile' should be included, but
        'verbose' and 'debug' should not). If the function accepts
        arguments that are not hashable or convertable into a hashable
        form, 'get_cache_key' should return None, causing
        :meth:`load_dataset` to reload the dataset.

        Cachable dataset classes may also implement the method
        'get_cache_message' which returns a message to display when the
        dataset is loaded from the cache.

        Arguments:
          cls (class): Dataset class
          dataset_cache (dict, optional): Cache of previously-loaded
            datasets
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Keyword arguments passed to cls.get_cache_key()
            and cls.__init__()

        Returns:
          dataset (cls): Dataset, either newly initialized or copied
          from cache
        """
        from inspect import getargspec
        from warnings import warn
        from .debug import db_s
        from .error import (is_argument_error, MPSArgumentError,
                            MPSDatasetError, MPSDatasetCacheError)

        if cls is None:
            cls = Dataset
        verbose = kwargs.get("verbose", 1)
        debug   = kwargs.get("debug",   0)

        if dataset_cache is not None and hasattr(cls, "get_cache_key"):
            try:
                cache_key = cls.get_cache_key(**kwargs)
            except TypeError as error:
                if is_argument_error(error):
                    error = MPSArgumentError(error, cls.get_cache_key,
                      kwargs, cls, "cls")
                raise MPSDatasetCacheError(error)
            if cache_key is None:
                try:
                    return cls(dataset_cache=dataset_cache, **kwargs)
                except TypeError as error:
                    if is_argument_error(error):
                        error = MPSArgumentError(error, cls.get_cache_key,
                          kwargs, cls, "cls")
                    raise MPSDatasetError(error)
            if cache_key in dataset_cache:
                if verbose >= 1:
                    if hasattr(cls, "get_cache_message"):
                        print(cls.get_cache_message(cache_key))
                    else:
                        print("Previously loaded")
                return dataset_cache[cache_key]
            else:
                try:
                    dataset_cache[cache_key] = cls(
                      dataset_cache=dataset_cache, **kwargs)
                except TypeError as error:
                    if is_argument_error(error):
                        error = MPSArgumentError(error, cls.get_cache_key,
                          kwargs, cls, "cls")
                    raise MPSDatasetError(error)
                return dataset_cache[cache_key]
        else:
            return cls(**kwargs)

    def __init__(self, infile, verbose=1, debug=0, **kwargs):
        """
        Initializes dataset.

        Arguments:
          infile (str): Path to input text file, may contain environment
            variables
          verbose (int): Level of verbose output
          debug (int): Level of debug output
          kwargs (dict): Additional keyword arguments
        """
        from os.path import expandvars
        import pandas as pd

        # Load dataset
        read_csv_kw = kwargs.get("read_csv_kw", {})
        if verbose >= 1:
            print("loading from '{0}'".format(expandvars(infile)))
        self.data = pd.read_csv(expandvars(infile), **read_csv_kw)
