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
    def __init__(self, **kwargs):
        """
        Initializes

        **Arguments:**
            :*infiles*: List of Paths to infiles
            :*infile*:  Path to single infile
            :*kwargs*:  Added as attributes
        """
        self.datasets = {}
        self.attrs    = {}

        if   "infiles" in kwargs:
            infiles = kwargs.pop("infiles")
        elif "infile" in kwargs:
            infiles = [infile]
        self.load(infiles, **kwargs)

    def load(self, infiles, **kwargs):
        """
        Loads data from text using np.loadtxt

        **Arguments:**
            :*infiles*: Paths to infiles
        """
        from os import isfile
        from warnings import warn

        for infile in infiles:
            if   len(infile) == 1:
                in_path = infile
                out_key = in_path
            elif len(infile) == 2:
                in_path, out_key = infile

            if not isfile(in_path):
                print("File {0} not found".format(in_path))
                continue

            if in_path.endswith("npy"):
                data = np.load(in_path, **kwargs)
            else:
                data = np.loadtxt(in_path, **kwargs)
            self.datasets[out_key] = np.array(dataset)
            print("Loaded Dataset {0}; Stored at {1}".format(
                  in_path, out_key))
