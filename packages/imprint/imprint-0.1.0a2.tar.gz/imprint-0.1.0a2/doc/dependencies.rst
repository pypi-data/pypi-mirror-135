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
.. along with this program.  If not, see <https://www.gnu.org/licenses/>.

.. Author: Joseph Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>
.. Version: 13 Apr 2019: Initial Coding


.. _dependencies:

============
Dependencies
============


.. _dependencies-python:

------
Python
------

Imprint requires Python version 3.6 or higher.


.. _dependencies-core:

----
Core
----

The core program depends only on three libraries in addition to the built-in
Python libraries:

- `python-docx`_: A library for creating documents in Office Open XML format.
- `lxml`_: An XML manipulation libarary that is also a dependency of
  `python-docx`_.
- `haggis`_: A suite of Python utilities developed by the author of Imprint to
  support common functionality across multiple tools, including Imprint itself.
  All additional dependencies come indirectly from Haggis.

Content-generation plugins generally tend to have a much wider set of
dependencies.


.. _dependencies-documentation:

-------------
Documentation
-------------

This documentation is built with `sphinx`_ (version >= 1.7.1 required).

The API documentation requires the `napoleon`_ extension, which is now bundled
with sphinx itself.

The default viewing experience for the documentation is provided by the
`ReadTheDocs Theme`_, which is, however, optional. If installed, a version
>= 0.4.0 is recommended\ [#rtd]_.


.. _dependencies-plugins:

-------
Plugins
-------

There is almost no restriction on what Imprint plugin code can depend on. In
fact, plugins can use a wide variety of open source tools and libraries for
tasks like graphics rendering and file conversion. Both Python libraries and
external programs can be dependencies for plugins, since the Python
:py:mod:`subprocess` module supports running arbitrary executables. The lists
below show a sample\ [#sample]_ of dependencies used by the :ref:`builtin
<plugins-builtin>`:


.. _dependencies-plugins-python:

Python Packages
===============

- `numpy`_: A fast array library for Python. This supports most of the data
  processing done in Imprint as numpy arrays are virtually ubiquitous in Python.
  This is a dependency of `scipy`_ and `pillow`_.
- `scipy`_: A scientific computation libary for Python. In addition to
  enhancements to numpy, it supplies interfaces to scientific file formats such
  as IDL files.
- `matplotlib`_: A plotting and graphics library for Python. Much of the data
  visualization is done through this library.
- `pandas`_: A spreadsheet library for easily manipulating tables.
- `pillow`_: A graphics file library for Python. Used to import images and
  convert image files.
- `natsort`_: A small natural text-sorting algorithm for Python. It provides
  advanced sorting techniques that are more intuitive than plain
  lexicorgaphical sorting, e.g., for strings containing both text and numbers.


.. _dependencies-plugins-external:

External Programs
=================

- `ImageMagick`_: A suite of image conversion programs suitable for almost any
  reasonable format. Mostly the :program:`convert` program is used, e.g., to
  create `LaTeX`_ equations for the :ref:`xml-spec-tags-latex` tag.
- `Poppler`_: A library for manipulating PDF files. In particular the
  :program:`pdftoppm` program is used to convert PDF files into importable
  images.
- `GhostScript`_ (:program:`gs`): Converts PostScript documents into importable
  images. This is particularly useful for dealing with some of the more
  flexible backends provided by `matplotlib`_, especially when it comes to
  `LaTeX`_ equations.
- `LaTeX`_: Some implementation of LaTeX is necessary to support in-text LaTeX
  equations. :program:`texlive` and :program:`pdflatex` are examples of
  implementations that have been used successfully in testing on Linux systems.
  Only documents containing the :ref:`xml-spec-tags-latex` XML tag require this.
- `dvips`_: A converter between `DVI`_ and PostScript formats is necessary
  to bridge the formats supported by :program:`latex` and :program:`convert`.
  This is only a dependency for documents that contain
  :ref:`xml-spec-tags-latex` tags. This program is almost always bundled with
  reasonable :program:`LaTeX` distributions.

Dependence on external programs generally represents a restriction to
portability across platforms. This is often not a major issue because many
standard programs are available for Linux and Mac environments, and generally,
a particular coniguration of Imprint plugins will be used in a fairly static
environment.


.. rubric:: Footnotes

.. [#rtd] Versions prior to 0.4.0 had issues with the alignment of line numbers
   to code in the tutorial examples.
.. [#sample] These lists are not exhaustive, but should cover most of the
   interesting items encountered in general use. All items required for the
   :ref:`plugins-builtin` *are* covered.

.. include:: /link-defs.rst
