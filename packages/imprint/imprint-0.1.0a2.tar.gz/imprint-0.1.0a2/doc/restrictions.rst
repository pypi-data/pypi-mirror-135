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


.. _restrictions:

============
Restrictions
============

While Imprint is an extremely complex and flexible system, there are in fact
certain things it can not do. The following list contains the major omissions,
with a brief explanation of the underlying reasons for each one:

1. **Updating the TOC:** each newly generated document requires the user to
right-click on the empty table of contents and manually select "Update Table".
This is necessary because calculating the page number of the headers would
require a rendering engine quivalent to MS Word.

2. **Header and Footer Parseability:** in some cases, the XML of the
:ref:`configuration-docx-headers-footers` must be massaged manually to ensure
that there are no spurious run-breaks within a keyword-replacement directive.
Word will sometimes chunk up text into runs when it is not strictly necessary,
resulting in the need for this
:ref:`manual massaging <t_additional_2-headers-footers-xml>`. The root cause is
that the `python-docx`_ library does not currently have support for headers and
footers.


.. include:: /link-defs.rst
