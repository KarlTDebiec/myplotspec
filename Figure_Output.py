#!/usr/bin/python
#   plot_toolkit.Figure_Output.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec on 14-04-25
####################################################### MODULES ########################################################
from __future__ import division, print_function
import os, sys, types
import numpy as np
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
###################################################### DECORATORS ######################################################
class Figure_Output:
    """
    Decorator class to allow plotting functions to save figures more easily

    **Arguments:**
        :*outfile*:  Output file name or <matplotlib.backends.backend_pdf.PdfPages>

    **Behavior:**
        | Calls decorated function, which should return a <matplotlib.Figure.Figure>
        | If *outfile* is a string ending in '.png', saves figure as a png file.
        | If *outfile* is a string ending in '.pdf', saves figure as a pdf file using PdfPages
        | If *outfile* is a PdfPages object, appends figure to that object as a page

    .. todo:
        - Test other outfile formats
        - Support html output with mpld3
        - Support show()
        - Figure out why figure cannot be returned from here
    """
    def __init__(self, function):
        self.function   = function
        self.__doc__    = function.__doc__
    def __call__(self, outfile = "test.pdf", *args, **kwargs):
        verbose = kwargs.get("verbose", "True")
        figure  = self.function(*args, **kwargs)
        if isinstance(outfile, matplotlib.backends.backend_pdf.PdfPages):
            figure.savefig(outfile, format = "pdf")
            if verbose: print("Figure saved to '{0}'.".format(os.path.abspath(outfile._file.fh.name)))
        else:
            if outfile.endswith("pdf"):
                outfile  = PdfPages(outfile)
                figure.savefig(outfile, format = "pdf", transparent = True)
                if verbose: print("Figure saved to '{0}'.".format(os.path.abspath(outfile._file.fh.name)))
                outfile.close()
            else:
                try:
                    figure.savefig(outfile)
                    if verbose: print("Figure saved to'{0}'.".format(outfile))
                except:
                    raise Exception("UNABLE TO OUTPUT TO FILE:" + outfile)


