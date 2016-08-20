Introduction
============

MYPlotSpec is a Python package used to write matplotlib-based plotting tools
that support powerful configuration options using the simple text format YAML.

The goal of MYPlotSpec is to make it possible to modify plot settings such as
proportions, ticks, colors, or fonts with per-figure, per-subplot, and
per-dataset specificity without needing to modify Python code or implement
support for individual settings. MYPlotSpec accomplishes this by parsing
arguments provided in YAML format and routing them to matplotlib's existing
formatting functions. MYPlotSpec should have no conflict with existing
matplotlibrc settings, instead offering a level of specific control on top of
them. MyPlotSpec supports a system of defaults and presets that make it easy to
prepare multiple versions of plots without modifying code, such as for a lab
notebook, printout, or presentation.

Sample applications of MYPlotSpec for plotting several types of data are
available on GitHub:

- `Molecular Dynamics Simulation Analysis
  <https://github.com/KarlTDebiec/MolDynPlot>`_
- `Ramachandran Plots
  <https://github.com/KarlTDebiec/Ramaplot>`_
- `Nuclear Magnetic Resonance Spectroscopy
  <https://github.com/KarlTDebiec/myplotspec_nmr>`_
- `Dynamic Light Scattering
  <https://github.com/KarlTDebiec/myplotspec_dls>`_
- `Fast Protein Liquid Chromatography
  <https://github.com/KarlTDebiec/myplotspec_fplc>`_

Dependencies
------------

MYPlotSpec supports Python 2.7 and 3.4, and requires the following packages:

- matplotlib
- numpy
- six
- yaml

MYPlotSpec has been tested with Anaconda python 2.2.0 on Arch Linux, OSX
Yosemite, and Windows 8.1.

Installation
------------

Put in your ``$PYTHONPATH``::

    export PYTHONPATH=/path/to/my/python/modules:$PYTHONPATH

where ``/path/to/my/python/modules`` contains ``myplotspec``.

Authorship
----------

MYPlotSpec is developed by Karl T. Debiec, a graduate student at the University
of Pittsburgh advised by Professors Lillian T. Chong and Angela M. Gronenborn.

License
-------

Released under a 3-clause BSD license.
