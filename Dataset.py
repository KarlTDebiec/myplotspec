#!/usr/bin/python
#   Dataset.py
#   Written by Karl Debiec on 12-10-22
#   Last updated by Karl Debiec on 14-04-04
####################################################### MODULES ########################################################
import os, sys
import numpy as np
from   MD_toolkit.HDF5_File import HDF5_File
####################################################### CLASSES ########################################################
class Dataset:
    """
    Class for organizing datasets for plotting. Accepts a dictionary of H5 files and paths to data or attributes within
    those H5 files. Opens the H5 files, loads those data and attributes, and closes the H5 files.

    **Initialization Arguments:**
        :*infiles*: Dictionary of input files; each key is the path to an H5 file, and each value is a list of
                    addresses to be loaded within that file
        :*label*:   Dataset label (default = filename of first H5 File)
        :*color*:   Dataset color (default = gray)
        :*kwargs*:  All other keyword arguments are assigned as properties (i.e. self.key = value)

    **Properties:**
        :*infile*:  Name of first infile
        :*label*:   Dataset label
        :*color*:   Dataset color
        :*data*:    Dictionary of data; each key is the address of the data in its source H5 File, and each value is
                    that data
        :*attrs*:   Dictionary of attrs; each key is the address of the data or group in its source H5 File, and each
                    value is a dictionary containing the attributes of that data or group

    """
    def __init__(self, infiles, verbose = True, **kwargs):
        self.infile     = infiles.keys()[0].split("/")[-2]

        if not hasattr(self, "label"):
            self.label = kwargs.pop("label", self.infile)

        if not hasattr(self, "color"):
            self.color = kwargs.pop("color", [0.5, 0.5, 0.5])

        for key, value in kwargs.iteritems():
            eval("self.{0} = {1}".format(key, value))

        self.data   = {}
        self.attrs  = {}
        for infile, keys in infiles.iteritems():
            if verbose:
                print "Loading data from {0}".format(infile)
            with HDF5_File(infile) as hdf5_file:
                for key in keys:
                    key     = hdf5_file._strip_path(key)
                    if verbose and not key in hdf5_file: print "WARNING: COULD NOT LOAD '{0}' FROM '{1}'".format(key, infile)
                    try:    self.data[key]  = hdf5_file[key]
                    except: pass
                    try:    self.attrs[key] = hdf5_file.attrs(key)
                    except: pass


