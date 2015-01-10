#!/usr/bin/python
# -*- coding: utf-8 -*-
#   MYPlotSpec.Debug.py
#   Written:    Karl Debiec     15-01-03
#   Updated:    Karl Debiec     15-01-10
"""
Decorator class to debug the passage of arguments to a wrapped function
or method
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def db_s(string = "", indent = 0):
    output = "DEBUG: {0}{1}".format("    " * indent, string)
    if len(output) >= 80:
        output = output[:77] + "..."
    print(output)
def db_kv(key, value, indent = 0, flag = "+"):
    output = "DEBUG: {0}  {1} {2}:{3}".format("    " * max(indent - 1, 0),
               flag, key, value)
    if len(output) >= 80:
        output = output[:77] + "..."
    print(output)
################################### CLASSES ###################################
class Debug_Arguments(object):
    """
    Decorator class to debug the passage of arguments to a wrapped
    function or method

    Note: This is a decorator class with arguments. These use a
      different syntax from decorator classes without arguments. When
      the wrapped function is declared, __init__ and __call__ from the
      decorator are called sequentially. __init__ receives the
      arguments, while __call__ receives the function. __init__ should
      store the values of the arguments, while __call__ should prepare
      and return a wrapped function using their values. Subsequent calls
      will go to the wrapped function. For decorator classes without
      arguments, __init__ is called when the function is declared, and
      should store the reference to the function; __call__ is called
      when the function is called, and should carry out the pre-function
      decorator logic, run the function, and carry out the post-function
      decorator logic.
    """

    def __init__(self, debug = False, **kwargs):
        """
        Stores decoration debug setting

        **Arguments:**
            :*debug*: Debug
        """
        self.debug = debug

    def __call__(self, function):
        """
        Wraps function or method

        **Arguments:**
            :*function*: function to wrap

        **Returns:**
            :*wrapped_function*: Wrapped function
        """
        from functools import wraps

        self.function = function

        @wraps(function)
        def wrapped_function(*args, **kwargs):
            """
            Wrapped version of function or method

            **Arguments:**
                :*\*args*:     Arguments passed to function at call
                               time
                :*\*\*kwargs*: Keyword arguments passed to function at
                               call time

            Note: The purpose of using *args_from call and **kwargs_from
              call is to allow this decorator to wrap class methods as
              well as functions. Standard usage of arguments in the
              declaration line of a decorator may make it very difficult
              to wrap both functions and methods with the same code. If
              a function is to be wrapped, the arguments pass from the
              call into the function as expected. However, if a method
              is to be wrapped, the first argument is the object hosting
              the method, shifting the positions of the other arguments.
              This may be avoided using the *args and **kwargs syntax.
              *args and **kwargs may be passed straight to the function
              or method, retaining the reference to the host object if
              present; while any keyword arguments needed by the
              decorator may be accessed from kwargs using pop or get.
            """
            debug = self.debug or kwargs.get("debug", False)

            if debug:
                print(
                  "DEBUG: Arguments passed to function/method '{0}':".format(
                  function.__name__))
                if len(args) > 0:
                    print("DEBUG:     Arguments:")
                    for arg in args:
                        print("DEBUG:         {0}".format(arg))
                if len(kwargs) > 0:
                    print("DEBUG:     Keyword arguments:")
                    for key in sorted(kwargs.keys()):
                        print("DEBUG:         {0}: {1}".format(key,
                          kwargs[key]))
            try:
                return function(*args, **kwargs)
            except TypeError as e:
                self.raise_verbosely(e, args, kwargs)

        return wrapped_function

    def raise_verbosely(self, e, args, kwargs):
        """
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
