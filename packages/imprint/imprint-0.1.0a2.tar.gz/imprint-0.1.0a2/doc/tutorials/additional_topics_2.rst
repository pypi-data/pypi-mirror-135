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


.. _t_additional_2:

=========================
Additional Topics, Part 2
=========================

This tutorial covers some of the topics not covered in the
:doc:`basic_tutorial`. The focus here is on how to set up proper styling
through :ref:`configuration-docx` and how to utilise plugins to their fullest
potential. A basic understanding of the topics covered in the
:doc:`basic_tutorial` is assumed. A passing understanding of the concepts in
:doc:`plugin_tutorial` may be required for an in-depth understanding.

For a tutorial covering topics more targeted towards content and configuration
through :ref:`configuration-xml` and :ref:`configuration-ipc`, see
:doc:`additional_topics_1`.


.. _t_additional_2-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_additional_2-project:

-------
Project
-------

The project for this tutorial is :download:`Invoice </demos/Invoice.zip>`. The
discussion will only focus on the relevant portions of the relevant files, so
readers are encouraged to download and extract the entire project before
delving into the tutorial.

There will also be sections that demonstrate how to work through the MS Word
user interface, as well as some XML formatting in a text editor.

The document created in the project will contain a made up customer invoice,
along with a letter to the customer. It will look something like this:

.. figure:: /_static/Invoice\ Output.png
   :name: t_additonal_2-output
   :scale: 50%
   :figwidth: 100%

   The output of the Invoice example.

The project uses two custom plugins and one built-in one to process the data.
The plugins are implemented in
:download:`invoice.py </demos/Invoice/templates/invoice.py>` and registered in
:download:`Company.iif </demos/Invoice/templates/Company.iif>`. If you have not
done so already, read through the :ref:`t_plugin-using` portion of the
:ref:`t_plugin` tutorial.


.. _t_additional_2-image-logging:

-------------
Image Logging
-------------

Images that are generated for the document can be "logged" by copying them into
the log directory, or if conventional logging is disabled, into to the document
output directory. Image logging also applies to strings, LaTeX equations, and
sometimes tables (all the common handlers implement it). For common handlers
that just insert images or table data as-is into a document, this is not much
of an advantage. However, when a figure handler generates a complex image or
chart from scratch, it is often useful to have it output to disc as well as
using it from memory.

Image logging is controlled by the :ref:`keywords-system-log_images`
:ref:`system keyword <keywords-system>` in the :ref:`configuration-ipc`:

.. literalinclude:: /demos/Invoice/Invoice.ipc
   :language: python
   :name: t_additional_2-image-logging-ipc
   :caption: :download:`Invoice.ipc </demos/Invoice/Invoice.ipc>`, lines 18-19,
             showing the :ref:`keywords-system-log_images` setting.
   :lineno-start: 18
   :lines: 18-19
   :emphasize-lines: 2

Image logging is not enabled by default. With logging turned on, you will see
the following additional files in your output directory:

- ``Invoice_authorized_signature.png``

  This is the only actual image that is logged. It is a copy of the
  authorization signature that is inserted by the :ref:`xml-spec-tags-figure`
  tag in the :ref:`configuration-xml`:

  .. literalinclude:: /demos/Invoice/templates/Invoice.xml
     :language: xml
     :name: t_additional_2-image-logging-xml-png
     :caption: :download:`Invoice.xml </demos/Invoice/templates/Invoice.xml>`,
               lines 57-65, emphasizing where the signature is generated.
     :lineno-start: 57
     :lines: 57-65
     :emphasize-lines: 5

- ``Invoice_damage_assessment.txt``

  This is the output of the :ref:`xml-spec-tags-string` tag in the
  :ref:`configuration-xml`. Strings are dumped into a text file for inspection,
  since they are generated content, like images.

  .. literalinclude:: /demos/Invoice/templates/Invoice.xml
     :language: xml
     :name: t_additional_2-image-logging-xml-txt
     :caption: :download:`Invoice.xml </demos/Invoice/templates/Invoice.xml>`,
               lines 25-29, emphasizing where the custom string is inserted.
     :lineno-start: 25
     :lines: 25-29
     :emphasize-lines: 3

