# -*- coding: utf-8 -*-
#   myplotspec.debug.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Classes and functions for debugging.

.. todo:
  - Probably will replace/move these
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
