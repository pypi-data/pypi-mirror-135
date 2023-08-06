====================
Self-composing views
====================

Sage 300 uses the concept of *views* to provide a simplified interface for
accessing data.  The view layer sits between the user interfaces, like screens
and imports, and the database. The views are where Sage implements and enforces
business logic.

Extender provides access to views in Python through the ``View`` object.
A view is usually backed by exactly one database table and provides access
to a single record at a time.  Sage allows views that share a unique identifier
to be *composed* with one another.  

When two views are composed, when the unique key field changes in one view,
it is changed in all other composed views as well. 
This makes accessing related data much easier: no need to seek twice.

Consider the case where a script must set the optional field ``MYFIELD`` on a
detail line to ``HASX`` if any of the lot numbers in an OE Order start with ``X``.
Working with Extender ``View`` objects and without composition:

.. code-block:: python
    
    # Open the order header and seek to the order
    oe0520 = openView("OE0520")

    if not oe0520:                          # If the open failed, return.
        return 1

    rc = oe0520.recordClear()
    if rc != 0:                             # If the record clear failed.
        return rc

    o  = oe0520.order(1)
    if o != 0:                              # If setting view order fails.
        return o 

    pu = oe0520.put("ORDNUMBER", "ORD453")  
    if pu != 0:                             # If setting the key field fails.
        return pu

    r  = oe0520.read()
    if r != 0:                              # If reading the record fails.
        return r

    # Get the order unique ID to lookup the detail lines.
    orduniq = oe0520.get("ORDUNIQ")

    # Open the order details and seek to the beginning
    oe0500 = openView("OE0500")
    if not oe0500:
        return 1

    rc = oe0500.recordClear()
    if rc != 0:
        return rc

    br = oe0500.browse("", 1)
    if br != 0:
        return br

    # In preparation for reading lots and optional fields, open the views.
    oe0507 = openView("OE0507")             # Order detail lots
    oe0501 = openView("OE0501")             # Order detail optional fields
    if not (oe0507 and oe0501):
        return 1

    # For each detail line in the order
    while(oe0500.fetch() == 0):
        # Seek the lot view to the lots for this line.
        linenum = oe0500.get("LINENUM")

        rc = oe0507.recordClear()
        if rc != 0:
            return rc

        br = oe0507.browse(
                'ORDUNIQ = "{}" AND LINENUM = "{}"'.format(orduniq, linenum))
        if br != 0:
            return br

        # Look at each lot associated with the line
        while(oe0507.fetch() == 0):

            # Get the lot number
            lotnumf = oe0507.get("LOTNUMF")

            # Check the condition
            if lotnumf and lotnumf.startswith("X"):

                # Try to read the optional field
                rc = oe0501.recordClear()
                if rc != 0:
                    return rc

                # The index requires order, line, and optional field keys.
                po = oe0501.put("ORDUNIQ", orduniq)
                pl = oe0501.put("LINENUM", linenum)
                pf = oe0501.put("OPTFIELD", "MYFIELD")
                if po != 0 or pl != 0 or pf != 0:
                    continue

                r = oe0501.read()
                if r != 0:
                    # The field doesn't exist yet, create it.
                    rg = oe0501.recordGenerate()
                    if rg != 0:
                        return rg

                    po = oe0501.put("ORDUNIQ", orduniq)
                    pl = oe0501.put("LINENUM", linenum)
                    pf = oe0501.put("OPTFIELD", "MYFIELD")
                    pv = oe0501.put("VALUE", "HASX")
                    if po != 0 or pl != 0 or pf != 0 or pv != 0:
                        return 1

                    ins = oe0501.insert()
                    if ins != 0:
                        return ins
                else:
                    # The field does exist, check it is correct.
                    if oe0501.get("VALUE") != "HASX":

                        # It isn't set correctly, update it.
                        pv = oe0501.put("VALUE", "HASX")
                        if pv != 0:
                            return pv

                        up = oe0501.update()
                        if up != 0:
                            return up

It is a bit of a mouthful.  Most of the code is opening, setting up, and 
seeking views.  At every step, we need to search for the ``orduniq`` and/or
``linenum``. This is where composition helps: it eliminates the a lot
of the repetitive work by automatically filling in the unique keys for composed
views.

Views can be composed at runtime.  We can compose the views we are 
working with as they all share the ``ORDUNIQ`` key.

Let's try again but this time manually compose the views we need.

