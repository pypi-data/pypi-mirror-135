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


:orphan:

.. _todos:

=========
ToDo List
=========

List of minor fixups/features:


  .. _todos-optional-stub:

- Make the :ref:`configuration-docx` stub optional. There is no reason to have
  it if the user is OK with using the default styles provided by the
  python-docx template. It means that the lowest level default hard-coded
  styles used by Imprint should match what is in that document.


  .. _todos-normalize-config:

- Add a step to normalize the configuration when it is loaded: add missing
  logging keys from the defaults. Add the max caption depth, etc. Defaults
  should not be implemented through function parameters (e.g., the defaults for
  :py:func:`haggis.logs.configure_logger`). Tag descriptors should not be
  forced to call `state.keywords.get` to determine if images should be dumped,
  for example.


  .. _todos-add-location:

- For all exceptions that are raised through the engine, add location
  information before re-raising.


  .. _todos-data-keywords:

- Make keywords available in the data configuration. `haggis`_ already supports
  such injection on load.


.. _todos-internal:

==============
Internal ToDos
==============

.. todolist::


.. include:: /link-defs.rst
