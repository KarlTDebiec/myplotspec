#!/usr/bin/python
desc = """pmf.py
    Plots potential of mean force
    Written by Karl Debiec on 12-10-22
    Last updated 13-11-03"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, re, sys
from   collections import OrderedDict
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
from plot_toolkit import get_font, set_xaxis, set_yaxis, set_title, set_inset, set_bigxlabel, set_bigylabel
################################################# MATPLOTLIB FUNCTIONS #################################################
def plot_pmf_multi(data, key, ytype, title = "", zero_min = None, bins = None, outfile = "pmf.pdf", **kwargs):
    insets  = {1: "SPC/E", 2: "TIP3P", 3: "TIPS3P", 4: "TIP4P/2005", 5: "TIP4P-Ew"}
    wms     = {re.sub("[/-]", "", v).upper():k for k, v in insets.iteritems()}
    handles = {1:[],2:[],3:[],4:[],5:[]}
    labels  = {1:[],2:[],3:[],4:[],5:[]}

    figure      = plt.figure(figsize = [6.5, 9])
    axes        = OrderedDict()
    for i in xrange(1, 6):
        axes[i] = figure.add_subplot(5, 1, i, autoscale_on = False)
    figure.subplots_adjust(left = 0.08, right = 0.98, bottom = 0.05, top = 0.95, hspace = 0.0)

    xticks              = kwargs.get("xticks",  np.arange( 2, 9))
    if   "comdist/"    in key: xlabel = kwargs.get("xlabel", "Center of Mass Distance ($\\AA$)")
    elif "mindist/"    in key: xlabel = kwargs.get("xlabel", "Heavy Atom Minimum Distance ($\\AA$)")
    elif "mindist_sb/" in key: xlabel = kwargs.get("xlabel", "Salt Bridge Minimum Distance ($\\AA$)")
    if   ytype.lower() in ["pmf", "potential of mean force"]:
        yticks          = kwargs.get("yticks",  np.arange(-3, 2))
        ylabel          = kwargs.get("ylabel",  "Potential of Mean Force $(\\frac{kcal}{mol})$")
        ykey            = "pmf"
        for i in axes:    axes[i].axhline(y = 0, linewidth = 0.5, color = "black")
    elif ytype.lower() in ["fe", "free energy"]:
        yticks          = kwargs.get("yticks",  np.arange(-1, 6))
        ylabel          = kwargs.get("ylabel",  "Free Energy $(k_B T)$")
        ykey            = "free energy"
    for i in axes:
        set_xaxis(axes[i], label = "", ticks = xticks, ticklabels = xticks if i == 5 else [])
        set_yaxis(axes[i], label = "", ticks = yticks, ticklabels = yticks if i == 1 else yticks[:-1])
        set_inset(axes[i], s = insets[i])
    set_title(figure,      s = title)
    set_bigxlabel(figure,  s = xlabel)
    set_bigylabel(figure,  s = ylabel)

    for dataset in data:
        i           = wms[dataset.wm]
        x           = np.mean(np.column_stack((dataset.data[key]["lower bound"],
                      dataset.data[key]["upper bound"])), axis=1)
        y           = dataset.data[key][ykey]
        if zero_min is not None:
            min_i   = (np.abs(x - float(zero_min.split(":")[0]))).argmin()
            max_i   = (np.abs(x - float(zero_min.split(":")[1]))).argmin()
            y      -= y[np.where(y == np.nanmin(y[min_i:max_i]))[0][0]]
        x           = x[x >= xticks[0]]
        y           = y[-1 * x.size:]
        x           = x[x <= xticks[-1]]
        y           = y[:x.size]
        handles[i] += axes[i].plot(x, y, lw = 2, color = dataset.color)
        labels[i]  += [dataset.label]
        if "cutoffs" in dir(dataset) and key in dataset.cutoffs:
            index   = np.array([(np.abs(x - dataset.cutoffs[key][0])).argmin(),
                      (np.abs(x - dataset.cutoffs[key][1])).argmin()])
            axes[i].plot(x[index], y[index], marker="|", ls="none", mfc=dataset.color, mec=dataset.color, ms=10, mew=2)
    handler = mpl.legend_handler.HandlerLine2D(numpoints = 1)
    for i in axes:
        axes[i].legend(handles[i], labels[i], prop = get_font("6r"), loc = 4, handler_map = {mpl.lines.Line2D: handler})

    if isinstance(outfile, mpl.backends.backend_pdf.PdfPages):
        figure.savefig(outfile, format = "pdf")
    else:
        output_pdf  = PdfPages(outfile)
        figure.savefig(output_pdf, format = "pdf")
        output_pdf.close()
        print "plot saved to " + outfile

def plot_pmf_single(data, key, outfile = "pmf.pdf", **kwargs):
    ytype      = kwargs.get("ytype",      "pmf")
    zero_min   = kwargs.get("zero_min",   None)
    downsample = kwargs.get("downsample", 1)

    # Prepare figure and subplots with specified dimensions
    figure  = plt.figure(figsize = [9, 6.5])
    axes    = figure.add_subplot(1, 1, 1, autoscale_on = False)
    figure.subplots_adjust(left = 0.07, right = 0.98, bottom = 0.08, top = 0.92)

    # Set labels and ticks
    xticks              = kwargs.get("xticks",   np.arange( 2, 17))
    if   "comdist/"    in key: xlabel = kwargs.get("xlabel", "Center of Mass Distance ($\\AA$)")
    elif "mindist/"    in key: xlabel = kwargs.get("xlabel", "Heavy Atom Minimum Distance ($\\AA$)")
    elif "mindist_sb/" in key: xlabel = kwargs.get("xlabel", "Salt Bridge Minimum Distance ($\\AA$)")
    if   ytype.lower() in ["pmf", "potential of mean force"]:
        yticks          = kwargs.get("yticks", np.linspace(-3, 1, 9))
        ylabel          = kwargs.get("ylabel", "Potential of Mean Force $(\\frac{kcal}{mol})$")
        ykey            = "pmf"
        axes.axhline(y  = 0, linewidth = 0.5, color = "black")
    elif ytype.lower() in ["fe", "free energy"]:
        yticks          = kwargs.get("yticks", np.linspace(-1, 5, 13))
        ylabel          = kwargs.get("ylabel", "Free Energy $(k_B T)$")
        ykey            = "free energy"
    title               = kwargs.get("title",  "")
    bins                = kwargs.get("bins",   None)    # For WESTPA
    set_xaxis(axes,   label = xlabel, ticks = xticks, ticklabels = xticks)
    set_yaxis(axes,   label = ylabel, ticks = yticks, ticklabels = yticks)
    set_title(figure, s     = title)

    # Plot pmfs
    handles = []
    labels  = []
    for dataset in data:
        x           = np.mean(np.column_stack((dataset.data[key]["lower bound"],
                      dataset.data[key]["upper bound"])), axis=1)
        y           = dataset.data[key][ykey]
        if zero_min is not None:
            min_i   = (np.abs(x - float(zero_min.split(":")[0]))).argmin()
            max_i   = (np.abs(x - float(zero_min.split(":")[1]))).argmin()
            y      -= y[np.where(y == np.nanmin(y[min_i:max_i]))[0][0]]
        x           = x[x >= xticks[0]]
        y           = y[-1 * x.size:]
        x           = x[x <= xticks[-1]]
        y           = y[:x.size]
        x           = np.mean(np.reshape(x, (x.size / downsample, downsample)), axis = 1)
        y           = np.mean(np.reshape(y, (y.size / downsample, downsample)), axis = 1)
        cip_index   = np.where(y == np.nanmin(y))[0][0]
        dsb_index   = cip_index + np.where(y[cip_index + 1:] - y[cip_index:-1] < 0)[0][0]
        ssip_index  = 0
        print dataset.ff, dataset.wm
        if hasattr(dataset, "cutoffs"):
            if not hasattr(dataset.cutoffs, "__iter__"): dataset.cutoffs = [dataset.cutoffs]
            print "    CUT is at {0:5.3f} A".format(dataset.cutoffs[0])
        print "    CIP is at {0:5.3f} A with depth of {1:5.3f}".format(x[cip_index], y[cip_index])
        print "    DSB is at {0:5.3f} A with depth of {1:5.3f}".format(x[dsb_index], y[dsb_index])
        axes.plot(x[cip_index], y[cip_index], marker="|", ls="none", mfc="black", mec="black", ms=10, mew=2)
        axes.plot(x[dsb_index], y[dsb_index], marker="|", ls="none", mfc="black", mec="black", ms=10, mew=2)
        handles    += axes.plot(x, y, lw = 2, color = dataset.color)
        labels     += [dataset.label]
#        if bins is not None:
#            bin_x   = []
#            bin_y   = []
#            for bin in bins:
#                index   = (np.abs(x - bin)).argmin()
#                bin_x  += [x[index]]
#                bin_y  += [y[index]]
#            axes.plot(bin_x, bin_y, marker="|", ls="none", mfc="black", mec="black", ms=10, mew=2)
        if hasattr(dataset, "cutoffs"):
            if not hasattr(dataset.cutoffs, "__iter__"): dataset.cutoffs = [dataset.cutoffs]
            for c in dataset.cutoffs: axes.axvline(x = c, linewidth = 0.5, color = "black")
    handler = mpl.legend_handler.HandlerLine2D(numpoints = 1)
    axes.legend(handles, labels, prop = get_font("8r"), loc = 4, handler_map = {mpl.lines.Line2D: handler})

    # Save file
    if isinstance(outfile, mpl.backends.backend_pdf.PdfPages):
        figure.savefig(outfile, format = "pdf")
    else:
        output_pdf  = PdfPages(outfile)
        figure.savefig(output_pdf, format = "pdf")
        output_pdf.close()
        print "plot saved to " + outfile
"""
d##ef plot_pmf_manuscript(data, key, ytype, title = "", zero_min = None, bins = None, outfile = "pmf.pdf", **kwargs):
    handles = []
    labels  = []

    figure  = plt.figure(figsize = [3.0, 3.0])
    axes    = figure.add_subplot(1, 1, 1, autoscale_on = False)
    figure.subplots_adjust(left = 0.17, right = 0.95, bottom = 0.12, top = 0.95)

    xticks              = kwargs.get("xticks", np.arange( 2, 9))
    if   "comdist/"    in key: xlabel = kwargs.get("xlabel", "Center of Mass Distance ($\\AA$)")
    elif "mindist/"    in key: xlabel = kwargs.get("xlabel", "Heavy Atom Minimum Distance ($\\AA$)")
    elif "mindist_sb/" in key: xlabel = kwargs.get("xlabel", "Salt Bridge Minimum Distance ($\\AA$)")
    if   ytype.lower() in ["pmf", "potential of mean force"]:
        yticks          = kwargs.get("yticks", np.linspace(-3, 0.5, 8))
        ylabel          = kwargs.get("ylabel", "Potential of Mean Force $(\\frac{kcal}{mol})$")
        ykey            = "pmf"
        axes.axhline(y  = 0, linewidth = 0.5, color = "black")
    elif ytype.lower() in ["fe", "free energy"]:
        yticks          = kwargs.get("yticks", np.linspace(-1, 5, 13))
        ylabel          = kwargs.get("ylabel", "Free Energy $(k_B T)$")
        ykey            = "free energy"
    set_xaxis(axes,   label = xlabel, ticks = xticks, ticklabels = xticks, label_fp = "8b", tick_fp = "6r")
    set_yaxis(axes,   label = ylabel, ticks = yticks, ticklabels = yticks, label_fp = "8b", tick_fp = "6r")
    set_title(figure, s     = title)

    for dataset in data:
        x           = np.mean(np.column_stack((dataset.data[key]["lower bound"],
                      dataset.data[key]["upper bound"])), axis=1)
        y           = dataset.data[key][ykey]
        if zero_min is not None:
            min_i   = (np.abs(x - float(zero_min.split(":")[0]))).argmin()
            max_i   = (np.abs(x - float(zero_min.split(":")[1]))).argmin()
            y      -= y[np.where(y == np.nanmin(y[min_i:max_i]))[0][0]]
        x           = x[x >= xticks[0]]
        y           = y[-1 * x.size:]
        x           = x[x <= xticks[-1]]
        y           = y[:x.size]
        handles    += axes.plot(x, y, lw = 1, color = dataset.color)
        labels     += [dataset.label]
        if bins is not None:
            bin_x   = []
            bin_y   = []
            for bin in bins:
                index   = (np.abs(x - bin)).argmin()
                bin_x  += [x[index]]
                bin_y  += [y[index]]
            axes.plot(bin_x, bin_y, marker="|", ls="none", mfc="black", mec="black", ms=10, mew=2)
#        if "cutoffs" in dir(dataset) and key in dataset.cutoffs:
#            for c in dataset.cutoffs[key]: axes.axvline(x = c, linewidth = 0.5, color = "black")
    handler = mpl.legend_handler.HandlerLine2D(numpoints = 1)
    axes.legend(handles, labels, prop = get_font("8r"), loc = 4, handler_map = {mpl.lines.Line2D: handler})

    if isinstance(outfile, PdfPages):
        figure.savefig(outfile, format = "pdf")
    else:
        output_pdf  = PdfPages(outfile)
        figure.savefig(output_pdf, format = "pdf")
        output_pdf.close()
        print "plot saved to " + outfile
"""

