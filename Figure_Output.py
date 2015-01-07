#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Figure_Output.py
#   Written by Karl Debiec on 13-10-22, last updated by Karl Debiec on 15-01-06
"""
Decorator class to manage the output of matplotlib figures by a wrapped
function or method
"""
################################### MODULES ####################################
from __future__ import absolute_import,division,print_function,unicode_literals
import os, sys
import six
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
################################### CLASSES ####################################
class Figure_Output(object):
    """
    Decorator class to manage the output of matplotlib figures by a
    wrapped function or method

    Saves figure returned by wrapped function to a file named
    *outfile*; passing additional keyword arguments *savefig_kw* to
    savefig. For pdf output, additional argument *outfiles* may be
    provided; this contains a dictionary whose keys are the absolute
    paths to output pdf files, and whose values are references to open
    PdfPages objects representing those files. The purpose of this is
    to allow figures output from multiple calls to the wrapped function
    (or other analogously wrapped functions) to be output to sequential
    pages of the same pdf file. Typically *outfiles* will be
    initialized before calling this wrapped function; and once calls to
    the function is complete the close() method of each outfile in
    *outfiles* should be run.

    .. todo:
        - Support show()
    """
    def __init__(self, debug = False, verbose = False):
        """
        Stores decoration arguments

        **Arguments:**
            :*debug*:   Debug
            :*verbose*: Verbose
        """
        self.debug   = debug
        self.verbose = verbose

    def __call__(self, function):
        """
        Wraps function or method

        **Arguments:**
            :*function*: function to wrap

        **Returns:**
            :*wrapped_function*: Wrapped function
        """
        from functools import wraps

        @wraps(function)
        def wrapped_function(*args, **kwargs):
            """
            Wrapped version of function or method

            **Arguments:**
                :*outfile*:    Outfile name or <PdfPages>
                :*outfiles*:   Nascent dictionary of outfile names and
                               references to associated PdfPages
                :*savefig_kw*: Keyword arguments passed to savefig
                :*\*args*:     Arguments passed to function
                :*\*\*kwargs*: Keyword arguments passed to function
            """
            debug   = self.debug   or kwargs.get("debug",   False)
            verbose = self.verbose or kwargs.get("verbose", False)

            figure     = function(*args, **kwargs)
            outfile    = kwargs.pop("outfile",    "outfile.pdf")
            outfiles   = kwargs.pop("outfiles",   None)
            savefig_kw = kwargs.pop("savefig_kw", {"transparent": True})

            if isinstance(outfile, matplotlib.backends.backend_pdf.PdfPages):
                outfile_name = os.path.abspath(outfile._file.fh.name)
            elif isinstance(outfile, six.string_types):
                outfile_name = os.path.abspath(outfile)

            if outfile_name.endswith("pdf"):
                savefig_kw["format"] = "pdf"
                if outfiles is None
                    outfile_pdf = PdfPages(outfile_name)
                    figure.savefig(outfile_pdf, **savefig_kw)
                    outfile_pdf.close()
                elif outfile_name in outfiles:
                    outfile_pdf = outfiles[outfile_name]
                    figure.savefig(outfile_pdf, **savefig_kw)
                else:
                    outfile_pdf = outfiles[outfil_ename] = PdfPages(
                      outfile_name)
                    figure.savefig(outfile_pdf, **savefig_kw)
            else:
                figure.savefig(outfile, **savefig_kw)
                    
            if verbose:
                print("Figure saved to '{0}'.".format(
                  outfile_name)

            return figure

        return wrapped_function