- ``Invoice_financial_data.csv``

  This is a copy of the financial data that is used to do the damage assessment
  and to generate the actual invoice. It is generated in response to the
  :ref:`xml-spec-tags-table` tag in the :ref:`configuration-xml`:

  .. literalinclude:: /demos/Invoice/templates/Invoice.xml
     :language: xml
     :name: t_additional_2-image-logging-xml-csv
     :caption: :download:`Invoice.xml </demos/Invoice/templates/Invoice.xml>`,
               lines 84-92, emphasizing where the invoice table is generated.
     :lineno-start: 84
     :lines: 84-92
     :emphasize-lines: 5

  Tables are not required to dump their data unless it really makes sense to
  do so. Due to the relatively flexible structure of tables in Word documents,
  the plugin itself is responsible for how the data is to be written. Other
  plugins rely on the tag to do their logging for them.

  .. todo:: Some of the last paragraph above probably belongs in the plugin
            tutorial, not here.


.. _t_additional_2-sections:

------------------
Inserting Sections
------------------


.. _t_additional_2-breaks:

--------------------
Line and Page Breaks
--------------------

The built-in tags support two types of breaks: line and page breaks. Both are
to be found in the :download:`Invoice </demos/Invoice.zip>` sample project.


.. _t_additional_2-breaks-line:

Line Breaks
===========

Line breaks are placed directly in a run of text using the
:ref:`xml-spec-tags-n` tag:

.. literalinclude:: /demos/Invoice/templates/Invoice.xml
   :language: xml
   :name: t_additional_2-breaks-xml-line
   :caption: :download:`Invoice.xml </demos/Invoice/templates/Invoice.xml>`,
             lines 39-44, showing how line breaks are inserted.
   :lineno-start: 39
   :lines: 39-44
   :emphasize-lines: 2, 3, 4

The result is a single run of text, but broken over multiple lines in a
controlled manner:

.. figure:: /_static/Invoice\ Line\ Breaks.png
   :name: t_additonal_2-line_breaks
   :scale: 100%
   :figwidth: 100%

   A made up address formatted with explicit line breaks.

Line breaks can only appear in a run of text. If they appear anywhere within a
:ref:`xml-spec-tags-par` tag, an attempt will be made to find or even create a
suitable run for the line break. However, outside a paragraph,
:ref:`xml-spec-tags-n` gets ignored completely, with a warning.


.. _t_additional_2-breaks-page:

Page Breaks
===========

Unlike line breaks, page breaks can appear just about anywhere. This includes
:ref:`xml-spec-tags-run` and :ref:`xml-spec-tags-par` tags, as well as the
:ref:`document root <xml-spec-root>`.

Page breaks are inserted with a :ref:`xml-spec-tags-break` tag:

.. literalinclude:: /demos/Invoice/templates/Invoice.xml
   :language: xml
   :name: t_additional_2-breaks-xml-page
   :caption: :download:`Invoice.xml </demos/Invoice/templates/Invoice.xml>`,
             lines 63-72, showing how a page break can be used.
   :lineno-start: 63
   :lines: 63-72
   :emphasize-lines: 5

The page break in this example separates the signature in the preface letter
from the page containing the actual customer invoice. Usually, page breaks
appear between paragraphs, as in this example, but that is not a requirement.

When a page break cuts a run or paragraph in two, a new paragraph and/or run
with the same style is really created on the next page.


.. _t_additional_2-headers-footers:

-----------------------------
Modifying Headers and Footers
-----------------------------


.. _t_additional_2-headers-footers-kwds:

Adding Keyword Replacement Directives
=====================================


.. _t_additional_2-headers-footers-xml:

Massaging the Internal XML
--------------------------
