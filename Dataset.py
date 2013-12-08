#!/usr/bin/python
desc = """Dataset.py
    Class for organizing HDF5 data for plotting
    Written by Karl Debiec on 12-10-22
    Last updated 13-11-30"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys
import numpy as np
from   MD_toolkit.HDF5_File import HDF5_File
####################################################### CLASSES ########################################################
class Dataset:
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
                    try:    self.data[key]  = hdf5_file[key]
                    except: pass
                    try:    self.attrs[key] = hdf5_file.attrs(key)
                    except: pass


