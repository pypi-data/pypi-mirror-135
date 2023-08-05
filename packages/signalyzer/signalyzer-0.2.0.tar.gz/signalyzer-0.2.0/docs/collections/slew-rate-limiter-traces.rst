.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _slew-rate limiter trace:

Slew-Rate Limiter Traces
========================

The `slew-rate limiter trace`_ collection is used to store the resulting
:ref:`signal traces <signal trace>` produced by the :ref:`slew-rate limiter
<slew-rate limiter>` of the signal :attr:`~Trace.samples` of a
:ref:`signal trace <signal trace>`.

Create the Trace Collection
---------------------------

You can create an `slew-rate limiter trace`_ collection without
:attr:`~Trace.samples` by calling the :class:`SlewRateLimiterTraces` class.

  >>> # create an empty slew-rate limiter trace collection
  >>> traces = SlewRateLimiterTraces()
  >>> traces
  SlewRateLimiterTraces(level=Trace(label='Trace', samples=[]),
                        deviation=Trace(label='Trace', samples=[]),
                        active=Trace(label='Trace', samples=[]))

Number of Traces
----------------

You can get the number of the traces in the :class:`SlewRateLimiterTraces`
collection with the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(traces)
  3

Names of the Traces
-------------------

You can get the :class:`list` with the names of the traces in the
:class:`SlewRateLimiterTraces` collection.

A :class:`list` with the key names of the traces is returned.

  >>> # key names of the traces in the collection
  >>> list(traces)
  ['level',
   'deviation',
   'active']

  >>> # key names of the traces in the collection
  >>> list(traces.keys())
  ['level',
   'deviation',
   'active']

Level Trace
-----------

You can get the *level* :class:`Trace` with the
:attr:`~SlewRateLimiterTraces.level` attribute from the
:class:`SlewRateLimiterTraces` collection.

The :class:`Trace` with the *level* :attr:`~Trace.samples` is returned.

  >>> # level trace by attribute
  >>> traces.level
  Trace(label='Trace', samples=[])
  >>> # level trace by key
  >>> traces['level']
  Trace(label='Trace', samples=[])

Deviation Trace
---------------

You can get the *deviation* :class:`Trace` with the
:attr:`~SlewRateLimiterTraces.deviation` attribute from the
:class:`SlewRateLimiterTraces` collection.

The :class:`Trace` with the *deviation* :attr:`~Trace.samples` is returned.

  >>> # deviation trace by attribute
  >>> traces.deviation
  Trace(label='Trace', samples=[])
  >>> # deviation trace by key
  >>> traces['deviation']
  Trace(label='Trace', samples=[])

Active Trace
------------

You can get the *active* :class:`Trace` with the
:attr:`~SlewRateLimiterTraces.active` attribute from the
:class:`SlewRateLimiterTraces` collection.

The :class:`Trace` with the *active* :attr:`~Trace.samples` is returned.

  >>> # active trace by attribute
  >>> traces.active
  Trace(label='Trace', samples=[])
  >>> # active trace by key
  >>> traces['active']
  Trace(label='Trace', samples=[])
