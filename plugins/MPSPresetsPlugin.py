#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec.plugins.MPSPresetsPlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds preset argument groups to a nascent spec
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("myplotspec.plugins")
from ..yspec.plugins.PresetsPlugin import PresetsPlugin


################################### CLASSES ###################################
class MPSPresetsPlugin(PresetsPlugin):
    """
    Adds preset argument groups to a nascent spec

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      available_presets (dict): Available presets; outermost keys are
        the preset names, while the values are the arguments associated
        with each preset
    """
