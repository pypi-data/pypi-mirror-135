Tests
-----

Automated tests have been built for as much of the code as possible.

Code that can run without ``accpac`` is tested using standard Python
`unittest`_.

.. _unittest: https://docs.python.org/3/library/unittest.html

Code that needs accpac has to be run through the Sage Desktop, or
mocked extensively (more to come). Tests are written using the
:py:class:`extools.test.ExTestCase` class to make  developement and execution
through the desktop easy.

Check out the tests for the project to get an understanding of how to test code 
for Extender or to get a feel for the extools internals.

.. toctree::

   tests/extools
   tests/exview

