#!/usr/bin/python
#   plot_toolkit.Figure_Output.py
#   Written by Karl Debiec on 12-10-22
#   Last updated by Karl Debiec 14-04-04
####################################################### MODULES ########################################################
import os, sys, types
import numpy as np
from   matplotlib.backends.backend_pdf import PdfPages
###################################################### DECORATORS ######################################################
class Figure_Output(object):
    """
    Decorator class to help functions that generate plots save figures more easily

    **Arguments:**
        :*outfile*:  Output file name or <matplotlib.backends.backend_pdf.PdfPages> object

    **Behavior:**
        | Calls decorated function, which should return a matplotlib.Figure.Figure object.
        | If *outfile* is a string ending in '.png', saves figure as a png file.
        | If *outfile* is a string ending in '.pdf', saves figure as a pdf file using PdfPages
        | If *outfile* is a PdfPages object, appends figure to that object as a page
    """
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


