extools.view.query
------------------

The ExQuery class, modelled loosely on Django's QuerySet and
JS semantics for method chaining, makes it easy to get at and
manipulate the data you need.

Data can generally be accessed quickly through the view if the
record you're searching for is indexed using the fields you're using
to look.  If you're off index, access through the view will require
programmatic filtering and can be cumbersome. In these cases, using SQL through
CS0120 is preferred.  

ExQuery selects the right method based on the view and query terms
in use.  If the data can be quickly retrieved from the view, ExQuery
retrieves data through the view.  Otherwise, it will autmatically
build an SQL query to retrieve the objects for you.

For example, can you iterate over all orders for a customer?  Although
CUSTOMER is a key field of OE0520 (OEORDH), you can't put to it in an
empty view, so SQL is the right approach.  ExQuery abstracts this away.

.. code-block:: python

    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200')
        for result in results:
            showMessageBox(result.ordnumber)

ExQueries can be refined by adding more terms, which are AND'd together.
All orders for customer 1200 shipped to the warehouse:

.. code-block:: python

    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200', SHIPTO='WAREHS')
        for result in results:
            showMessageBox(result.ordnumber)

You can also limit the number of results, from a particular offset if required,
and control the ordering.  Get the 11 - 20 orders for customer 1200, ordered
by item total descending:

.. code-block:: python

    # Pagination style example
    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200').order_by('ITMINVTOT').limit(10).offset(10)
        for result in results:
            showMessageBox(result.ordnumber)

You can chain where clauses as well. Get the 11 - 20 orders for customer 1200
that shipped to the warehouse, ordered by the total item amount descending:

.. code-block:: python

    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200').order_by('ITMINVTOT').limit(10).offset(10)
        # I want the same query results but with a ship to filter
        results = results.where(SHIPTO='WAREHS')
        for result in results:
            showMessageBox(result.ordnumber)

The example above is not as inefficient as it may seem.  The query is not
executed until results are actually read.  The database isn't accessed
until the beginning of the for loop, when results is first read from.
The first query, without the SHIPTO qualifier, is never executed.

What about cases where you may need an OR?  Orders for customer 1200 or 1100?
ExQuery results can be combined like sets.  So you can get their union (|),
intersection (&), or difference (-) between two results sets.

.. code-block:: python

    with exview("OE0520") as orders:
        c1_results = orders.where(CUSTOMER='1200')
        c2_results = orders.where(CUSTOMER='1100')
        # find the union of the two result sets
        results = c1_results | c2_results
        for result in results:
            showMessageBox(result.ordnumber)

How about writing back?  You can do that too.  Set all orders for
customer 1200 shipping to the warehouse on hold:

.. code-block:: python

    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200').where(SHIPTO='WAREHS')
        for result in results:
            result.update(ONHOLD=1)

Every result row in an ExQuery results maintains it's primary key.
When you update a result, the update is made through the view,
which is seeked directly to the correct record using the stored key.

You can treat an ExQuery like a list: index and slice it however you
like:

.. code-block:: python

    with exview("OE0520") as orders:
        results = orders.where(CUSTOMER='1200').order_by("ORDTOTAL")
        # most expensive order outstanding is first:
        most_expensive = results[0]
        # least expensive is last
        least_expensive = results[-1]
        # Top ten orders
        top_ten = results[0:10]

