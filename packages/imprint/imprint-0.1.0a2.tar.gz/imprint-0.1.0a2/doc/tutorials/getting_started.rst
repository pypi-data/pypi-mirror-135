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


.. _t_start:

===============
Getting Started
===============

If you are a first time user, you have come to the right place. This tutorial
is the "Hello World!" example for Imprint. It demonstrates the most basic setup,
and hopefully explains some of the possible uses for Imprint in doing so. Most
of the material shown here is reiterated with more detail in the
:doc:`basic_tutorial`.


.. _t_start-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_start-setup:

----------------------
Creating a New Project
----------------------

The easiest way to set up a new project is usually to copy an existing one. If
that is not an option, create a new folder for your new project. All of the
:ref:`configuration-ipc-paths` in a project will be resolved relative to that
folder, so it will be self-contained.

If you would like to simulate copying an existing project, download and extract
the :download:`HelloWorld example </demos/HelloWorld.zip>`. If you would like
to start a new project, create a folder named ``HelloWorld`` somewhere, and
follow along with the rest of this tutorial. Unless otherwise stated, all the
files described below exist under the root ``HelloWorld`` folder.


.. _t_start-template:

Making a Template
=================

First let's begin by laying out the structure and content of our document in an
:ref:`configuration-xml`. Our basic template for this example will look like
this:

.. literalinclude:: /demos/HelloWorld/HelloWorld.xml
   :language: xml
   :name: _t_start-template-xml
   :caption: :download:`HelloWorld.xml </demos/HelloWorld/HelloWorld.xml>`: The
             document content and structure template.
   :linenos:

Let us inspect the contents of this file tag-by-tag to understand what is going
on.

The outermost :ref:`<imprint-template> <xml-spec-root>` tag is necessary to make
the XML into a Imprint template.

Document text is arranged into paragraphs, which are surrounded by
:ref:`xml-spec-tags-par` tags. Our example has only one such tag, and therefore
only one paragraph. The paragraph has a *Normal* style. Paragraphs can contain
different :ref:`xml-spec-tags-run`\ s of character-level formatting, but it is
fairly standard to have a single run with the *Default Paragraph Font* style.
This style means that all the paragraph-level styling information is left
untouched.

Finally, the innermost portion is the text of the paragraph. Our example
contains two elements: the literal word *Hello*, and a :ref:`xml-spec-tags-kwd`
tag. This tag tells the :ref:`introduction-layers-engine` to perform a
:ref:`keyword <keywords>` replacement. The name of the keyword is *What*. We
will see how to define the value of *What* next. This value will be placed
literally into the document, replacing the :ref:`xml-spec-tags-kwd` tag. You
can begin to imagine how this could be useful for generating multiple documents
from the same template.

.. note::

   Keep in mind that this template is very simple and easy to write. A normal
   Imprint template is usually quite large, and should be created only once for
   a large number of documents. Normally, the template will be stored outside
   the setup directory, where it can be accessed by many configurations.


.. _t_start-configuration:

Creating the Configuration
==========================

The second file we will create for this example is the
:ref:`program configuration <configuration-ipc>`. This file tells the
:ref:`introduction-layers-engine` what to do, in addition to setting up the
:ref:`keywords-user`, like *What*, required by the
:ref:`template <t_start-template>`. Here is our configuration file:

.. literalinclude:: /demos/HelloWorld/HelloWorld.ipc
   :language: python
   :name: t_start-configuration-ipc
   :caption: :download:`HelloWorld.ipc </demos/HelloWorld/HelloWorld.ipc>` The
             document configuration script.
   :linenos:

This is a simple Python file that defines some :ref:`keywords`.

Keywords starting with lowercase letters are :ref:`keywords-system`.
:ref:`keywords-system-input_xml` and :ref:`keywords-system-output_docx` are
both mandatory: Imprint will raise an error and abort immediately without them.
The former references the :ref:`template <t_start-template>` we just created,
while the latter gives the name of the output document.

:ref:`keywords-system-overwrite_output` is an optional system keyword. It tells
Imprint what to do if the output already exists. Setting it to ``'silent'`` as
we did here tells the engine to overwrite an existing output file without
further ado. You can omit this keyword entirely, but the default is to raise
an error if :ref:`keywords-system-output_docx` already exists.

Keywords starting with upppercase letters are :ref:`keywords-user`. Our example
only has one user-defined keyword: *What*. The value of this keyword is used to
replace the :ref:`xml-spec-tags-kwd` tag in our XML template.

The order of keywords does not matter. You can shuffle them however you want,
mix system and user defined keywords, and generally do whatever seems best.
However, since this is Python code, keywords can reference each other. In that
case, any keywords on the right hand side of the assignment must be defined
before they are referenced for the first time.

All of the paths in configuration files are resolved relative to the folder
containing the :ref:`configuration-ipc`. This means that you can copy the
entire folder, make some modifications to the configuration, and run it to get
an entirely different and independent document.


.. _t_start-run:

---------------
Running Imprint
---------------

You now have a working setup. :program:`imprint` is a command-line tool. You can
run it by passing in a single argument: the name of the
:ref:`configuration file <t_start-configuration>`. Assuming that your current
working directory is set to ``HelloWorld``, you can generate your first
document by doing ::

    imprint HelloWorld.ipc

That's it. you should now have a file called ``HelloWorld.docx``. If you open
it in MS Word, you will see

.. figure:: /_static/HelloWorld\ Output.png
   :name: t_start-running-output
   :scale: 75%

   The output of our first Hello World document.

The output will be the same (and in the same place) regardless of what
directory you run :program:`ipc` from.

In this simple example, we did not show the use of plugins, logging, or any of
the other advanced features of Imprint. Look into the other :doc:`tutorials`,
starting with the :doc:`basic_tutorial` for additional information.
