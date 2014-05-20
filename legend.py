#!/usr/bin/python
#   plot_toolkit.legend.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-05-15
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys
import numpy as np
from . import multi_kw, gen_font
################################################# MATPLOTLIB FUNCTIONS #################################################
def set_legend(subplot, handles = None, labels = None, **kwargs):
    """
    Draws and formats a legend on *subplot*

    By default includes all series; may alternatively accept manual lists of *handles* and *labels* for plotted series

    **Arguments:**
        :*subplot*: <Axes> on which to act
        :*handles*: List of handles for plotted series
        :*labels*:  List of labels for plotted series
        :*fp*:      Legend font; *fontproperties* and *prop* also supported; passed to gen_font(...)

    **Returns:**
        :*legend*:  <Legend>
    """
    kwargs["prop"] = gen_font(multi_kw(["fp", "fontproperties", "prop"], "8r", kwargs))
    if handles is not None and labels is not None:
        return subplot.legend(handles, labels, **kwargs)
    else:
        return subplot.legend(**kwargs)


