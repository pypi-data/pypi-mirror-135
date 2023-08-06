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


.. _future-work:

===========
Future Work
===========

This section details some of the prominent features that are currently being
proposed or already implemented for Imprint, but are not a part of the main
baseline. This is not an exhaustive list, and does not contain any of the minor
bug fixes and enhancements that come naturally with any project of this scope.

Further requests and issues should be raised on the GitHub `issues`_ page.


.. _future-work-xml-root:

Configurable XML Root Tag
=========================

The name of the XML root tag can be configured through a key in the
:ref:`*.ipc <configuration-ipc>`. If the ``input_xml_root`` keyword is missing,
the default will remain ``imprint-template``.


.. _future-work-mathml:

Full MathML Support
===================

Imprint will have full MathML support out of the box. At the moment, the details
of the interface are being worked out. Currently, a ``<math>`` tag simply
includes all the XML found inside it verbatim into the OOXML document structure.


.. _future-work-caching:

Caching of Data
===============

Rather than ensuring that the same loader is used for all datasets, as the
current system does, it is better to create a cache of weak references to named
datasets, with clear loading instructions by data name rather than handler name.
This will improve the speed of Imprint (and is therefore not of prime
importance).


.. _future-work-user-defaults:

User Defaults File
==================

Create a file with user-level defaults. This will be a ``.imprint`` file in the
user directory on Linux Systems. It will be a mix of default
:ref:`configuration-ipc` and options for hard coded default styles, as well as
anything else that the user uses consistently as a fallback.

An environment variable, something like ``IMPRINTDEFS`` will allow the user to
override this option, along with a ``-D`` command-line option to
:program:`imprint`.


.. _future-work-anchors:

Clickable Anchors
=================

``<figure-ref>``, ``<table-ref>`` and especially ``<segment-ref>`` tags should
be replaced with a clickable link-field in the output document. This won't
affect the printed version much, but would be a very nice feature to have.


.. _future-work-pptx:

PowerPoint Presentations
========================

Since the `python-pptx`_ library supports a similar low-level interface to
`python-docx`_, it is possible to eventually extend Imprint to generate
PowerPoint presentations. This is not a high priority because the nature of the
PowerPoint medium is such that most presentations tend to be very unique. Word
documents tend to be more suitable for cookie cutter generation.


.. _future-work-pdf:

PDF Documents
=============

While this migration/support may be desirable from a portability standpoint, MS
Word is fairly ubiquitous, and PDFs are not as editable. This is also a low
priority item.


.. _future-work-default-docx:

Default DOCX Stub
=================

Given :ref:`future-work-user-defaults`, a default docx stub will be referenced
in that file, which will guarantee the existence of all the referenced styles.
This allows detailed per-organization or per-project configuration of the styles
that get used.


.. _future-work-section-tag:

Section Tag
===========
The :ref:`xml-spec-tags-section` tag can also specify the page-break type, the
margins and the gutter.


.. _future-work-default-plugin-prefix:

Default Plugin Prefix
=====================

Add a single default prefix to A) the config file, which would override the
B) :ref:`future-work-user-defaults` value. The default-default should be
something like ``imprint.handlers``.


.. include:: /link-defs.rst
