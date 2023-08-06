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


.. _t_basic:

==============
Basic Tutorial
==============

This tutorial offers a more realistic example of how to set up a simple project
from scratch than the :doc:`getting_started` page. For this tutorial, we will
create a somewhat contrived, but fairly polished document describing a made-up
series of candle flame height measurements.


.. _t_basic-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_basic-setup:

-------------
Project Setup
-------------

The files for this tutorial are available in the
:download:`CandleFlame example </demos/CandleFlame.zip>`. You may chose to
download and extract the provided archive, or start with an empty folder named
``CandleFlame`` and populate it as the tutorial progresses.

For this tutorial, we will emphasize the differences between the
:ref:`introduction-layers-configuration` and the
:ref:`introduction-layers-template`. Our templates (both
:ref:`configuration-xml` and :ref:`configuration-docx`), are placed in a
separate folder named ``CandleFlame/templates``. Normally, this folder would be
outside the document configuration entirely, so that it can be shared by
multiple documents. The :ref:`configuration-iif` will be placed here as well, to
emphasize their shared role.


.. _t_basic-plugins:

-------------
Using Plugins
-------------


.. _t_basic-plugins-configuration:

Creating a Data Configuration
=============================


.. _t_basic-plugins-figure:

Adding a Picture
================


.. _t_basic-plugins-table:

Adding a Simple Table
=====================


.. _t_basic-plugins-string:

Adding a Text File
==================


.. _t_basic-styles:

--------------------
Adding Custom Styles
--------------------


.. _t_basic-styles-stub:

Creating a Stub Document
========================


.. _t_basic-xml:

----------------------------
Customizing the XML Template
----------------------------


.. _t_basic-xml-expr:

Computing Keywords
==================


.. _t_basic-xml-toc:

Adding a TOC
============


.. _t_basic-xml-equations:

Inserting Equations
===================


.. _t_basic-keywords:

--------------
Using Keywords
--------------


.. _t_basic-keywords-include:

Adding Include Files
====================


.. _t_basic-keywords-log:

Enabling the Log
================
