FigureManager
=============
.. automodule:: myplotspec.FigureManager
.. autoclass::  myplotspec.FigureManager.FigureManager
.. automethod:: myplotspec.FigureManager.FigureManager.draw_report
.. automethod:: myplotspec.FigureManager.FigureManager.draw_figure
.. automethod:: myplotspec.FigureManager.FigureManager.draw_subplot
.. automethod:: myplotspec.FigureManager.FigureManager.draw_dataset
.. automethod:: myplotspec.FigureManager.FigureManager.load_dataset
.. automethod:: myplotspec.FigureManager.FigureManager.initialize_presets
.. automethod:: myplotspec.FigureManager.FigureManager.main

Dataset
=======
.. automodule:: myplotspec.Dataset
.. autoclass::  myplotspec.Dataset.Dataset
.. automethod:: myplotspec.Dataset.Dataset.get_cache_key
.. automethod:: myplotspec.Dataset.Dataset.get_cache_message
.. automethod:: myplotspec.Dataset.Dataset.load_dataset

Decorators
==========

.. note::
    MyPlotSpec's decorator classes all support arguments provided at decoration
    (e.g. ``@decorator(foo = bar)``). These use a different syntax from
    decorator classes without arguments. When the wrapped function is declared,
    ``__init__`` and ``__call__`` from the decorator are called sequentially.
    ``__init__`` receives the arguments, while ``__call__`` receives the
    function. ``__init__`` should store the values of the arguments, while
    ``__call__`` should prepare and return a wrapped function using their
    values. Subsequent calls will go to the wrapped function. For decorator
    classes without arguments, ``__init__`` is called when the function is
    declared, and should store the reference to the function; ``__call__`` is
    called when the function is called, and should carry out the pre-function
    decorator logic, run the function, and carry out the post-function
    decorator logic.

.. note::
   MyPlotSpec's decorator classes :class:`~.manage_kwargs.manage_kwargs`,
   :class:`~.manage_output.manage_output`, and :class:`~.debug.debug_arguments`
   may be used to wrap either functions or methods. This is enabled by
   restricting the arguments of their ``wrapped_function`` to ``*args`` and
   ``**kwargs``, and accessing any arguments needed by the decorator using
   ``kwargs.pop()`` or ``kwargs.get().`` If a method is wrapped, the first
   argument is the host object of the method (``self``), shifting the positions
   of other named arguments.

manage_defaults_presets
-----------------------
.. automodule:: myplotspec.manage_defaults_presets
.. autoclass::  myplotspec.manage_defaults_presets.manage_defaults_presets

manage_kwargs
-------------
.. automodule:: myplotspec.manage_kwargs
.. autoclass::  myplotspec.manage_kwargs.manage_kwargs

manage_output
-------------
.. automodule:: myplotspec.manage_output
.. autoclass::  myplotspec.manage_output.manage_output

Functions
=========

General
-------
.. automodule::   myplotspec
.. autofunction:: myplotspec.load_dataset
.. autofunction:: myplotspec.get_yaml
.. autofunction:: myplotspec.merge_dicts
.. autofunction:: myplotspec.multi_get
.. autofunction:: myplotspec.multi_get_copy
.. autofunction:: myplotspec.multi_pop
.. autofunction:: myplotspec.pad_zero
.. autofunction:: myplotspec.get_color
.. autofunction:: myplotspec.get_colors
.. autofunction:: myplotspec.get_edges
.. autofunction:: myplotspec.get_figure_subplots
.. autofunction:: myplotspec.get_font

Axes
----
.. automodule::   myplotspec.axes
.. autofunction:: myplotspec.axes.set_xaxis
.. autofunction:: myplotspec.axes.set_yaxis
.. autofunction:: myplotspec.axes.set_colorbar
.. autofunction:: myplotspec.axes.add_partner_subplot

Text
----
.. automodule::   myplotspec.text
.. autofunction:: myplotspec.text.set_title
.. autofunction:: myplotspec.text.set_shared_xlabel
.. autofunction:: myplotspec.text.set_shared_ylabel
.. autofunction:: myplotspec.text.set_label
.. autofunction:: myplotspec.text.set_text

Legend
------
.. automodule::   myplotspec.legend
.. autofunction:: myplotspec.legend.set_legend
.. autofunction:: myplotspec.legend.set_shared_legend
