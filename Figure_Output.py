#!/usr/bin/python
#   plot_toolkit.Figure_Output.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec on 14-11-18
"""
"""
################################## MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys, types
import numpy as np
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
################################### CLASSES ####################################
class Figure_Output(object):
    """
    Decorator class to allow plotting functions to save figures more
    easily

    **Arguments:**
        :*outfile*: Output file name or
                    <matplotlib.backends.backend_pdf.PdfPages>

    **Behavior:**
        | Calls decorated function, which should return a
        |   <matplotlib.Figure.Figure>
        | If *outfile* is a string ending in '.pdf', saves figure as a
        |   pdf file using PdfPages
        | If *outfile* is a PdfPages object, appends figure to that
        |   object as a page

    .. todo:
        - Test other outfile formats
        - Support html output with mpld3
        - Support show()
    """
    def __init__(self, function):
        from functools import update_wrapper

        self.function = function
        update_wrapper(self, function)

    def __call__(self, *args, **kwargs):
        verbose = kwargs.get("verbose", "True")

        outfile = kwargs.pop("outfile", "test.pdf")
        figure  = self.function(*args, **kwargs)

        if isinstance(outfile, matplotlib.backends.backend_pdf.PdfPages):
            figure.savefig(outfile, format = "pdf")
            if verbose:
                print("Figure saved to '{0}'.".format(
                  os.path.abspath(outfile._file.fh.name)))
        else:
            if outfile.endswith("pdf"):
                outfile  = PdfPages(outfile)
                figure.savefig(outfile, format = "pdf", transparent = True)
                if verbose:
                    print("Figure saved to '{0}'.".format(
                      os.path.abspath(outfile._file.fh.name)))
                outfile.close()
            else:
                try:
                    figure.savefig(outfile)
                    if verbose:
                        print("Figure saved to'{0}'.".format(outfile))
                except:
                    raise Exception("UNABLE TO OUTPUT TO FILE:" + outfile)
        return figure
