#!/usr/bin/python
#   plot_toolkit.format.legend.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-04-09
####################################################### MODULES ########################################################
import os, sys
import numpy as np
from   ...plot_toolkit.auxiliary import gen_font
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_legend(subplot, handles = None, labels = None, fp = "8r", loc = 1, **kwargs):
    """
    Draws and formats a legend on *subplot*

    By default includes all series, or accepts manual lists of *handles* and *labels* for plotted series

    **Arguments:**
        :*subplot*: <matplotlib.axes.AxesSubplot> on which to act
        :*handles*: List of handles for plotted series (e.g. <matplotlib.lines.Line2D>)
        :*labels*:  List of labels for plotted series
        :*fp*:      Legend font in form of '##L'
        :*loc*:     Legend location
        :*kwargs*:  Keyword arguments to be passed to subplot.legend

    **Returns:**
        :*legend*:  matplotlib.legend.Legend

    .. todo::
        - Does *loc* need to be an argument to this function?
    """
    if handles is not None and labels is not None:
        return subplot.legend(handles, labels, loc = loc, prop = gen_font(fp), **kwargs)
    else:
        return subplot.legend(loc = loc, prop = gen_font(fp), **kwargs)


