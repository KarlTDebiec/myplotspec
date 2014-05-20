#!/usr/bin/python
# -*- coding: utf-8 -*-
#   plot_toolkit.examples.py
#   Written by Karl Debiec on 14-04-25, last updated by Karl Debiec on 14-05-20
"""
Examples to demonstrate usage of each component of plot_toolkit
"""
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys, types
import numpy as np
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from plot_toolkit.Figure_Output import Figure_Output
from plot_toolkit import gen_figure_subplots, identify
from plot_toolkit.axes import set_xaxis, set_yaxis
from plot_toolkit.text import set_inset, set_text, set_title
###################################################### FUNCTIONS #######################################################
@Figure_Output
def page_1(**kwargs):
    figure, subplots = gen_figure_subplots(nrows = 2, ncols = 2, nsubplots = 3, fig_width = 7.5, fig_height = 11.0,
                                           sub_width  = 2.0, left   = 1.5, wspace = 1.0,
                                           sub_height = 2.0, bottom = 4.5, hspace = 1.0)
    gen_figure_subplots(figure = figure, subplots = subplots, nrows = 1, ncols = 1,
                                           sub_width  = 0.1, left   = 3.5,
                                           sub_height = 2.0, bottom = 4.5)
    gen_figure_subplots(figure = figure, subplots = subplots, nrows = 2, ncols = 5,
                                           sub_width  = 1.0, left   = 1.5, wspace = 0.0,
                                           sub_height = 1.0, bottom = 1.5, hspace = 0.0)
    set_title(figure, "Plot Toolkit Sample Plots")

    # Subplot 1: Text Annotation
    set_title(subplots[1], "Text Annotation")
    set_xaxis(subplots[1], ticks = range(-5, 6, 1), label = "X")
    set_yaxis(subplots[1], ticks = range(-5, 6, 1), label = "Y", label_kw = dict(rotation = "horizontal"))
    subplots[1].plot([-10, 10], [  0,  0], color = "black")
    subplots[1].plot([  0,  0], [-10, 10], color = "black")
    subplots[1].plot(np.random.randn(100), np.random.randn(100), ls = "none", marker = "o", color = "blue")
    set_inset(subplots[1], "Quadrant I",   fp = "10r", xpos = 0.95, ypos = 0.95, ha = "right", va = "top") 
    set_inset(subplots[1], "Quadrant II",  fp = "10r", xpos = 0.05, ypos = 0.95, ha = "left",  va = "top")
    set_inset(subplots[1], "Quadrant III", fp = "10r", xpos = 0.05, ypos = 0.05, ha = "left",  va = "bottom")
    set_inset(subplots[1], "Quadrant IV",  fp = "10r", xpos = 0.95, ypos = 0.05, ha = "right", va = "bottom")
    
    # Subplot 2: Tick and Font Settings
    set_title(subplots[2], "Tick and Font Settings")
    set_xaxis(subplots[2], ticks = range(11), label = "Arabic Numeral",
        tick_params = dict(direction = "out", length = 5, width = 1, top = 0))
    if os.path.isfile("/Library/Fonts/Hei.ttf"):
        set_yaxis(subplots[2], ticks = range(11), 
          ticklabels  = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十"],
          tick_fp     = dict(fname    = "/Library/Fonts/Hei.ttf", size =  8),
          tick_params = dict(direction = "out", length = 5, width = 1, right = 0),
          label       = u"数\n字",
          label_fp    = dict(fname    = "/Library/Fonts/Hei.ttf", size = 10, weight = "bold"),
          label_kw    = dict(rotation = "horizontal", labelpad = 10))
    else:
        set_yaxis(subplots[2], ticks = range(11),
          ticklabels  = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?"],
          tick_params = dict(direction = "out", length = 5, width = 1, right = 0),
          label       = "Hei Chinese Font Unavailable")
    subplots[2].plot([0, 10], [0, 10], color = "blue", lw = 1)

    # Subplot 3: Colorbar
    set_title(subplots[3], "Colorbar")
    set_xaxis(subplots[3], ticks = range(11), label  = "X")
    set_yaxis(subplots[3], ticks = range(11), labbel = "Y")

    identify(subplots)
    return figure

######################################################### MAIN #########################################################
if __name__ == "__main__":
    outfile = PdfPages("examples.pdf")
    page_1(outfile)
    outfile.close()


