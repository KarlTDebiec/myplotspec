# -*- coding: utf-8 -*-
#   myplotspec.manage_output.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Decorator to manage the output of matplotlib figures.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class manage_output(object):
    """
    Decorator to manage the output of matplotlib figures.

    Saves figure returned by wrapped function to a file named
    ``outfile``; passing additional keyword arguments ``savefig_kw`` to
    ``Figure.savefig()``. For pdf output, additional argument
    ``outfiles`` may be provided; containing a dictionary whose keys are
    the paths to output pdf files, and whose values are open PdfPages
    objects representing those files. The purpose of this is to allow
    figures output from multiple calls to the wrapped function to be
    output to sequential pages of the same pdf file. Typically
    ``outfiles`` will be initialized before calling this wrapped
    function; and once calls to the function is complete the
    ``PdfPages.close()`` method of each outfile in ``outfiles`` is
    called.

    .. todo:
        - Support show()
    """

    def __init__(self, verbose=False, debug=False):
        """
        Stores arguments provided at decoration.

        Arguments:
          verbose (bool): Enable verbose output
          debug (bool): Enable debug output
        """
        self.verbose = verbose
        self.debug = debug

    def __call__(self, function):
        """
        Wraps function or method.

        Arguments:
          function (function): Function or method to wrap

        Returns:
          (function): Wrapped function or method
        """
        from functools import wraps

        self.function = function

        @wraps(function)
        def wrapped_function(*args, **kwargs):
            """
            Wrapped version of function or method

            Arguments:
              outfile (str, PdfPages): outfile path or PDFpages
                object
              outfiles (dict): Nascent dict of [outfile path]: PdfPages 
              savefig_kw (dict): Keyword arguments passed to savefig()
              args (tuple): Arguments passed to function
              kwargs (dict): Keyword arguments passed to function

            Returns:
              Return value of wrapped function
            """
            from os.path import abspath
            import six
            import matplotlib
            from matplotlib.backends.backend_pdf import PdfPages

            debug = self.debug or kwargs.get("debug", False)
            verbose = self.verbose or kwargs.get("verbose", False)

            figure = function(*args, **kwargs)
            outfile = kwargs.pop("outfile", "outfile.pdf")
            outfiles = kwargs.pop("outfiles", None)
            savefig_kw = kwargs.pop("savefig_kw", {})

            if isinstance(outfile, matplotlib.backends.backend_pdf.PdfPages):
                outfile_name = abspath(outfile._file.fh.name)
            elif isinstance(outfile, six.string_types):
                outfile_name = abspath(outfile)

            if outfile_name.endswith("pdf"):
                savefig_kw["format"] = "pdf"
                if outfiles is None:
                    outfile_pdf = PdfPages(outfile_name)
                    figure.savefig(outfile_pdf, **savefig_kw)
                    outfile_pdf.close()
                elif outfile_name in outfiles:
                    outfile_pdf = outfiles[outfile_name]
                    figure.savefig(outfile_pdf, **savefig_kw)
                else:
                    outfile_pdf = outfiles[outfile_name] = PdfPages(
                      outfile_name)
                    figure.savefig(outfile_pdf, **savefig_kw)
            else:
                figure.savefig(outfile, **savefig_kw)

            if verbose:
                print("Figure saved to '{0}'.".format(outfile_name))

            return figure

        return wrapped_function
