#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Dataset.py
#   Written:    Karl Debiec     12-10-22
#   Updated:    Karl Debiec     15-01-10
"""
Class for managing datasets
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class Dataset(object):
    """
    Class for managing datasets
    """
    def __init__(self, verbose = True, debug = False, **kwargs):
        """
        Initializes

        **Arguments:**
            :*infiles*: List of paths to infiles
            :*infile*:  Path to single infile
            :*kwargs*:  Added as attributes
            :*verbose*: Enable verbose output
            :*debug*:   Enable debug output
        """
        self.datasets = {}
        self.verbose  = verbose
        self.debug    = debug

        if   "infiles" in kwargs:
            infiles = kwargs.pop("infiles")
        elif "infile" in kwargs:
            infiles = [kwargs.pop("infile")]
        else:
            infiles = []
        self.load(infiles, **kwargs)

    def load(self, infiles, **kwargs):
        """
        Loads data from text using np.loadtxt

        **Arguments:**
            :*infiles*: Paths to infiles
        """
        from os.path import isfile
        import six
        import numpy as np

        for infile in infiles:
            if isinstance(infile, six.string_types):
                in_path = out_key = infile
            elif isinstance(infile, list):
                if len(infile) == 1:
                    in_path = infile
                    out_key = in_path
                elif len(infile) == 2:
                    in_path, out_key = infile

            if not isfile(in_path):
                if self.verbose:
                    print("File {0} not found".format(in_path))
                continue

            if in_path.endswith("npy"):
                dataset = np.load(in_path)
            else:
                dataset = np.loadtxt(in_path)
            self.datasets[out_key] = np.array(dataset)
            if self.verbose:
                print("Loaded Dataset {0}; Stored at {1}".format(
                      in_path, out_key))
