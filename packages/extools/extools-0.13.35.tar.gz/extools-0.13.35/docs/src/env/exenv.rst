extools.env
-------------

A number of helpers are available here for the Extender Python environment. For
example: :py:meth:`extools.env.execution_context` can detect whether a script
is running through PS or VI, and whether you can show messages.

Aso included is the :py:class:`extools.env.StreamConductor`, which allows you
to temporarily redirect and capture the standard input and output streams used
globally.  Useful for getting code to run that expects these streams to be
connected.


.. automodule:: extools.env
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: extools.env.stream_conductor
    :members:
    :undoc-members:
    :show-inheritance:
