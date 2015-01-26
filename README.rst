Introduction
============

MYPlotSpec is a Python package used to design matplotlib-based figures using
the simple text format YAML.

MYPlotSpec may be used to rapidly write programs for plotting particular types
of data while retaining detailed control over plot configuration. The minimal
'quick & dirty' code needed to plot a certain type of data should be very close
to the polished code used to produce publication-quality figures featuring
precisely chosen proportions, ticks, colors, and fonts. MYPlotSpec accomplishes
this by offering a system for routing arguments provided in YAML format to
matplotlib's existing formatting functions. Settings may be applied globally or
routed to specific figures, subplots, and datasets. MYPlotSpec should have no
conflict with existing matplotlibrc settings, instead offering a level of
specific control on top of them. MyPlotSpec supports a system of defaults and
presets that make it easy to prepare multiple versions of plots without
changing code, such as for a lab notebook, printout, or presentation.

Dependencies
------------

MYPlotSpec supports Python 2.7 and 3.4, and requires the following packages:

- matplotlib
- numpy
- six
- yaml

MYPlotSpec has been tested with Anaconda python 2.1.0 on Arch Linux, OSX
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
