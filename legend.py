#!/usr/bin/python
# -*- coding: utf-8 -*-
#   plot_toolkit.legend.py
#   Written by Karl Debiec on 12-10-22, last updated by Karl Debiec 14-11-22
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
import numpy as np
from . import multi_kw, gen_font
################################## FUNCTIONS ###################################
def set_legend(subplot, handles = None, labels = None, legend_kw = {},
    **kwargs):
    """
    Draws and formats a legend on *subplot*

    By default includes all series; may alternatively accept manual
    lists of *handles* and *labels* for plotted series

    **Arguments:**
        :*subplot*: <Axes> on which to act
        :*handles*: List of handles for plotted series
        :*labels*:  List of labels for plotted series
        :*fp*:      Legend font; *fontproperties* and *prop* also
                    supported; passed to gen_font(...)

    **Returns:**
        :*legend*:  <Legend>
    """
    legend_kw["prop"] = gen_font(multi_kw(
      ["fp", "fontproperties", "legend_fp", "prop"], "8r", kwargs))
    if handles is not None and labels is not None:
        return subplot.legend(handles, labels, **legend_kw)
    else:
        return subplot.legend(**legend_kw)


