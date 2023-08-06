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


.. _t_styles:

=====================
Styles and Formatting
=====================

This section demonstrates how to apply styles and formatting to the document at
every level.


.. _t_styles-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_styles-defining:

---------------
Defining Styles
---------------


.. _t_styles-applying:

---------------
Applying Styles
---------------


.. _t_styles-pages:

Pages
=====


.. _t_styles-paragraphs:

Paragraphs
==========


.. _t_styles-paragraphs-headings:

Headings
--------


.. _t_styles-paragraphs-lists:

Lists
-----

The :ref:`t_additional_1-lists` tutorial explains how to create lists. For
simple lists, a default paragraph style is automatically selected, based on
whether the list is numbered or bulleted. Anything more complicated will
require explicitly setting a style.

A good example of when to use explicit list styles is when a list item contains
multiple paragraphs. Consider the following snippet:

.. literalinclude:: /demos/Snippets/ListStyles.xml
   :language: xml
   :name: _t_additional-lists-extend-code
   :caption: Snippet showing an extended list.
   :linenos:
   :lines: 3-17
   :emphasize-lines: 7

The result is a multi-paragraph list item for item #1. If we had not explicitly
added the same style to the middle paragraph, its indentation would not have
been correct for a list item:

.. figure:: /_static/ListStyles\ Output.png
   :name: t_styles-paragraphs-lists-output
   :scale: 65%

   Detail of an extended list continued over multiple paragraphs.

.. todo::

   Add a big blurb about the fact that this only works because the default
   list styles are sensibly set in the global defaults file. If not, the
   most default default list style is actually not very useful (indents by 4
   tabs).


.. _t_styles-runs:

Runs
====


.. _t_styles-figures:

Figures
=======


.. _t_styles-tables:

Tables
======


.. _t_styles-equations:

Equations
=========


.. _t_styles-defaults:

--------
Defaults
--------

