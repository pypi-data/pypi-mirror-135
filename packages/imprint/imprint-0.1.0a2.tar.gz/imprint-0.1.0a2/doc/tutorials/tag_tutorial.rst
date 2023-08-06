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


.. _t_tag:

===================
Writing Custom Tags
===================


.. _t_tag-toc:

.. contents:: Topics Covered:
   :depth: 2
   :local:


.. _t_tag-descriptor:

------------------------------------------------------
Writing a :py:class:`~imprint.core.tags.TagDescriptor`
------------------------------------------------------

.. todo::

   Add the following:

   > This tutorial covers the creation of a basic XML tag. It does not delve
   > into the subject of tags with :ref:`plugins <t_plugin>`. This advanced
   > topic is covered in the :doc:`content_tutorial`.


.. _t_tag-register:

--------------------------
Registering the Descriptor
--------------------------


.. _t_tag-usage:

-----------------------
Putting it all Together
-----------------------


.. _t_tag-dev:

------------------------
Making Your Tag Built-In
------------------------

If you end up writing a tag that you believe is generic and useful enough to be
built-in, feel free to submit a `pull request`_ or patch to the author. Be sure
to include all, or at least most, of the following items:

  - A properly documented implementation of your tag in the
    :py:mod:`imprint.core.tags` module.
  - A proper entry in :doc:`/reference/xml_spec`.
  - At least a brief mention of your tag in at least one of the tutorials.
  - Proper tests, once that becomes a thing.


.. include:: /link-defs.rst
