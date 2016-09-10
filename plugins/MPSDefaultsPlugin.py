#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.MPSDefaultsPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds default arguments to a nascent spec.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
    import myplotspec.plugins
from ..yspec.plugins.DefaultsPlugin import DefaultsPlugin
################################### CLASSES ###################################
class MPSDefaultsPlugin(DefaultsPlugin):
    """
    Adds default arguments to a nascent spec.

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      defaults (dict): Default arguments
    """
