# -*- coding: utf-8 -*-
#   myplotspec.debug.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Classes and functions for debugging.

.. todo:
  - should *indent* be specified in units of 1 space rather than 4
    spaces?
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def db_s(string, indent=0):
    """
    Prints debug output.

    Arguments:
      string (str): Content of debug output
      indent (int, optional): Indentation level; multiplied by 4
    """
    try:
        output = "DEBUG: {0}{1}".format("    " * indent,
                   str(string).replace("\n", "\\n"))
    except UnicodeEncodeError:
        output = "DEBUG: {0}{1}".format("    " * indent, string)
    if len(output) >= 80:
        output = output[:77] + "..."
    print(output)

def db_kv(key, value, indent=0, flag=" "):
    """
    Prints debug output for a key:value pair, truncated to 80 columns.

    Arguments:
      key (str): key
      value (str): value
      indent (int, optional): Indentation level; multiplied by 4
      flag (str, optional): Single-character flag describing pair
    """
    try:
        output = "DEBUG: {0}  {1} {2}:{3}".format("    " * max(indent - 1, 0),
                   flag, str(key).replace("\n", "\\n"),
                   str(value).replace("\n", "\\n"))
    except UnicodeEncodeError:
        output = "DEBUG: {0}  {1} {2}:{3}".format("    " * max(indent - 1, 0),
                   flag, key, value)
    if len(output) >= 80:
        output = output[:77] + "..."
    print(output)

def identify(subplots, **kwargs):
    """
    Identifies key of each subplot with inset text.

    Arguments:
      subplots (OrderedDict): subplots
    """
    from .text import set_inset

    for key, subplot in subplots.items():
        set_inset(subplot, text = key, xpos = 0.5, ypos = 0.5, ha = "center",
          va = "center", **kwargs)
################################### CLASSES ###################################
class debug_arguments(object):
    """
    Decorator to debug argument passage to a function or method.

    Provides more verbose output if a TypeError is encountered at
    function call

    Attributes:
      debug (int): Level of debug output
    """

    def __init__(self, debug=0):
        """
        Stores arguments provided at decoration.

        Arguments:
          debug (int): Level of debug output
        """
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

        decorator = self
        self.function = function

        @wraps(function)
        def wrapped_function(*args, **kwargs):
            """
            Wrapped version of function or method

            Arguments:
              args (tuple): Arguments passed to function
              kwargs (dict): Keyword arguments passed to function

            Returns:
              Return value of wrapped function
            """
            debug = self.debug or kwargs.get("debug", 0)

            if debug >= 1:
                db_s("Arguments passed to function/method '{0}':".format(
                  function.__name__))
                if len(args) > 0:
                    db_s("Arguments:", 1)
                    for arg in args:
                        db_s(arg, 2)
                if len(kwargs) > 0:
                    db_s("Keyword arguments:", 1)
                    for key in sorted(kwargs.keys()):
                        db_kv(key, kwargs[key], 2)
            try:
                return function(*args, **kwargs)
            except TypeError as e:
                self.raise_verbosely(e, args, kwargs)

        return wrapped_function

    def raise_verbosely(self, e, args, kwargs):
        """
        Arguments:
          e (TypeError): Error that cause wrapped function to fail
          args (tuple): Arguments passed to wrapped function
          kwargs (dict): Keyword arguments passed to wrapped function
        """
        from inspect import getargspec

        if not e.message.startswith(self.function.__name__):
            raise e

        print("TypeError: {0}".format(e))

        expected_args = getargspec(self.function).args

        if len(expected_args) > 0:
            print("    Expects arguments:")
            for expected_arg in expected_args:
                print("        {0}".format(expected_arg))
        if len(args) > 0:
            print("    Passed arguments:")
            for arg in args:
                print("        {0}".format(arg))
        if len(kwargs) > 0:
            print("    Passed keyword arguments:")
            for key in sorted(kwargs.keys()):
                print("        {0}".format(key))