.. code-block:: python
    
    # Open the views
    oe0520 = View("OE0520")     # Order Header
    oe0500 = View("OE0500")     # Order Details
    oe0507 = View("OE0507")     # Order Detail Lot Numbers
    oe0501 = View("OE0501")     # Order Detail Optional Field
    if not (oe0520 and oe0500 and oe0507 and oe0501):
        return 1

    # Compose them all together. 
    c20 = oe0520.compose(oe0500, None, None, None, None, None)

    # The arguments to compose can be a bit like a shell game...
    c00 = oe0500.compose(oe0520, oe0501, None, None, None, oe0507)
    c07 = oe0507.compose(oe0500)
    c01 = oe0501.compose(oe0500)

    # Make sure the composing was successful for all views
    if c20 != 0 or c00 != 0 or c07 != 0 or c01 != 0:
        return 1

    rc = oe0520.recordClear()
    if rc != 0:                             # If the record clear failed.
        return rc
        
    o  = oe0520.order(1)
    if o != 0:                              # If setting view order fails.
        return o 

    pu = oe0520.put("ORDNUMBER", "ORD453")  
    if pu != 0:                             # If setting the key field fails.
        return pu

    r  = oe0520.read()
    if r != 0:                              # If reading the record fails.
        return r

    # Now a magical thing has happened, the detail view is ready to 
    # read the lines for this order.
    rc = oe0500.recordClear()
    if rc != 0:
        return rc

    # For each detail line in the order
    while(oe0500.fetch() == 0):
        # The fetch causes the optional field and lot views to filter out
        # all but records for the current line.

        rc = oe0507.recordClear()
        if rc != 0:
            return rc

        # Look at each lot associated with the line
        while(oe0507.fetch() == 0):
            # Get the lot number
            lotnumf = oe0507.get("LOTNUMF")

            # Check the condition
            if lotnumf and lotnumf.startswith("X"):

                # Because the ORDUNIQ and LINENUM are set implicitly through
                # composition, use the setOptionalField helper from the 
                # Extender View class
                so = oe0501.setOptionalField("MYFIELD", "HASX")
                if not so:
                    return so

That is much better.  However, you need to know how to compose these things.
There are thousands of views in Sage and not all views can be composed with all
others. Composition is also uni-directional: the Order Headers view is composed
with the Order Details but the Order Details must also be composed with the 
Order Header!

Consider the OE Order Header. In the example above, the header is only 
partially composed. It can be composed with up to five other views, each of
which can be composed with many others. Fully composing the OE Header View
involves opening and composing 13 other views, a total of 26 lines.

The :py:meth:`extools.view.ExView` class is self-composing, so you don't need
to worry about opening and checking the views or playing the shell game with
compose arguments.

.. code-block:: python

    # ExViews use exceptions, wrap it all in a try and provide helpful
    # output if an error is encountered.
    try:
        # Open the Order Header view
        oe0520 = ExView("OE0520")     
        # Fully compose it, creating a new property for each related view
        oe0520.compose()
        # Set the order to search by ORDNUMBER
        oe0520.order(1)
        # Seek to the order we want
        oe0520.seek_to(ORDNUMBER="ORD453")

        # For each detail line in the order
        for line in oe0520.oe0500.lines():

            # For each lot in the detail line
            for lot in line.oe0507.lines():

                # Get the lot number
                lotnumf = lot.get("LOTNUMF")

                # Check the condition
                if lotnumf and lotnumf.startswith("X"):

                    # Use the setOptionalField helper from the ExView class
                    oe0501.setOptionalField("MYFIELD", "HASX")

    except ExViewError as e:
        showMessage("Failed to set MYFIELD: {}".format(e))
        return 1

The call to :py:meth:`extools.view.ExView.compose` introspects the view to
find the other views that it can be composed with.  It then opens them all with
the correct indexing and composes them with one another.  Each composed view is
set as a property of the parent view so you can access them easily. 

In the manual compose example, the views ``OE0500``, ``OE0501``, ``OE0507``,
and ``OE0520`` were composed together.  The "compose tree" for those views is::

    OE0520
       |_ OE0500
            |_ OE0520
            |_ OE0501
            |     |_ OE0500
            |_ OE0507
                  |_ OE0500

Composing the ``OE0520`` ``ExView`` creates the following properties on the 
``exview`` instance::

    exview = ExView("OE0500")
    exview.compose()
                                
    OE0520                      exview
       |_ OE0500                exview.oe0500
            |_ OE0520           exview.oe0500.oe0520 (back to self)
            |_ OE0501           exview.oe0500.oe0501
            |     |_ OE0500     exview.oe0500.oe0501.oe0500 (back to parent)
            |_ OE0507           exview.oe0500.oe0507
                  |_ OE0500     exview.oe0500.oe0507.oe0500 (back to parent)

Note that because views are often composed bi-directionally, each composed
view has a property that links back to its parent.

