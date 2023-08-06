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


.. _internals:

============
Internal API
============

The internals of Imprint are implemented in the :mod:`imprint.core` package.
Some of the internals are exposed to the user through the :ref:`tag-api` in
:mod:`imprint.core.tags` and :mod:`imprint.core.state`. The remainder is not
normally of interest to the user. However, it may be useful for developers and
authors of more complex plugins to have access to the internals of the engine.


.. _internals-toc:

.. contents:: Contents
   :depth: 2
   :local:


.. _internals-parsers:

-------
Parsers
-------

.. automodule:: imprint.core.parsers

.. autoclass:: DocxParserBase

.. autoclass:: ReferenceProcessor

.. autoclass:: TemplateProcessor


.. _internals-parsers-tags:

Tag Handling
------------

.. autoclass:: RootTag

.. autoclass:: TagStack

.. autoclass:: TagStackNode

.. autoexception:: OpenTagError


.. _internals-utilities:

---------
Utilities
---------

.. automodule:: imprint.core.utilities
   :members:
