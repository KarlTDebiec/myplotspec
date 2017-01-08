# -*- coding: utf-8 -*-
#   myplotspec.error.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Classes and functions for error handling.
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)


################################## FUNCTIONS ##################################
def is_argument_error(error):
    """
    Checks if an Exception has resulted from the passage of
    inappropriate arguments to a function or method.
    
    e.g.: 'get_cache_key() takes at least 2 arguments (3 given)'. This
    is the error I encounter most often in Python, but is raised as a
    generic TypeError rather than being assigned its own subclass of
    Exception, making it difficult to catch in a try/except.
    Additionally, the error message provides no information about which
    arguments missing, making debugging difficult. Alternatively, I may
    also have missed something and there may be a more intelligent way
    to handle this.

    .. todo:
      - There may be other error messages that may result from
        inappropriate passage or arguments
    """
    import re
    import six

    if isinstance(error, Exception):
        error = error.args[0]
    if six.PY2:
        test = re.compile("^\S+\(\) takes at least \d arguments")
    else:
        test = re.compile("^\S+\(\) missing \d+ required positional argument")
    if re.match(test, error):
        return True
    else:
        return False


################################### CLASSES ###################################
class MPSError(Exception):
    """
    Base error class for MYPlotSpec
    """

    def __init__(self, error):
        """
        Initializes from an existing error and stores traceback
        """
        from sys import exc_info

        self.traceback = exc_info()
        super(MPSError, self).__init__(error)


class MPSArgumentError(MPSError):
    """
    Error raised when a function is passed incorrect arguments

    Implements Python 3-style useful error messages listing missing
    arguments in Python 2.
    """

    def __init__(self, error, function, kwargs=None, class_=None, skip=None):
        """
        Initializes from an existing error and writes message
        """
        import six

        super(MPSArgumentError, self).__init__(error)

        if six.PY2:
            from inspect import getargspec

            argspec = getargspec(function)
            args = [a for a in argspec.args]
            if skip is not None:
                if isinstance(skip, six.string_types):
                    skip = [skip]
                for s in skip:
                    if s in args:
                        args.remove(s)
            args = args[:-1 * len(argspec.defaults)]
            given = [a for a in args if a in kwargs]
            missing = [a for a in args if a not in kwargs]
            message = "{0}() missing ".format(function.__name__)
            if class_ is not None:
                message = "{0}.{1}".format(class_.__name__, message)

            message += "{0} ".format(len(missing))
            if len(missing) > 1:
                message += "required positional arguments: "
            else:
                message += "required positional argument: "
            message += str(missing).lstrip("[").rstrip("]")

        else:
            message = self.args[0]
            if class_ is not None:
                message = "{0}.{1}".format(class_.__name__, message)
        self.args = (message,)


class MPSDatasetError(MPSError):
    """
    Error raised when initializing dataset
    """
    pass


class MPSDatasetCacheError(MPSError):
    """
    Error raised when checking the presence of a dataset in dataset
    cache
    """
    pass
