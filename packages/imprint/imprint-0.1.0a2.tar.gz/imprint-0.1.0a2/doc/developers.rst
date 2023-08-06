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
.. along with this program. If not, see <https://www.gnu.org/licenses/>.

.. Author: Joseph Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>
.. Version: 13 Apr 2019: Initial Coding


.. _development:

===========
Development
===========

You can contribute to imprint by providing but reports (or just usage
experience), or writing code. Issues can be submitted on GitHub at
https://github.com/madphysicist/imprint/issues. To contribute code, fork and
clone the repository from  https://github.com/madphysicist/imprint. You can
modify the code as you wish, and submit a `pull request`_ through GitHub.



.. _development-branches:

----------------
Branch Structure
----------------

Feature branches should be branched from ``dev``. Accepted features should be
squashed into a small number of commits. When a sufficient number of commits are
made, they will be added to master, the minor version will increment, and a
release candidate branch will start.


.. _development-install:

------------
Installation
------------

Installing the project is not strictly necessary for development. That being
said, some features may be better tested when the project is installed.
Developers can install their local copy for testing by running the following in
the project root::

    python setup.py develop

This will symlink the development project to the site packages of the current
python environment. It is recommended that this command be run in a dedicated
virtual environment.


.. _development-coding:

------
Coding
------

Feel free to suggest and/or implement any feature that you feel is useful. The
general phiposophy is to keep things modular. General purpose functions should
be added to the `haggis`_ library rather than to Imprint itself.

The documentation should explain how the project works. :ref:`introduction`
provides a high-level explanation of the overall structure. The
:ref:`reference` secion contains all the references to the individual
components.


.. _development-testing:

-------
Testing
-------

At the moment, there is no test package for Imprint. Instead, the
:ref:`tutorials-demos` in the documentation provide good coverage of almost all
available features. If you add a feature that is not already covered, please add
a section to the appropriate :ref:`tutorials` page, and modify the corresponding
demo (or add a new one) as necessary.

If you would like to contribute a test package to Imprint, that would be
wonderful.


.. include:: /link-defs.rst
