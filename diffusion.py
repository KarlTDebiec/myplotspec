#!/usr/bin/python
desc = """plot_Ka.py
    Plots amino acid analogue Ka of mean force
    Written by Karl Debiec on 12-10-17
    Last updated 13-11-03"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from   matplotlib.backends.backend_pdf import PdfPages
from   plot_toolkit import set_xaxis, set_yaxis, set_title
################################################# MATPLOTLIB FUNCTIONS #################################################
def plot_Ka_manuscript(data, keys, experiment = None, outfile = "Ka.pdf", **kwargs):
    title           = kwargs.get("title",           "")
    xlabel          = kwargs.get("xlabel",          "")
    xticklabels     = kwargs.get("xticklabels",     ["", "$P_{Bound}$", "$\\frac{k_{on}}{k_{off}}$", ""])
    if not xticklabels[0]  ==  "":  xticklabels = [""] + xticklabels
    if not xticklabels[-1] == "":   xticklabels = xticklabels + [""]
    xticks          = kwargs.get("xticks",          [0, 0.5, 1.5, 2.5, 3])
    print xticklabels
    print xticks
    ylabel          = kwargs.get("ylabel",          "$K_a (M^{-1})$")
    yticks          = kwargs.get("yticks",          range(0, 21, 2))
    y2label         = kwargs.get("y2label",         "$P_{Bound}$")
    y2ticks         = kwargs.get("y2ticks",         range(0, 21, 2))
    y2ticklabels    = kwargs.get("y2ticklabels",    np.linspace(0,1,11))
    figure  = plt.figure(figsize = [3.0, 3.0])
    axes    = figure.add_subplot(1, 1, 1, autoscale_on = False)
    axes2   = axes.twinx()
    figure.subplots_adjust(left = 0.12, right = 0.85, bottom = 0.12, top = 0.95)
    set_xaxis(axes,  label = xlabel,  ticks = xticks,  ticklabels = xticklabels,  label_fp = "8b", tick_fp = "8b")
    set_yaxis(axes,  label = ylabel,  ticks = yticks,  ticklabels = yticks,       label_fp = "8b", tick_fp = "6r")
    set_yaxis(axes2, label = y2label, ticks = y2ticks, ticklabels = y2ticklabels, label_fp = "8b", tick_fp = "6r")

    set_title(figure, s     = title)
    if experiment:
        axes.fill_between([0, 10.0], [experiment[0], experiment[0]], [experiment[1], experiment[1]], lw = 0,
          color = [0.5,0.5,0.5])
    for dataset in data:
        color   = dataset.color
        y       = np.array([dataset.attr[key + "/Pbound"]["Ka"]    for key in keys], np.float)
        yerr    = np.array([dataset.attr[key + "/Pbound"]["Ka se"] for key in keys], np.float)
        print dataset.infile, y, np.arange(0, y.size, 1) + 0.5
        axes.errorbar(np.arange(y.size) + 0.5, y, yerr = yerr * 1.96, mec=color, mfc=color, color=color,marker="o",
        elinewidth=2.0, capsize=10, mew=2, ms=5, ls = "None")
    if isinstance(outfile, PdfPages):
        figure.savefig(outfile, format = "pdf")
    else:
        output_pdf  = PdfPages(outfile)
        figure.savefig(output_pdf, format = "pdf")
        output_pdf.close()
        print "plot saved to " + outfile


