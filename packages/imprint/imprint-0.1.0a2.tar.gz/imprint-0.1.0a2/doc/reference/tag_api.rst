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


.. py:currentmodule:: imprint.core.tags

.. _tag-api:

===========
XML Tag API
===========

The Imprint :ref:`engine <introduction-layers-engine>` comes with a complete set
of processors for the tags specified in the :doc:`xml_spec`. However, additional
tags may be necessary for highly customized applications, so an API exists for
defining and registering new tags. The API is defined in the
:py:mod:`imprint.core.tags` module. Example usage can be found in the
:ref:`t_tag` tutorial.


.. _tag-api-toc:

.. contents:: Contents
   :depth: 2
   :local:


.. _tag-api-descriptors:

---------------
Tag Descriptors
---------------

The tag API revolves around the :py:class:`TagDescriptor` class. The class can
be extended directly, or instantiated through a delegate object that fulfills
the necessary duck-type API. Objects contain a set of attributes and two
callbacks that define how to handle XML tags of a given type. All the elements
are optional and have sensible default values.

Any registered object will be viewed through :py:meth:`TagDescriptor.wrap`, so
it is not necessary to extend or instantiate :py:class:`TagDescriptor` to
create a working tag descriptor.


.. _tag-api-descriptor-errors:

Errors
======

Tag descriptors may raise any type of error they deem necessary in their
:py:meth:`~TagDescriptor.start` and :py:meth:`~TagDescriptor.end` methods. Most
classes of errors will be logged and cause the application to abort. However,
two special classes of errors will not cause a fatal crash:

1. :py:exc:`~imprint.core.KnownError` is used to flag known conditions that can
   be handled gracefully by the tag.
2. :py:exc:`OSError`. Specifically, the :py:exc:`FileNotFoundError` and
   :py:exc:`PermissionError` subclasses are deemed to be "known errors". If
   they represent a fatal condition, they should be wrapped in another
   exception type.

Any plugins with a dynamic :ref:`tag-api-configuration-data` will generally
receive an alt-text placeholder where the content would normally go instead of
completely aborting.

.. autoexception:: imprint.core.KnownError
   :members:


.. _tag-api-configuration:

-------------
Configuration
-------------

Tags have two types of configuration available to them. Static configuration
for a given :ref:`configuration-xml` is provided through the tag attributes in
the XML file. Dynamic configuration through the :ref:`configuration-idc` can be
enabled to provide per-document fine-tuning.


.. _tag-api-configurtion-attributes:

XML Attributes
==============

XML attributes are supplied to the :py:meth:`~TagDescriptor.start` and
:py:meth:`~TagDescriptor.end` methods of a :py:class:`TagDescriptor` as the
second argument. The inputs are presented to both methods as a vanilla
:py:class:`dict`. The dictionary are meant to be treated as read-only, but this
is not a requirement, meaning that technically :py:meth:`~TagDescriptor.start`
can modify what :py:meth:`~TagDescriptor.end` sees. The dictionary is filtered
to exclude any attributes that are not listed in the
:py:attr:`~TagDescriptor.required` and :py:attr:`~TagDescriptor.optional`
elements of the :py:class:`TagDescriptor`.


.. _tag-api-configuration-data:

Data Configuration
==================

For some types of content, static configuration is not enough. To allow
per-document configurations, a :py:class:`TagDescriptor` must define a
non-\ :py:obj:`None` :py:attr:`~TagDescriptor.data_config` attribute. This
attribute gives the name of the dictionary to extract from the
:ref:`configuration-idc`.

:py:meth:`~TagDescriptor.start` and :py:meth:`~TagDescriptor.end` methods of a
:py:class:`TagDescriptor` with the :py:attr:`~TagDescriptor.data_config`
attribute set will receive an additional input argument containing the
:ref:`plugins-data-configuration` loaded from the :ref:`configuration-idc`.

The data configuration can override some of the static
:ref:`tag-api-configurtion-attributes` of a tag. For built-in tags, the
:doc:`xml_spec` notes which attributes can be overriden. Built-in tags that
support dynamic configuration are :ref:`xml-spec-tags-figure`,
:ref:`xml-spec-tags-table` and :ref:`xml-spec-tags-string`.

All built-in tags that support dynamic configuration also support a type of
:doc:`plugin <plugin_api>`, but this is not a requirement for custom tags.


.. _tag-api-references:

----------
References
----------

A :py:class:`TagDescriptor` is :term:`referenceable` if it has a
non-\ :py:obj:`None` :py:attr:`~TagDescriptor.reference`. A reference made to a
tag will be substituted by the appropriate reference text. By default reference
tags have the target tag name with "-ref" appended:
:ref:`xml-spec-tags-figure-ref` references :ref:`xml-spec-tags-figure`,
:ref:`xml-spec-tags-table-ref` references :ref:`xml-spec-tags-table`. A notable
exception is :ref:`xml-spec-tags-segment-ref`, which references paragraphs
(:ref:`xml-spec-tags-par` tags), but only ones that have a heading style.

References are usually identified by a required ``id`` attribute. Segments can
also be identified by the title of the segment, which is the aggressively
trimmed collection of all the text in the text in the paragraph. For example,
the title of the following XML snippet would be ``'Example Heading'``::

    <par style="Heading 3">
        <run style="Default Paragraph Font">
            Example
            Heading
        </run>
    </par>

:ref:`xml-spec-tags-segment-ref` tags can therefore identify their target with
either a ``id`` or ``title`` attribute. User-defined tags can implement their
own customized rules for identiying targets.


.. _tag-api-references-roles:

Roles
=====

For the purpose of creating references, any tag may impersonate, or play the
role of, any other tag using a special :ref:`xml-spec-attributes-role`
attribute. This attribute is implicitly optional for every tag. It is
interpreted directly by the parsers in the :ref:`introduction-layers-engine` to
determine the type of reference that a tag will represent.

For example, a :ref:`xml-spec-tags-table` tag (or any other tag for that
matter), which has ``role="figure"`` must be referenced by a
:ref:`xml-spec-tags-figure-ref` tag, not a :ref:`xml-spec-tags-table-ref` tag,
in the :ref:`configuration-xml`. That table will be a figure for the purposes
of the document in question.

Any arbitrary tag can be referenced the same way with the appropriate
:ref:`xml-spec-attributes-role`. Usually, such a referenceable tag will be
styled appropriately, and will have the headings, captions, etc. appropriate
for its role rather than its nominal tag.

A specific case is arbitrary tags that have a :ref:`xml-spec-tags-par` role.
Such tags are automatically referenceable by :ref:`xml-spec-tags-segment-ref`.
Their entire contents will be treated as the title of the heading, so the
``par`` role must be used carefully.


.. _tag-api-register:

--------------------
Registering New Tags
--------------------

Once a :py:class:`TagDescriptor` or a delegate object has been constructed,
there are two main ways to get Imprint to use the descriptor for actual tag
processing.


.. _tag-api-register-config:

Via Configuration
=================

In the normal course of things, Imprint will not automatically import
unspecified user-defined modules. To let it know where to find tag extensions,
add them by name or by reference to the :ref:`configuration-ipc` to the mapping
in the :ref:`keywords-system-tags` keyword. This will automatically import all
the necessary modules, and register the custom descriptor under the requested
tag name.


.. _tag-api-register-prog:

Programatically
===============

Under the hood, tags are registered with the Imprint core simply by adding them
to :py:data:`tag_registry`::

    tag_registry[name] = descriptor

The registry is a special mapping that ensures that ``name`` is a string not
representing an existing tag. While it is not possible to remove or overwrite
existing tags, the same descriptor can be registered under multiple names.

This method is useful mostly to users wishing to write a custom driver program
for the engine. Under normal circumstances, the
:ref:`configuration solution <tag-api-register-config>` will be more suitable.


.. _tag-api-engine-state:
    
------------
Engine State
------------

Both callbacks of a :py:class:`TagDescriptor` accept an
:py:class:`~imprint.core.state.EngineState` object as their first argument,
which supports stateful tag processing. The engine state provides a mutable
container for arbitrary attributes. Each :py:class:`TagDescriptor` can add,
remove and modify attributes of the state object to communicate with itself,
the engine, and other tags.

As a rule, objects should prefer to delete state attributes rather than setting
them to :py:obj:`None`. This meshes well with the fact that
:py:class:`~imprint.core.state.EngineState` provides a containment check. For
example, to check if the parser is in the middle of a run of text, descriptors
should check ::

    if 'run' in state: ...

The built-in tags and the engine use a set of attributes and methods to operate
properly. Modifying these predefined attributes in a way other than explicitly
documented will almost inevitably lead to unexpected behavior. Properties are
used instead of simple attributes in a few cases to provide sanity checks for
the supported modifications. Custom tags can add, remove and modify any
additional attributes they choose. The full list of built-in attributes is
available in the :py:class:`~imprint.core.state.EngineState` documentation.


.. _tag-api-logging:

-------
Logging
-------

See :ref:`logging-tags`.


.. _tag-api-api:

-------
The API
-------

.. automodule:: imprint.core

.. automodule:: imprint.core.tags

The following members are used to construct and register new tags:

.. autodata:: tag_registry
   :annotation:  = {}

.. autoclass:: TagDescriptor
   :members:
   :special-members:
   :exclude-members: __weakref__

.. autoclass:: BuiltinTag
   :members:
   :special-members:
   :exclude-members: __weakref__,
   :show-inheritance:

.. _tag-api-builtins:

------------------------
Built-in Tag Descriptors
------------------------

The existing tag descriptors implement the :doc:`xml_spec`:

.. autoclass:: BreakTag
   :members:
   :show-inheritance:

.. autoclass:: ExprTag
   :members:
   :show-inheritance:

.. autoclass:: FigureTag
   :members:
   :show-inheritance:

.. autoclass:: KwdTag
   :members:
   :show-inheritance:

.. autoclass:: LatexTag
   :members:
   :show-inheritance:

.. autoclass:: NTag
   :members:
   :show-inheritance:

.. autoclass:: ParTag
   :members:
   :show-inheritance:

.. autoclass:: RunTag
   :members:
   :show-inheritance:

.. autoclass:: SectionTag
   :members:
   :show-inheritance:

.. autoclass:: SkipTag
   :members:
   :show-inheritance:

.. autoclass:: StringTag
   :members:
   :show-inheritance:

.. autoclass:: TableTag
   :members:
   :show-inheritance:

.. autoclass:: TocTag
   :members:
   :show-inheritance:

.. autoclass:: ReferenceProcessor
   :members:
   :show-inheritance:

.. autoclass:: SegmentRefProcessor
   :members:
   :show-inheritance:


.. _tag-api-refs:

---------------------
Reference Descriptors
---------------------

.. autoclass:: ReferenceDescriptor
   :members:
   :special-members:
   :exclude-members: __weakref__, __init__, prefix

.. autoclass:: SegmentReferenceDescriptor
   :members:
   :inherited-members:
   :exclude-members: __weakref__, __init__, prefix
   :show-inheritance:


.. _tag-api-utilities:

-----------------
Utility Functions
-----------------

.. autofunction:: get_key

.. autofunction:: get_size

.. autofunction:: get_handler

.. autofunction:: get_and_run_handler

.. autofunction:: compute_styles

.. autofunction:: compute_size


.. _tag-api-parser-state:

--------------------
Parser State Objects
--------------------

.. automodule:: imprint.core.state

.. Exclude the attributes implmented as properties

.. autoclass:: EngineState
   :members:
   :special-members: __contains__
   :inherited-members:
   :exclude-members: content, content_stack, doc, keywords, last_list_item,
       references

.. autoclass:: ReferenceState
   :members:
   :special-members: __contains__
   :inherited-members:
   :exclude-members: references

.. autoclass:: ReferenceMap
   :members:
   :special-members:
   :exclude-members: __weakref__, _mapping, _locked

.. autoclass:: ListType
   :members:
