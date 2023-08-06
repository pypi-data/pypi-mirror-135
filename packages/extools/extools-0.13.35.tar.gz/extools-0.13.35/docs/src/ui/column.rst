Grid Column UIs
-----------------

Some pre-built classes are included for quickly customizing a grid on
screen.

The :py:class:`extools.ui.callback_column.CallbackColumnUI` adds a column to
the grid that is populated with a callback. It looks after the screen and
column setup, and calls the callback to popluate the cell whenever a value is
requested.  The callback receives the grid edit event and data source as
arguments.

The :py:class:`extools.ui.optfield_column.OptfieldColumnUI` adds a column to
the grid that is populated with an optional field.  The UI supports both
editable and non-editable cells and automatically writes back values to the
optional field data source.

The :py:class:`extools.ui.optfield_column.OptfieldMultiColumnUI` adds columns
to the grid that are populated optional fields.  The UI supports both editable
and non-editable cells and automatically writes back values to the optional
field data source.

The :py:class:`extools.ui.datasource_column.DatasourceColumnUI` adds a column
that is populated with a datasource field - any datasource, it need not be the
one that backs the grid.

.. autoclass:: extools.ui.callback_column.CallbackColumnUI
    :members:

.. autoclass:: extools.ui.optfield_column.OptfieldColumnUI
    :members:

.. autoclass:: extools.ui.optfield_multicolumn.OptfieldMultiColumnUI
    :members:

.. autoclass:: extools.ui.datasource_column.DatasourceColumnUI
    :members:
