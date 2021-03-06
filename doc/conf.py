#!/usr/bin/python
# -*- coding: utf-8 -*-
#   myplotspec/doc/conf.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
################################### MODULES ###################################
import sphinx_rtd_theme
################################ CONFIGURATION ################################
todo_include_todos = False

needs_sphinx = "1.3"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo" ]
source_suffix = ".rst"
source_encoding = "utf-8"
napoleon_use_rtype = False
intersphinx_mapping = {
  "h5py":       ("http://docs.h5py.org/en/latest", None),
  "pandas":     ("http://pandas.pydata.org/pandas-docs/stable", None)}
master_doc = "index"
project   = "myplotspec"
copyright = "2015-2017, Karl T Debiec"
author    = "Karl T Debiec"
version   = "0.1"
release   = "16-06-29"

exclude_patterns  = ["_build"]
pygments_style    = "sphinx"
html_theme        = "sphinx_rtd_theme"
html_theme_path   = sphinx_rtd_theme.get_html_theme_path()
html_static_path  = ["_static"]
htmlhelp_basename = "myplotspecdoc"

autoclass_content     = "both"
autodoc_member_order  = "bysource"
autodoc_default_flags = ["members", "show-inheritance"]
