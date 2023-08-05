.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _traces:

Trace Collections
=================

The ``signalyzer`` package provides a :class:`Traces` class in order to collect
the result traces of one or more processed signal traces.

A collection of :class:`Traces` is a data class with mutable mapping support to
iterate over the traces within the collection or to select a :class:`Trace`
within the collection by its name.

.. note::

  The :class:`Traces` class is base class for trace collections and is not
  intended to be used directly.

You can import the :class:`Traces` class from the ``signalyzer`` package.

  >>> from signalyzer import Traces

.. toctree::
   :maxdepth: 3
   :caption: Trace Collections
   :hidden:

   vector-traces
   statistics-traces
   slew-rate-limiter-traces
   exponential-smoothing-traces
   linear-regression-traces

Create a Collection of Traces
-----------------------------

You can create an empty collection of :class:`Traces` by calling the
:class:`Traces` class.

  >>> # create an empty collection
  >>> Traces()
  Traces()

Number of Traces
----------------

You can get the number of the traces in the collection of :class:`Traces` with
the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(Traces())
  0

Names of the Traces in the Collection
-------------------------------------

You can get the :class:`list` with the names of the traces in the collection of
:class:`Traces`.

A :class:`list` with the key names of the traces is returned.

  >>> # list of the key names of the traces in the collection
  >>> list(Traces())
  []

You can get an iterator over the names of the traces in the collection of
:class:`Traces`.

  >>> # name iterator of the traces
  >>> Traces().keys()
  KeysView(Traces())

Traces in the Collection
------------------------

You can get the :class:`list` with the traces in the collection of
:class:`Traces`.

A :class:`list` with the traces is returned.

  >>> # list of the traces in the collection
  >>> list(Traces().values())
  []

You can get an iterator over the traces in the collection of :class:`Traces`.

  >>> # trace iterator of the collection
  >>> Traces().values()
  ValuesView(Traces())

Items in the Collection
------------------------

You can get the :class:`list` with the trace items in the collection of
:class:`Traces`.

A :class:`list` with the name, trace items is returned.

  >>> # list of the items in the collection
  >>> list(Traces().items())
  []

You can get an iterator over the items in the collection of :class:`Traces`.

  >>> # item iterator of the collection
  >>> Traces().items()
  ItemsView(Traces())


Labels of the Traces in the Collection
--------------------------------------

You can get the list with the labels of the traces in the collection of
:class:`Traces` by calling the method :meth:`~Traces.labels`.

A list with the labels of the traces is returned.

  >>> # list of the labels of the traces in the collection
  >>> Traces().labels()
  ()

Convert Traces to Dictionary
----------------------------

Your can convert a collection of :class:`Traces` into a :class:`dict` class by
calling the method :meth:`~Traces.as_dict`.

  >>> Traces().as_dict()
  {}

Your can convert a collection of :class:`Traces` into a :class:`dict` class with
the function :func:`~dataclasses.asdict` from the :mod:`dataclasses` module.

  >>> from dataclasses import asdict
  >>> asdict(Traces())
  {}

Convert Traces to Tuple
-----------------------

Your can convert a collection of :class:`Traces` into a :class:`tuple` class by
calling the method :meth:`~Traces.as_tuple`.

  >>> Traces().as_tuple()
  ()

Your can convert a collection of :class:`Traces` into a :class:`tuple` class with
the function :func:`~dataclasses.astuple` from the :mod:`dataclasses` module.

  >>> from dataclasses import astuple
  >>> astuple(Traces())
  ()
