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


.. _configuration:

===========================
Imprint Configuration Files
===========================

This page contains a summary of the different files that users must provide to
have :program:`imprint` operate properly. Most of the files have their own
reference pages and tutorial sections.

The different types of files are normally referred to by their extension.
However, since internally files are always referenced to by their full name,
none of the extensions listed here are actually mandatory. They are a default
choice made for clarity and aesthetics, not functionality.


.. _configuration-toc:

.. contents:: Contents
   :depth: 2
   :local:


.. _configuration-ipc:

--------
IPC File
--------

The Imprint Program Configuration (IPC) file is the main script for a given
output of :program:`imprint`. It contains a set of :ref:`keywords` mapped to
values. Some of the keywords reference the other configuration files and
configure the :ref:`introduction-layers-engine`; others provide the user-defined
data for content generation. The former are referred to as
:ref:`keywords-system`, while the latter are :ref:`keywords-user`.

The file is written using Python syntax. Keywords are normal Python names. All
the restrictions that apply to Python variable names apply to keyword names.
Traditionally, :ref:`keywords-system` which direct the operation of the
:ref:`introduction-layers-engine` start with lowercase letters, while
:ref:`keywords-user` containing per-document data start with uppercase letters.
Any keyword starting with a dunder (double underscore / ``__``) is for internal
use by the configuration file, and will not be exposed to the core at all.
Modules imported into the configuration will not be exposed either.


.. _configuration-ipc-paths:

Paths
=====

Relative paths are resolved from the directory containing the
:ref:`configuration-ipc`, not the current directory. This makes it easy to copy
entire configurations to different locations, and have them work out of the
box. It also allows a user to generate multiple documents correctly without
changing directories, and generally removes any dependence on the current
directory.

In particular, this applies to the following system keywords, which are
expected to contain a path or paths:

- :ref:`keywords-system-data_config`
- :ref:`keywords-system-includes`
- :ref:`keywords-system-input_docx`
- :ref:`keywords-system-input_xml`
- :ref:`keywords-system-log_file`
- :ref:`keywords-system-output_docx`


.. _configuration-idc:

--------
IDC File
--------

A Imprint Data Configuration (IDC) file complements the core configuration of
the :ref:`configuration-ipc` by supplying the data configuration mappings for
the :ref:`introduction-layers-plugins`. The data configuration is referenced by
the :ref:`keywords-system-data_config` keyword.

Like the :ref:`configuration-ipc`, the :ref:`configuration-idc` uses Python
syntax. It follows a similar loading convention of removing any names starting
with a dunder (double underscore / ``__``) from the loaded namespace. Unlike
:ref:`configuration-ipc`, recursive includes are not allowed.

Each name in the global namespace of the :ref:`configuration-idc` corresponds
to a plugin configuration. Normally, all the visible names in the file are
Python dictionaries, but other mapping types are allowed.

The builtin :ref:`xml-spec-tags-figure`, :ref:`xml-spec-tags-table` and
:ref:`xml-spec-tags-string` tags support plugins. The plugins are structured so
that unnecessary keys are silently ignored, making it possile to share data
configuration across multiple tags. For example, a figure and a table generated
from the same data set can share a data configuration, and therefore avoid the
redundancy of repeated data source specs.


.. _configuration-idc-names:

Configuration Names
===================

Plugin tags in the :ref:`configuration-xml` are mapped to their configuration
objects by a special attribute, usually ``id``. The name of the attribute is
set for each plugin's :ref:`descriptor <tag-api-descriptors>`.

A missing configuration aborts the generation of its particular content, but
does not necessarily constitute a :term:`fatal error`.


.. _configuration-iif:

---------
IIF Files
---------

Imprint Include Files (IIF) have the exact same format as the main
:ref:`configuration-ipc`. Their purpose is to share content between multiple
document configurations, using the :ref:`keywords-system-includes` keyword.

Include files are intended to supplement the main configuration file. The main
configuration automatically overrides any duplicate keys that are found in the
includes.

Includes may be done recursively. Since the engine does not check for infinite
loops, use this feature carefully.


.. _configuration-xml:

------------
XML Template
------------

The XML template defines the structure and content of the document. A full
specification of the XML structure is given in :doc:`xml_spec`. Additional
features can be added through the :doc:`tag_api`. The template is referenced by
the :ref:`keywords-system-input_xml` keyword.


.. _configuration-docx:

---------
DOCX Stub
---------

The DOCX stub is an empty template document that defines all of the styles and
formatting. All the styles referenced explicitly in the
:ref:`configuration-xml`, as well as the implicit default styles must exist
in the stub. The stub is also responsible for setting up the page numbering,
headers and footers. The stub is referenced by the
:ref:`keywords-system-input_docx` keyword.


.. _configuration-docx-headers-footers:

Headers and Footers
===================

Headers and footers in the template may contain any number of keyword
replacement directives in their text. These directives are the name of a
keyword surrounded by curly braces (``{...}``), and optionally containing
additional formatting instructions in the Python :ref:`formatstrings`.

Header and footer keyword replacement occurs as a post-processing step after
the output document has been created and written to disk. If a
:ref:`keywords-system-date` key is not defined in the :ref:`configuration-ipc`,
it is implicitly set to a :py:class:`~datetime.datetime` representation of the
current date and time for the duration of this particular post-processing step.

Any directives that can not be replaced for any reason are left exactly as-is
in the output document. The following example footer text:

.. parsed-literal::

   Current Date: {date:%B %d, %Y} ID: {0001-0234-4455-0708}

would result in the follwing replacement:

.. parsed-literal::

   Current Date: |today| ID: {0001-0234-4455-0708}


.. .. _configuration-global:
.. 
.. --------------------
.. Global Defaults File
.. --------------------
