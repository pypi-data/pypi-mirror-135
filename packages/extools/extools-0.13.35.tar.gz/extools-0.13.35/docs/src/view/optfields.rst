====================
Optional fields
====================

Optional fields are one of the few things implemented consistently in the 
Sage 300 views. ``ExView`` instances take advantage of this, automatically
creating the following helpers to manage the optional fields associated with an
entry:

- :py:meth:`extools.view.ExView.create_optfield`
- :py:meth:`extools.view.ExView.update_optfield`
- :py:meth:`extools.view.ExView.get_optfield`
- :py:meth:`extools.view.ExView.delete_optfield`
- :py:meth:`extools.view.ExView.update_or_create_optfield`
- :py:meth:`extools.view.ExView.seek_to_optfield`
- :py:meth:`extools.view.ExView.has_optfield`
- :py:data:`extools.view.ExView.optfields`

When an ``ExView`` instance is created, it checks to see if it has any of 
the fields in the special constant 
:py:data:`extools.view.ExView.OPTFIELD_VIEW_HINTS`. If so, the helper
methods are automatically added to the class.

Optional fields are really custom properties of the object they are attached 
to, i.e. the Order Header optional fields are really properties of the Header
itself - they just weren't included in Sage. ``ExView`` applies this idea to
views that are :ref:`composed <Self-composing views>`, automatically adding the
helpers to both the optional field and the attached object.

For example, when you open an optional field view (like ``OE0522`` Order 
Optional Fields), the helpers are automatically added to the instance.

.. code-block:: python

    try:
        # Open the Order Optional Fields view
        # Because this is an optional field view, helpers are added on init.
        oe0522 = ExView("OE0522")     

        # If the optional field exists
        if oe0522.has_optfield("MYFIELD"):
            
            # Tell the user its value.
            showMessage("Myfield is set to: {}".format(
                oe0522.get_optfield("MYFIELD")))

    except ExViewError as e:
        showMessage("Failed get optional MYFIELD: {}".format(e))
        return 1

Because the Order Optional Fields are really properties of the 
``OE0520`` Order Header view, when you compose the header view
the helpers are added to it as well.  This provides a convenient,
idiomatic, shortcut to managing an object's optional fields:

.. code-block:: python

    try:
        # Open the Order Header view and compose it
        oe0520 = ExView("OE0520")     
        oe0520.compose()

        # If the optional field exists
        if oe0520.has_optfield("MYFIELD"):
            
            # Tell the user its value.
            showMessageBox("Myfield is set to: {}".format(
                oe0520.get_optfield("MYFIELD")))

    except ExViewError as e:
        showMessage("Failed get optional MYFIELD: {}".format(e))
        return 1

In the composed scenario, access from both the object and the composed
optional field view are available and equivalent.

.. code-block:: python

    try:
        # Open the Order Header view
        oe0520 = ExView("OE0520")     
        oe0520.compose()

        # This will always evaluate to True
        oe0520.has_optfield("MYFIELD") == oe0520.oe0522.has_optfield("MYFIELD")

        oe0520.create_optfield("F1", 1)

        if oe0520.oe0522.has_optfield("F1"):
            # True, we just created it through the header!
            ...
    except ExViewError as e:
        showMessage("Failed ...")
        return 1


