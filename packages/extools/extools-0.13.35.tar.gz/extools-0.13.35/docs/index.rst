extools package
===============

.. toctree::
   :hidden:
   :maxdepth: 4

   src/extools
   src/view/exview
   src/message/exmessages
   src/test/extest
   src/ui/exui
   src/env/exenv
   src/report/exreport
   src/tests
   src/notes/notes

extools is created and maintained by `Poplar Development`_. The full source
is available on `Bitbucket`_.

.. _Poplar Development: https://poplars.dev
.. _Bitbucket: https://bitbucket.org/cbinckly/extools

Before we get started, what brings you here today?  Are you looking to...

- Work with the built-in Extender views but write more idiomatic code? 
  Check out :ref:`extools: foundation`.
- Write Extender scripts using ``try/except`` instead of ``if r != 0``,
  views that compose themselves, automatic optional field helpers,
  intelligent seek, and more? Try :ref:`extools.view` on for size.
- Handle messages and logging easily and consistently in your Extender 
  scripts?  Have a look at :ref:`extools.message`.
- Automate the testing of your code? The :ref:`extools.test` package
  may be just what you need.
- Get a better handle on the environment in which your scripts are running?
  is this being called from Process Scheduler, an import, or a view? 
  Helpers in :ref:`extools.env` may help.
- Write scripts that need to be run from the panel but don't need a UI?
  :ref:`extools.ui.bare` helps with that.
- Add a new column to pretty much any grid in just a few lines?
  :py:class:`extools.ui.callback_column.CallbackColumnUI`,
  :py:class:`extools.ui.datasource_column.DatasourceColumnUI`,
  :py:class:`extools.ui.optfield_column.OptfieldColumnUI` have you 
  covered.
  

extools: foundation
-----------------------

Full of little helpers that can be used to make Extender scripts more
idiomatic, these functions are the foundation for the other tools in the
package.  Things like checking the success of view operations in bulk, or
generators that yield all records in a view.  Instead of

.. code-block:: python

    _rc = view.recordClear()
    _br = view.browse("")

    if _rc != 0 or _br != 0:
        showMessage("Custom Script: failed to clear or browse.")
        return False
    
    while view.fetch() == 0:
        val = view.get("FIELD")
        # do stuff

Use the helpers in extools to make things more idiomatic.

.. code-block:: python

    from extools import (success, all_records_in, )
    
    _rc = view.recordClear()
    _br = view.browse("")

    # Avoid numeric comparisons that can be hard to understand.
    if not success(_rc, _br):
        # Generate messages
        alert("failed to clear or browse.")
        return False
    
    while success(view.fetch()):
        val = view.get("FIELD")
        # do stuff

    # alternatively, use a for loop and the all_records_in helper.
    for item in all_records_in(view):
        val = item.get("FIELD")

extools.messages: a simple logging framework for Extender scripts
-------------------------------------------------------------------

Messages provides the ExMessages class, which acts like a logger but 
shows messages on screen (as well as writing to a file if required).  It
provides configurable log levels, so the verbosity of the module
is easily controlled. 

Set it to DEBUG while developing and then to WARNING before releasing,
be confident that you haven't left a hanging debug message lying around.

Instead of having to uncomment those hidden showMessages when trying to
fix a problem in place, just change the log level and undo the Extender
script check-in when you've finished troubleshooting.  

And keep DRY. Set the log level once, and the message output format, along
with titles, once.  The user experience will be more consistent and the code
must easier to maintain.

.. code-block:: python

    from extools.message import ExMessages
    from extools.env import vidir_path

    exn = ExMessages("My Customization", 
                          level=ExMessages.INFO,
                          logpath=vidir_path / "mycust.log")

    # Write to the log and display a message box with "My Customization" as a
    # header and the message as content.
    exn.info("This is an info message.")

    # Would display a message box with "DEBUG - My Customization" as a header 
    # and the message as content but suppressed due to level.
    exn.debug("This is a debug message.")

    # Update the log level on the fly.
    exn.level = ExMessages.DEBUG

    # This time it will work.
    exn.debug("This is a debug message.")

As an added bonus messages logged at the panic, critical, and error level 
can include traceback information - allowing the capture of deep
tracebacks that exceed the Sage system message size.

.. code-block:: python
    
    # Append the traceback for the last exception to the
    # message.
    exn.error("This error occured!", exc_info=True)

extools.view: a wrapper around Extender views that raises
-----------------------------------------------------------

ExView is an exception raising wrapper around the standard Extender
View object.  It has some other extensions as well, such as built in
generators, that make working with with views more pythonic.

.. code-block:: python

    from extools.message import ExMessages
    from extools.view import ExView, ExViewError

    exm = ExMessages("MYMOD")

    try:
        # Open the AR Items view
        exv = ExView("AR0010")
        # Compose, adding the ar0009 (aritd) and ar0011 (aritt) views
        exv.compose()
        for item in exv.lines():
            for price in item.ar0009.lines():
                # Do some stuff with the item prices
    except ExViewError as e:
        # Use the descriptive message in the exception.
        exm.error("Failed to update pricing, {}.".format(e))

For more information on ExView's self-composing feature, see the 
doc on :ref:`Self-composing views`.

extools.env: details on the current execution env
-----------------------------------------------------------------

Sometimes you need details about the execution environment from
within a customization.  What is the VI root directory? Where
can I put a temp file? Is this script executing from Process Scheduler?

The environment package leverages Python's Path library to make working
with the environment easy.
