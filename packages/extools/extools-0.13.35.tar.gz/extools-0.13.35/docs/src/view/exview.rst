extools.view
--------------

.. toctree::

    Errors<errors>
    composition
    optfields
    exsql<exsql>
    query
    utils


.. automodule:: extools.view
    :members: exview, exgen, EXVIEW_BLACKLIST
    :show-inheritance:

.. autoclass:: extools.view.ExView
    :members:
    :undoc-members:

    .. method:: lines(self)

        A generator that yields all lines in a detail view.
        
        Only available on detail views.

        :rtype: None
        :yields: ExView

        .. code-block:: python
            
            for line in oe500.lines():
                # line now contains the oe0500 view seeked to the next line

    .. method:: lines_from(start, end=None)

        A generator that yields all lines from ``start`` to ``end``.

        Only available on detail views.

        :param start: line to start at (numbering starts at 0)
        :type start: int
        :param end: line to end on (inclusive)
        :type end: int
        :yields: ExView
        :rtype: None


        .. code-block:: python
            
            for line in oe500.lines_from(2, 3):
                # line now contains the oe0500 view seeked to the second line
                # there will be one more iteration with the third line

    .. method:: lines_where(key=value, key=value, key=value, ...)

        A generator that yields all lines matched by browsing for the provided
        keys.  All key value pairs are combined using the ``AND`` condition and
        used to browse.

        Only available on detail views.

        :param key: a field name in the view.
        :type key: str
        :param value: the value to browse to
        :type value: any
        :yields: ExView
        :rtype: None


        .. code-block:: python
            
            for line in oe500.lines_where(ORDUNIQ=234234):
                # line now contains the oe0500 view seeked to first line or
                # the oder with unqiue key 234234.

    .. method:: create_optfield(field, value)
            
        Create a new optional field, set its value, and save it.

        :param field: Optional field name.
        :type field: str
        :param value: Optional field value.
        :type value: builtins.*
        :rtype: None
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()
                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                oe0500.create_optfield("MYFIELD", "NEWVAL")
            except ExViewError as e:
                # Do something on fail.

    .. method:: update_optfield(field, value)
            
        Update an existing optional field.

        :param field: Optional field name.
        :type field: str
        :param value: Optional field value.
        :type value: builtins.*
        :rtype: None
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()
                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                oe0500.update_optfield("MYFIELD", "UPDATEDVAL")

                # The composed OE0522 view is also accessible.
                oe0500.oe0522.update_optfield("MYFIELD", "UP2DATEVAL")

            except ExViewError as e:
                # Do something on fail.

    .. method:: delete_optfield(field)

        Delete an existing optional field.

        :param field: Optional field name.
        :type field: str
        :rtype: None
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()

                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                oe0500.delete_optfield("MYFIELD")

                # The composed OE0522 view is also accessible.
                oe0500.oe0522.delete_optfield("MYFIELD")

            except ExViewError as e:
                # Do something on fail.

    .. method:: get_optfield(field)

        Get the value of an existing optional field.

        :param field: Optional field name.
        :type field: str
        :returns: Optional field value.
        :rtype: builtins.*
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()

                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                value = oe0500.get_optfield("MYFIELD")

                # The composed OE0522 view is also accessible.
                value = oe0500.oe0522.get_optfield("MYFIELD")

            except ExViewError as e:
                # Do something on fail.

    .. method:: seek_to_optfield(field)

        Seek the view to an existing optional field.

        :param field: Optional field name.
        :type field: str
        :rtype: None
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()

                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                oe0500.seek_to_optfield("MYFIELD")

                # The composed OE0522 view is also accessible.
                # Now that is has seeked to MYFIELD extract the value with get.
                value = oe0500.oe0522.get("VALUE")

            except ExViewError as e:
                # Do something on fail.

    .. method:: update_or_create_optfield(field, value)

        Update an existing optional field if it exists, otherwise create it.

        :param field: Optional field name.
        :type field: str
        :param value: Optional field value.
        :type value: builtins.*
        :rtype: None
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()
                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                oe0500.update_or_create_optfield("MYFIELD", "UPDATEDVAL")

                # The composed OE0522 view is also accessible.
                oe0500.oe0522.update_or_create_optfield("MYFIELD", "UPDATEVAL")

            except ExViewError as e:
                # Do something on fail.

    .. method:: has_optfield(field)
        
        Check if an optional field exists.

        :param field: Optional field name.
        :type field: str
        :returns: True if an optional field with name ``field`` exists.
        :rtype: bool
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()
                # When the view is composed, the associated optional field view
                # OE0522 is auto-detected so you can call the ``*_optfield`` 
                # methods directly on oe0500.
                if oe0500.has_optfield("MYFIELD"):
                    showMessageBox("MYFIELD already defined.")

                # The composed OE0522 view is also accessible.
                oe0500.oe0522.has_optfield("MYFIELD", "UPDATEVAL")

            except ExViewError as e:
                # Do something on fail.

    .. data:: optfields
        
        Get all optional fields for a view.

        :returns: mapping of field names to values.
        :rtype: dict
        :raises: ExViewError

        .. code-block:: python
            
            try: 
                oe0500 = ExView("OE0500")
                oe0500.compose()

                # oe0500.optfields is now poplated with all the optional
                # fields currently defined for the header.
                # { "FIELDNAME": "VALUE", "F1": 1, "MYFIELD": "VALUE"}
                if "MYFIELD" in oe0500.optfields.keys():
                    showMessage("MYFIELD is set to {}".format(
                        oe0500.optfields["MYFIELD"]))
            except ExViewError as e:
                # Do something on fail.

