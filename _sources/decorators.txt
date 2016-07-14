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
.. autoclass::  myplotspec.manage_defaults_presets.manage_defaults_presets

manage_kwargs
-------------
.. autoclass::  myplotspec.manage_kwargs.manage_kwargs

manage_output
-------------
.. autoclass::  myplotspec.manage_output.manage_output
