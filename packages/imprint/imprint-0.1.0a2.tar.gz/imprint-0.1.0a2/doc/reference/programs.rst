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

.. Author: Joseph Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>
.. Version: 13 Apr 2019: Initial Coding


.. _programs:

========
Programs
========

Imprint comes with a set of command-line entry points to facilitate different
tasks. This page is the manual for these programs.

.. _programs-toc:

.. contents:: Contents
   :depth: 2
   :local:


.. program:: imprint

.. _programs-imprint:

-------
imprint
-------

The main program of Imprint, serving as the entry point to create documents.


.. _programs-imprint-command:

Command
=======

The same command can be run on both Linux and Windows systems. The Windows file
that provides the executable has a ``.bat`` extension and delegates to the
extension-less Python file::

     imprint configuration


.. _programs-imprint-options:

Options
=======

.. option:: configuration

   :program:`imprint` accepts a single argument, the :ref:`configuration-ipc` to
   process.


.. program:: docx2xml

.. _programs-docx2xml:

--------
docx2xml
--------

A small utility for extracting text content out of existing Word documents.

Placeholders are inserted for every element that appears to be a table or a
figure. No attempt is made to preserve the styles of those elements. Paragraph
styles are preserved, as are run styles. An attempt is made to merge as many
consecutive runs of the same style as possible.

This program can only operate on ``.docx`` files, not on ``.doc`` files.


.. _programs-docx2xml-command:

Command
=======

The same command can be run on both Linux and Windows systems. The Windows file
that provides the executable has a ``.bat`` extension and delegates to the
extension-less Python file::

    docx2xml input[.docx] [output[.xml]]


.. _programs-docx2xml-options:

Options
=======

.. option:: input

   The input DOCX file to parse. A ``.docx`` extension will be appended to the
   file name if not already present. ``.doc`` extensions will only have one
   letter appended.

.. option:: output

   The output XML file to create. A ``.xml`` extension will be appended to the
   file name if not already present. If the name is missing entirely, the base
   name of :option:`input` will be used, with the ``.docx`` extension replaced
   by ``.xml``.

