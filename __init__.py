#!/usr/bin/python
desc = """__init__.py
    Standard functions for plotting
    Written by Karl Debiec on 12-10-22
    Last updated 14-03-27"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys, warnings, types
import numpy as np
from   collections import OrderedDict
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.cm as cm
import matplotlib.colors as cl
from   matplotlib.backends.backend_pdf import PdfPages
################################################## GENERAL FUNCTIONS ###################################################
def abs_listdir(directory):
   for dirpath, _, filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
def hsl_to_rgb(h, s, l):
    c   = (1. - abs(2. * l - 1.)) * s
    hp  = h * 6
    i   = c * (1. - abs(hp % 2. - 1.))
    m   = l - 0.5 * c
    if   hp >= 0. and hp <  1.: return np.array([c,  i,  0.]) + m
    elif hp >= 1. and hp <  2.: return np.array([i,  c,  0.]) + m
    elif hp >= 2. and hp <  3.: return np.array([0., c,   i]) + m
    elif hp >= 3. and hp <  4.: return np.array([0., i,   c]) + m
    elif hp >= 4. and hp <  5.: return np.array([i,  0.,  c]) + m
    elif hp >= 5. and hp <= 6.: return np.array([c,  0.,  i]) + m
def pad_zero(ticks):
    n_zeros = 0
    for tick in ticks:
        if '.' in str(tick):    n_zeros = max(n_zeros, len(str(tick).split('.')[1]))
    if n_zeros  == 0:   return np.array(ticks, dtype = np.int)
    else:               return ["{0:.{1}f}".format(tick, n_zeros) for tick in ticks]
def gen_font(fp): return fm.FontProperties(family="Arial",size=int(fp[:-1]),weight={"r":"regular","b":"bold"}[fp[-1]])
def get_edges(figure, **kwargs):
    return {"x": np.array([[ax.get_position().xmin, ax.get_position().xmax] for ax in figure.axes]),
            "y": np.array([[ax.get_position().ymin, ax.get_position().ymax] for ax in figure.axes])}
def gen_contour_levels(I, cutoff = 0.9875, include_negative = False):
    I_flat      = np.sort(I.flatten())
    min_level   = I_flat[int(I_flat.size * cutoff)]
    max_level   = I_flat[-1]
    exp_int     = (max_level ** (1.0 / 9.0)) / (min_level ** (1.0 / 9.0))
    p_levels    = np.array([min_level * exp_int ** a for a in range(0, 10, 1)][:-1], dtype = np.int)
    if include_negative:
        I_flat      = I_flat[I_flat < 0]
        min_level   = -1 * I_flat[0]
        max_level   = -1 * I_flat[int(I_flat.size * (1 - cutoff))]
        exp_int     = (max_level ** (1.0 / 9.0)) / (min_level ** (1.0 / 9.0))
        m_levels    = -1 * np.array([min_level * exp_int ** a for a in range(0, 10, 1)][:-1], dtype = np.int)
        return        np.append(m_levels, p_levels)
    else:
        return p_levels
def gen_cmap(p_color):
    if isinstance(p_color, str):
        if   p_color == "blue":    r, g, b = [0.00, 0.00, 1.00]
        elif p_color == "red":     r, g, b = [1.00, 0.00, 0.00]
        elif p_color == "green":   r, g, b = [0.00, 0.50, 0.00]
        elif p_color == "cyan":    r, g, b = [0.00, 0.75, 0.75]
        elif p_color == "magenta": r, g, b = [0.75, 0.00, 0.75]
        elif p_color == "yellow":  r, g, b = [0.75, 0.75, 0.00]
        elif p_color == "black":   r, g, b = [0.00, 0.00, 0.00]
    else: r, g, b = p_color
    cdict   = {"red": ((0, r, r), (1, r, r)), "green": ((0, g, g), (1, g, g)), "blue": ((0, b, b), (1, b, b))}
    return    cl.LinearSegmentedColormap("cmap", cdict, 256)
def gen_figure_subplots(**kwargs):
    """ Generates figure and subplot according to selected format. Currently supports generation of 1 and 4 subplots in
        portraint or landscape orientation. """
    format = kwargs.get("format", "l1").lower()
    if   format == "l1":
        fig_w, fig_h    = kwargs.get("fig_w", 10.000), kwargs.get("fig_h",  7.500)  # Figure dimensions
        sub_w, sub_h    = kwargs.get("sub_w",  9.100), kwargs.get("sub_h",  6.500)  # Subplot dimensions
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)  # Outer margins
    elif format == "l4":
        fig_w, fig_h    = kwargs.get("fig_w", 10.000), kwargs.get("fig_h",  7.500)
        sub_w, sub_h    = kwargs.get("sub_w",  4.200), kwargs.get("sub_h",  3.000)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
        mar_w, mar_h    = kwargs.get("mar_w",  0.700), kwargs.get("mar_h",  0.500)  # Subplot margins
    elif format == "p1":
        fig_w, fig_h    = kwargs.get("fig_w",  7.500), kwargs.get("fig_h", 10.000)
        sub_w, sub_h    = kwargs.get("sub_w",  6.600), kwargs.get("sub_h",  4.700)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
    elif format == "p4":
        fig_w, fig_h    = kwargs.get("fig_w",  7.500), kwargs.get("fig_h", 10.000)
        sub_w, sub_h    = kwargs.get("sub_w",  2.950), kwargs.get("sub_h",  2.100)
        mar_t, mar_r    = kwargs.get("mar_t",  0.500), kwargs.get("mar_r",  0.200)
        mar_w, mar_h    = kwargs.get("mar_w",  0.700), kwargs.get("mar_h",  0.500)
    figure  = plt.figure(figsize = [fig_w, fig_h])
    subplots = OrderedDict()
    if   format.endswith("1"):
        subplots[1] = figure.add_subplot(1, 1, 1, autoscale_on = False)
        subplots[1].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,    # Left
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,    # Bottom
                                   sub_w                            / fig_w,    # Width
                                   sub_h                            / fig_h])   # Height
    elif format.endswith("4"):
        for i in [1,2,3,4]: subplots[i] = figure.add_subplot(2, 2, i, autoscale_on = False)
        subplots[1].set_position([(fig_w - mar_r - mar_w - 2*sub_w) / fig_w,
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[2].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,
                                  (fig_h - mar_t         - 1*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[3].set_position([(fig_w - mar_r - mar_w - 2*sub_w) / fig_w,
                                  (fig_h - mar_t - mar_h - 2*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
        subplots[4].set_position([(fig_w - mar_r         - 1*sub_w) / fig_w,
                                  (fig_h - mar_t - mar_h - 2*sub_h) / fig_h,
                                   sub_w                            / fig_w,
                                   sub_h                            / fig_h])
    return figure, subplots
########################################### MATPLOTLIB FORMATTING FUNCTIONS ############################################
def set_xaxis(ax, **kwargs): set_axis(ax.set_xlabel,ax.set_xbound,ax.axvline,ax.set_xticks,ax.set_xticklabels,**kwargs)
def set_yaxis(ax, **kwargs): set_axis(ax.set_ylabel,ax.set_ybound,ax.axhline,ax.set_yticks,ax.set_yticklabels,**kwargs)
def set_axis(set_label, set_bound, axline, set_ticks, set_ticklabels, label = "", ticks = range(11),
             ticklabels = range(11), label_fp = "11b", tick_fp = "8r", **kwargs):
    set_label(label, fontproperties = gen_font(label_fp),           **kwargs.get("label_kwargs",     {}))
    if ticks != []:
        set_bound(float(ticks[0]), float(ticks[-1]))
        if kwargs.get("outline", True):
            axline(ticks[0],  linewidth = 2, color = "black")
            axline(ticks[-1], linewidth = 2, color = "black")
    set_ticks(np.array(ticks, np.float32),                         **kwargs.get("tick_kwargs",      {}))
    set_ticklabels(ticklabels, fontproperties = gen_font(tick_fp), **kwargs.get("ticklabel_kwargs", {}))
def set_subtitle(axes, label, fp = "11b", **kwargs):
    axes.set_title(label = label, fontproperties = gen_font(fp), **kwargs)
def set_title(figure, edge_distance = 0.5, fp = "16b", **kwargs):
    edges       = get_edges(figure)
    kwargs["x"] = kwargs.get("x", (np.min(edges["x"]) + np.max(edges["x"])) / 2.0)
    kwargs["y"] = kwargs.get("y",  np.max(edges["y"]) + float(1.0 - np.max(edges["y"])) * edge_distance)
    set_text(figure, fp = fp, **kwargs)
def set_bigxlabel(figure, edge_distance = 0.3, fp = "11b", **kwargs):
    edges       = get_edges(figure)
    kwargs["x"] = (np.min(edges["x"]) + np.max(edges["x"])) / 2.0
    kwargs["y"] =  np.min(edges["y"]) * edge_distance
    set_text(figure, fp = fp, **kwargs)
def set_bigylabel(figure, side = "left", edge_distance = 0.3, fp = "11b", **kwargs):
    edges               = get_edges(figure)
    if side == "left":    kwargs["x"] = np.min(edges["x"]) * edge_distance
    else:                 kwargs["x"] = 1.0 - (1.0 - np.max(edges["x"])) * edge_distance
    kwargs["y"]         = (np.min(edges["y"]) + np.max(edges["y"])) / 2.0
    set_text(figure, fp = fp, rotation = "vertical", **kwargs)
def set_inset(axes, xpos = 0.5, ypos = 0.9, fp = "11b", **kwargs):
    position    = axes.get_position()
    kwargs["x"] = kwargs.get("x", position.xmin + xpos * position.width)
    kwargs["y"] = kwargs.get("y", position.ymin + ypos * position.height)
    set_text(axes.get_figure(), fp = fp, **kwargs)
def set_legend(subplot, handles = None, labels = None, fp = "8r", loc = 1, **kwargs):
    if handles is not None and labels is not None:
        return subplot.legend(handles, labels, loc = loc, prop = gen_font(fp), **kwargs)
    else:
        return subplot.legend(loc = loc, prop = gen_font(fp), **kwargs)
def set_text(figure_or_subplot, fp = "24b", ha = "center", va = "center", **kwargs):
    return figure_or_subplot.text(ha = ha, va = va, fontproperties = gen_font(fp), **kwargs)
def set_colorbar(cbar, ticks, ticklabels, label = "", label_fp = "12b", tick_fp = "8r", **kwargs):
    zticks  = np.array(ticks, np.float32)
    zticks  = (zticks - zticks[0]) / (zticks[-1] - zticks[0])
    cbar.ax.tick_params(bottom = "off", top = "off", left = "off", right = "off")
    cbar.set_ticks(ticks)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [],         outline = False)
        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticklabels, outline = False, tick_fp = tick_fp)
    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
    cbar.set_label(label, fontproperties = gen_font(label_fp))
###################################################### DECORATORS ######################################################
class Figure_Output(object):
    def __init__(self, plot_function):
        self.plot_function = plot_function
    def __call__(self, outfile = "test.pdf", *args, **kwargs):
        verbose = kwargs.get("verbose", "True")
        figure  = self.plot_function(*args, **kwargs)
        if isinstance(outfile, mpl.backends.backend_pdf.PdfPages):
            figure.savefig(outfile, format = "pdf")
            if verbose: print "Figure saved to'{0}'.".format(os.path.abspath(outfile._file.fh.name))
        elif isinstance(outfile, types.StringTypes):
            if outfile.endswith("pdf"):
                outfile  = PdfPages(outfile)
                figure.savefig(outfile, format = "pdf")
                if verbose: print "Figure saved to'{0}'.".format(os.path.abspath(outfile._file.fh.name))
                outfile.close()
            else:
                try:
                    figure.savefig(outfile)
                    if verbose: print "Figure saved to'{0}'.".format(outfile)
                except:
                    raise Exception("UNABLE TO OUTPUT TO FILE:" + outfile)
        else:
            raise Exception("TYPE OF OUTFILE NOT UNDERSTOOD:" + outfile)


