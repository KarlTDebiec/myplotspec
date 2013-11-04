#!/usr/bin/python
desc = """Molecular_Association_Dataset.py
    Class for organizing HDF5 data from molecular association trajectories for plotting
    Written by Karl Debiec on 13-10-22
    Last updated 13-11-31"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys
import numpy as np
sys.path   += ["/share/home/ktd3/scripts/"]
from plot_toolkit.Dataset import Dataset
from plot_toolkit         import hsl_to_rgb
####################################################### CLASSES ########################################################
default_labels  = {"AMBER03":       "AMBER03",                      "AMBER99SBILDN": "AMBER99",
                   "AMBERIPOLQ":    "AMBER13$\\alpha$",             "AMBER13ALPHA":  "AMBER13$\\alpha$",
                   "GAFF":          "GAFF",                         "CHARMM27":      "CHARMM22",
                   "CHARMM22STAR":  "CHARMM22*",                    "CHARMM36":      "CHARMM36",
                   "CGENFF":        "CGENFF",                       "OPLSAAL":       "OPLS-AA/L"}
default_colors  = {"AMBER03":       hsl_to_rgb(0.00, 1.00, 0.10),   "AMBER99SBILDN": hsl_to_rgb(0.00, 1.00, 0.45),
                   "AMBERIPOLQ":    hsl_to_rgb(0.00, 1.00, 0.80),   "AMBER13ALPHA":  hsl_to_rgb(0.00, 1.00, 0.80),
                   "GAFF":          hsl_to_rgb(0.20, 1.00, 0.50),   "CHARMM27":      hsl_to_rgb(0.40, 1.00, 0.10),
                   "CHARMM22STAR":  hsl_to_rgb(0.40, 1.00, 0.45),   "CHARMM36":      hsl_to_rgb(0.40, 1.00, 0.80),
                   "CGENFF":        hsl_to_rgb(0.60, 1.00, 0.50),   "OPLSAAL":       hsl_to_rgb(0.80, 1.00, 0.50)}
class Molecular_Association_Dataset(Dataset):
    def __init__(self, infiles, verbose = True, **kwargs):
        infile          = infiles.keys()[0].split("/")[-2]
        self.ff         = kwargs.pop("ff",    infile.split("/")[-1].split(".")[0].split("_")[0])
        self.wm         = kwargs.pop("wm",    infile.split("/")[-1].split(".")[0].split("_")[1])
        self.label      = kwargs.pop("label", default_labels[self.ff])
        self.color      = kwargs.pop("color", default_colors[self.ff])
        Dataset.__init__(self, infiles = infiles, verbose = verbose, **kwargs)
#        self.cutoffs    = {}
#        for key in self.attrs:
#            if "bound_cutoff" in self.attrs[key] and "unbound_cutoff" in self.attrs[key]:
#                self.cutoffs[key]  = np.array([self.attrs[key]["bound_cutoff"], self.attrs[key]["unbound_cutoff"]])
