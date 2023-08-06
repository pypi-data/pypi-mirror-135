.. imprint: a program for creating documents from data and content templates

.. Copyright (C) 2019  Joseph R. Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>

.. This program is free software: you can redistribute it and/or modify
.. it under the terms of the GNU Affero General Public License as
.. published by the Free Software Foundation, either version 3 of the
.. License, or (at your option) any later version.

.. This program is distributed in the hope that it will be useful,
.. but WITHOUT ANY WARRANTY; without even the implied warranty of
.. MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
.. GNU Affero General Public License for more details.

.. You should have received a copy of the GNU Affero General Public License
.. along with this program. If not, see <https://www.gnu.org/licenses/>.

.. Author: Joseph Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>
.. Version: 13 Apr 2019: Initial Coding


.. _installation:

==================
Installation Guide
==================

This document explains how to install Imprint.


.. _installation-install:

----------------------
Installing the Package
----------------------


.. _installation-pypi:

PyPI
====

Imprint is available via `pypi`_, so the recommended way to install it is ::

    pip install imprint[all]

The extra ``[all]`` installs most of the :ref:`dependencies` necessary to
generate simple images and tables. It can be omitted for a bare-bones
install.


.. _installation-source:

Source
======

Imprint uses `setuptools`_, so you can install it from source as well. If you
have a copy of the source distribution, run ::

    python setup.py install

from the project root directory, with the appropriate privileges. A source
distribution can be found on `PyPI`_ as well as directly on `GitHub`_.

You can do the same thing with :program:`pip` if you prefer. Any of the
following should work, depending on how you obtained your distribution ::

    pip install git+<URL>/imprint.git@master[all]  # For a remote git repository
    pip install imprint.zip[all]                   # For an archived file
    pip install imprint[all]                       # For an unpacked folder or repo

See the page about :doc:`dependencies` for a complete description of additional
software that may need to be installed. Using :program:`setup.py` or
:program:`pip` should take care of all the Python dependencies.


.. _installation-demos:

-----
Demos
-----

Imprint is packaged with a set of demo projects intended primarily for the
:doc:`tutorials/tutorials`. The demos are not normally installed as part of
Imprint, Instead, they are to be accessed through the source repository or the
documentation :ref:`installation-documentation`, once that is built. See
:ref:`tutorials-demos` for a complete list.


.. _installation-tests:

-----
Tests
-----

Imprint does not currently have any formal unit tests available. However,
running through all of the demos serves as a non-automated set of tests, since
they exercise nearly every part of Imprint. Eventually, pytest-compatible tests
will be added in the :py:mod:`~imprint.tests` package.


.. _installation-documentation:

-------------
Documentation
-------------

If you intend to build the documentation, you must have `Sphinx`_ installed,
and optionally the `ReadTheDocs Theme`_ extension for optimal viewing. See the
:ref:`dependencies spec <dependencies-documentation>` for more details.

The documentation can be built from the complete source distribution by using
the specially defined command::

    python setup.py build_sphinx

Alternatively (perhaps preferably), it can be built using the provided
Makefile::

    cd doc
    make html

Both options work on Windows and Unix-like systems that have :program:`make`
installed. The Windows version does not require :program:`make`. On Linux you
can also do ::

    make -C doc html

Building the documentation will also make a copy of the
:ref:`installation-demos`.

The documentation is not present in the `PyPI`_ source distributions, only
directly from `GitHub`_.


.. include:: /link-defs.rst
