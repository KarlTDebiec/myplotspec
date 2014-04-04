#!/usr/bin/python
desc = """Molecular_Association_Dataset.py
    Class for organizing HDF5 data from molecular association trajectories for plotting
    Written by Karl Debiec on 13-10-22
    Last updated 13-12-17"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys
import numpy as np
from   plot_toolkit.Dataset import Dataset
from   plot_toolkit         import hsl_to_rgb
####################################################### CLASSES ########################################################
default_labels   = {"AMBER99SBILDN": "AMBER ff99SB-ILDN",           "AMBER99":       "AMBER ff99SB-ILDN",
                    "AMBER03":       "AMBER ff03",
                    "AMBERIPOLQ":    "AMBER ff13$\\alpha$",         "AMBER13ALPHA":  "AMBER ff13$\\alpha$",
                    "CHARMM27":      "CHARMM27",
                    "CHARMM22STAR":  "CHARMM22*",
                    "CHARMM36":      "CHARMM36",
                    "OPLSAAL":       "OPLS_2005",
                    "GAFF":          "GAFF",
                    "CGENFF":        "CGENFF"}
default_colors   = {"AMBER99SBILDN": hsl_to_rgb(0.60, 1.00, 0.25),  "AMBER99":       hsl_to_rgb(0.60, 1.00, 0.25),
                    "AMBER03":       hsl_to_rgb(0.60, 1.00, 0.60),
                    "AMBERIPOLQ":    hsl_to_rgb(0.60, 1.00, 0.80),  "AMBER13ALPHA":  hsl_to_rgb(0.60, 1.00, 0.80),
                    "CHARMM27":      hsl_to_rgb(0.00, 1.00, 0.25),
                    "CHARMM22STAR":  hsl_to_rgb(0.00, 1.00, 0.50),
                    "CHARMM36":      hsl_to_rgb(0.00, 1.00, 0.75),
                    "OPLSAAL":       hsl_to_rgb(0.30, 1.00, 0.25),
                    "GAFF":          hsl_to_rgb(0.00, 1.00, 0.00),
                    "CGENFF":        hsl_to_rgb(0.00, 1.00, 0.00)}
class Molecular_Association_Dataset(Dataset):
    def __init__(self, infiles, verbose = True, **kwargs):
        infile          = infiles.keys()[0].split("/")[-2]
        self.ff         = kwargs.pop("ff",    infile.split("/")[-1].split(".")[0].split("_")[0])
        self.wm         = kwargs.pop("wm",    infile.split("/")[-1].split(".")[0].split("_")[1])
        self.label      = kwargs.pop("label", default_labels.get(self.ff, self.ff + " " + self.wm))
        self.color      = kwargs.pop("color", default_colors.get(self.ff, [0,0,0]))
        if infiles.values()[0] != "": 
            Dataset.__init__(self, infiles = infiles, verbose = verbose, **kwargs)


