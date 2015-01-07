#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Dataset.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec on 15-01-04
"""
Class for managing datasets
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
################################### CLASSES ####################################
class Dataset(object):
    """
    Class for managing datasets
    """
    def __init__(self, **kwargs):
        """
        Initializes

        **Arguments:**
            :*infiles*: Paths to infiles
            :*infile*:  Paths to single infile
            :*kwargs*:  Added as attributes
        """
        self.datasets = {}
        self.attrs    = {}

        if  "infiles" in kwargs:
            infiles = kwargs.pop("infiles")
        elif "infile" in kwargs:
            infiles = [infile]
        self.load(infiles, **kwargs)
            
#        for key, value in kwargs.iteritems():
#            setattr(self, key, value)

    def load(self, infiles, **kwargs):
        """
        Loads data from text using np.loadtxt
        
        **Arguments:**
            :*infiles*: Paths to infiles
        """
        from warnings import warn
        import numpy as np

        for infile in infiles:
            if   len(infile) == 1:
                in_path = infile 
                out_key = in_path
            elif len(infile) == 2:
                in_path, out_key = infile

            if not os.path.isfile(in_path):
                print("File {0} not found".format(in_path))
                continue

            data = np.loadtxt(in_path, **kwargs)
            self.datasets[out_key] = np.array(dataset)
            print("Loaded Dataset {0}; Stored at {1}".format(
                  in_path, out_key))
