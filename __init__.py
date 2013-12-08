#!/usr/bin/python
desc = """__init__.py
    Standard functions for plotting
    Written by Karl Debiec on 12-10-22
    Last updated 13-10-22"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, sys, warnings
import numpy as np
import matplotlib.font_manager as fm
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
########################################### MATPLOTLIB FORMATTING FUNCTIONS ############################################
def get_font(fp): return fm.FontProperties(family="Arial",size=int(fp[:-1]),weight={"r":"regular","b":"bold"}[fp[-1]])
def get_edges(figure, **kwargs):
    return {"x": np.array([[ax.get_position().xmin, ax.get_position().xmax] for ax in figure.axes]),
            "y": np.array([[ax.get_position().ymin, ax.get_position().ymax] for ax in figure.axes])}
def set_xaxis(ax, **kwargs): set_axis(ax.set_xlabel,ax.set_xbound,ax.axvline,ax.set_xticks,ax.set_xticklabels,**kwargs)
def set_yaxis(ax, **kwargs): set_axis(ax.set_ylabel,ax.set_ybound,ax.axhline,ax.set_yticks,ax.set_yticklabels,**kwargs)
def set_axis(set_label, set_bound, axline, set_ticks, set_ticklabels, label = "", ticks = range(11),
             ticklabels = range(11), label_fp = "11b", tick_fp = "8r"):
    set_label(label, fontproperties = get_font(label_fp))
    if ticks != []:
        set_bound(float(ticks[0]), float(ticks[-1]))
        axline(ticks[0],  linewidth = 2, color = "black")
        axline(ticks[-1], linewidth = 2, color = "black")
    set_ticks(np.array(ticks, np.float32))
    set_ticklabels(ticklabels, fontproperties = get_font(tick_fp))
def set_title(figure, edge_distance = 0.5, fp = "16b", **kwargs):
    edges           = get_edges(figure)
    kwargs["x"]     = (np.min(edges["x"]) + np.max(edges["x"])) / 2.0
    kwargs["y"]     =  np.max(edges["y"]) + (1.0 - np.max(edges["y"])) * edge_distance
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
    position        = axes.get_position()
    kwargs["x"]     = kwargs.get("x", position.xmin + xpos * position.width)
    kwargs["y"]     = kwargs.get("y", position.ymin + ypos * position.height)
    set_text(axes.get_figure(), fp = fp, **kwargs)
def set_text(figure, fp = "24b", ha = "center", va = "center", **kwargs):
    figure.text(ha = ha, va = va, fontproperties = get_font(fp), **kwargs)
def set_colorbar(cbar, ticks, label = "", label_fp = "11b", **kwargs):
    zticks  = np.array(ticks, np.float)
    zticks  = (zticks - zticks[0]) / (zticks[-1] - zticks[0])
    cbar.ax.tick_params(bottom = "off", top = "off", left = "off", right = "off")
    cbar.set_ticks(ticks)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        set_xaxis(cbar.ax, ticks = [0,1],  ticklabels = [])
        set_yaxis(cbar.ax, ticks = zticks, ticklabels = ticks)
    for y in zticks: cbar.ax.axhline(y = y, linewidth = 1.0, color = "black")
    cbar.set_label(label, fontproperties = get_font(label_fp))


