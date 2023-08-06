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


.. _t_additional_1:

=========================
Additional Topics, Part 1
=========================

This tutorial covers some of the topics not covered in the
:doc:`basic_tutorial`. The focus here is on the flexibility offered by the
configuration files, especially the :ref:`configuration-xml` and
:ref:`configuration-ipc`. A basic understanding of the topics covered in the
:doc:`basic_tutorial` is assumed.

For a tutorial covering topics more targeted towards formatting through the
:ref:`configuration-docx` and plugin usage, see :doc:`additional_topics_2`.


.. _t_additional_1-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_additional_1-project:

-------
Project
-------

The project for this tutorial is :download:`Games </demos/Games.zip>`. The
discussion will only focus on the relevant portions of the relevant files, so
readers are encouraged to download and extract the entire project before
delving into the tutorial.

The document created in the project will contain a couple of trivial lists of
board games just for illustration. The baseline version can be created using
:download:`Games.ipc </demos/Games/Games.ipc>`::

    imprint Games.ipc

The output ``Games.docx`` will look something like this:

.. figure:: /_static/Games\ Output.png
   :name: t_additonal_1-output
   :figwidth: 100%
   :align: left
   :scale: 40%

   The output of the Games example.


.. _t_additional_1-keywords:

-------------------
Overriding Keywords
-------------------

The :ref:`keywords-system-includes` system keyword is not only for
:ref:`configuration-iif`. It can also be used to modify portions of the
:ref:`configuration-ipc` in a traceable and repeatable manner.

Using the fact that included files can not override defined keywords, we can
define an :ref:`configuration-ipc` snippet that just overrides the keywords
that we want, and includes everything else from the original file:

.. literalinclude:: /demos/Games/Games0.ipc
   :language: python
   :name: t_additional_1-keywords-ipc
   :caption: :download:`Games0.ipc </demos/Games/Games0.ipc>`: Overriding the
             :ref:`keywords-system-caption_counter_depth`.
   :linenos:

The example show here is used to modify the
:ref:`keywords-system-caption_counter_depth` setting. The same technique can be
used equally well to modify other :ref:`keywords-system` as well as
:ref:`keywords-user`. Such modification is useful for testing and to create
documents that are closely related to each other in terms of most of their
configuration.

:download:`Games0.ipc </demos/Games/Games0.ipc>` and its siblings
:download:`Games2.ipc </demos/Games/Games2.ipc>`,
:download:`Games3.ipc </demos/Games/Games3.ipc>`, and
:download:`GamesNone.ipc </demos/Games/GamesNone.ipc>` are revisited
in the section on :ref:`t_additional_1-references-depth`.


.. _t_additional_1-lists:

------------
Making Lists
------------

Lists are created by setting the ``list`` attribute of the
:ref:`xml-spec-tags-par` tags. List items are just regular paragraphs with some
extra styling added on for bullets or numbering. A sample
:ref:`configuration-xml` with list items looks like this:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-lists-xml
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`: The
             content and structure template, with list items emphasized.
   :linenos:
   :emphasize-lines: 26, 28, 43, 45

To start a new list, set the ``list`` attribute to either ``numbered`` or
``bulleted``. Lines **26** and **43** in the example show how this is done.
The full word (which is case-insensitive by the way) can be spelled out, or
any prefix of it can be used, as in line **43**.

To append elements to a list, set ``list`` to ``continued``, as in lines
**28** and **45**. The list will be continued regardless of how many additional
paragraphs or other elements are placed between the list items. For example,
the figures on line **27**, **29** and **46** and table on line **44** do not
break up the numbering scheme of the two lists we created:

.. figure:: /_static/Games\ Output\ List1.png
   :name: t_additonal_1-lists-output1
   :figwidth: 100%
   :align: left
   :scale: 100%

   The first list of games, with figures between list items.

.. figure:: /_static/Games\ Output\ List2.png
   :name: t_additonal_1-lists-output2
   :figwidth: 100%
   :align: left
   :scale: 100%

   The second list of games, emphasizing the restarted numbering.

Additional information is available in the
:ref:`List Styling <t_styles-paragraphs-lists>` tutorial.


.. _t_additional_1-references:

-----------------
Adding References
-----------------

The text |Figure12 Reference Inline|, |Figure34 Reference Inline| and
|Segment1 Reference Inline| are dynamically generated reference names, which
are automatically derived from the position of the figure or heading in the
document outline.

The figure references are created by the :ref:`xml-spec-tags-figure-ref` tags
on lines **12**, **14** and **15**:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-references-xml1
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`, lines
             10-18, emphasizing the :ref:`xml-spec-tags-figure-ref`\ s.
   :lineno-start: 10
   :lines: 10-18
   :emphasize-lines: 3, 5, 6

Each :ref:`xml-spec-tags-figure-ref` identifies the figure it refers to by its
``id`` attribute. This is how most :ref:`tag-api-references` are identified.

The text reference on line **40** is greated by a
:ref:`xml-spec-tags-segment-ref` tag, which points to paragraphs. Since
paragraphs do not normally have an ``id`` attribute, they can be referenced by
``title`` instead:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-references-xml2
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`, lines
             39-41, emphasizing the :ref:`xml-spec-tags-segment-ref`\ .
   :lineno-start: 39
   :lines: 39-41
   :emphasize-lines: 2

The ``title`` of a :ref:`xml-spec-tags-segment-ref` is the
full text of the heading or other paragraph that is being pointed to, with all
the extra spaces and line-breaks removed:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-references-xml3
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`, lines
             20-24, emphasizing the heading title that the
             :ref:`xml-spec-tags-segment-ref` refers to.
   :lineno-start: 20
   :lines: 20-24
   :emphasize-lines: 3

Among builtin tags, :ref:`xml-spec-tags-figure` and :ref:`xml-spec-tags-par`
can be referenced by :ref:`xml-spec-tags-figure-ref` and
:ref:`xml-spec-tags-segment-ref`, respectively. We have not seen
:ref:`xml-spec-tags-table-ref` tags in the tutorial so far, which reference
:ref:`xml-spec-tags-table`\ s. :ref:`xml-spec-tags-table-ref` works just like
:ref:`xml-spec-tags-figure-ref`, but with "Table" in the reference name instead
of "Figure".


.. _t_additional_1-references-depth:

Setting the Caption Counter Depth
=================================

The formatting of the figure number for :ref:`xml-spec-tags-figure-ref` (and
table number for :ref:`xml-spec-tags-table-ref`\ ) is set by the
:ref:`keywords-system-caption_counter_depth`
:ref:`system keyword <keywords-system>`.

The default :ref:`keywords-system-caption_counter_depth` is 1, meaning that
only the top-level heading is considered when counting and naming figures. If
we were to change :ref:`keywords-system-caption_counter_depth` to say 2:

.. literalinclude:: /demos/Games/Games2.ipc
   :language: python
   :name: t_additional_1-references-depth-ipc2
   :caption: :download:`Games2.ipc </demos/Games/Games2.ipc>`: Overriding the
             :ref:`keywords-system-caption_counter_depth`, setting the depth to
             2.
   :linenos:

We would see two elements in the heading level, and the figure counter would
restart with every second-level heading instead of just the top level heading.
The references that previously looked like |Figure12 Reference Inline| and
|Figure34 Reference Inline| now look like |Figure212 Reference Inline| and
|Figure234 Reference Inline|.

This snippet provides additional illustration for
:ref:`t_basic-keywords-include`. We can use a similar technique to remove the
heading information from the references entirely, by setting
:ref:`keywords-system-caption_counter_depth` to zero:

.. literalinclude:: /demos/Games/Games0.ipc
   :language: python
   :name: t_additional_1-references-depth-ipc0
   :caption: :download:`Games0.ipc </demos/Games/Games0.ipc>`: Overriding the
             :ref:`keywords-system-caption_counter_depth`, setting the depth to
             0.
   :linenos:

These references show the figure counter for the whole document:
|Figure012 Reference Inline| and |Figure034 Reference Inline|.

The cases shown here are well-behaved. In the case where
:ref:`keywords-system-caption_counter_depth` is 2, all the references live in
a heading at least two deep, when it is zero, there can't be any problems at
all. But if :ref:`keywords-system-caption_counter_depth` is set to a number
that is greater than the outline depth of the heading containing the reference,
the missing levels are ignored:

.. literalinclude:: /demos/Games/Games3.ipc
   :language: python
   :name: t_additional_1-references-depth-ipc3
   :caption: :download:`Games3.ipc </demos/Games/Games3.ipc>`: Overriding the
             :ref:`keywords-system-caption_counter_depth`, setting the depth to
             3.
   :linenos:

In this case, the references will look identical to the ones with
:ref:`keywords-system-caption_counter_depth` set to 2.

To turn off the the truncation of captions entirely, and just count references
within each nested level of subheading independently, set
:ref:`keywords-system-caption_counter_depth` to :py:obj:`None`:

.. literalinclude:: /demos/Games/GamesNone.ipc
   :language: python
   :name: t_additional_1-references-depth-ipcN
   :caption: :download:`GamesNone.ipc </demos/Games/GamesNone.ipc>`: Overriding
             the :ref:`keywords-system-caption_counter_depth`, unsetting the
             depth entirely.
   :linenos:

The result will be identical with the case where
:ref:`keywords-system-caption_counter_depth` is 2 for this particular example
as well, but in general, the heading portion of the reference will not be
constrained (similar to section headings). The counter will restart for any
heading that is encountered in the document.

There are plenty of other pathalogical cases out there in terms of missing
heading levels. The reader is assured that Imprint handles all of them
consistently, and is left with the exercise of verifying that assertion for
themselves. For a starting point, see the obscure
:download:`PathologicalCases </demos/PathologicalCases.zip>` project.


.. _t_additional_1-references-roles:

Using Roles
===========

:ref:`tag-api-references-roles` allow tags to impersonate each other as
reference targets. The most common usage is to turn tables or equations into
figures that can be referenced as "Figure 1.3-1", rather than being treated as
a table or equation.

Our sample template creates such a :ref:`xml-spec-tags-table` to describe
Tic-Tac-Toe:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-references-roles-xml1
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`, lines
             43-44, emphasizing the :ref:`xml-spec-tags-table` tag.
   :lineno-start: 43
   :lines: 43-44
   :emphasize-lines: 2

The reference for this table can only be performed through a
:ref:`xml-spec-tags-figure-ref` tag, rather than the usual
:ref:`xml-spec-tags-table-ref`:

.. literalinclude:: /demos/Games/templates/Games.xml
   :language: xml
   :name: t_additional_1-references-roles-xml2
   :caption: :download:`Games.xml </demos/Games/templates/Games.xml>`, lines
             13-15, emphasizing the unusual :ref:`xml-spec-tags-figure-ref`
             tag.
   :lineno-start: 13
   :lines: 13-15
   :emphasize-lines: 2

Any tag, whether it is normally referenceable or not, can impersonate a role.
For example, all it takes for a :ref:`xml-spec-tags-latex` equation to become
a figure is the addition of an attribute: ``role="figure"``. That being said,
not all roles are suitable for every tag. For example, the
:download:`PathologicalCases </demos/PathologicalCases.zip>` project has an
example of a :ref:`xml-spec-tags-table` that plays the role of a heading with
``role="par"``. This introduces the problem that :ref:`xml-spec-tags-table`
should not contain text, and so normally can not be referenced by
:ref:`xml-spec-tags-segment-ref`\ 's title attribute.


.. |Figure12 Reference Inline| image:: /_static/Figure12\ Reference\ Inline.png
                               :scale: 75%
.. |Figure34 Reference Inline| image:: /_static/Figure34\ Reference\ Inline.png
                               :scale: 75%
.. |Segment1 Reference Inline| image:: /_static/Segment1\ Reference\ Inline.png
                               :scale: 75%
.. |Figure212 Reference Inline| image:: /_static/Figure212\ Reference\ Inline.png
                               :scale: 75%
.. |Figure234 Reference Inline| image:: /_static/Figure234\ Reference\ Inline.png
                               :scale: 75%
.. |Figure012 Reference Inline| image:: /_static/Figure012\ Reference\ Inline.png
                               :scale: 75%
.. |Figure034 Reference Inline| image:: /_static/Figure034\ Reference\ Inline.png
                               :scale: 75%
