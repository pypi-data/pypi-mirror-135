.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _moving differentiation:

Moving Differentiation
======================

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
differentiated over a number of signal :attr:`~Trace.samples`.

Sample Based
------------

You can differentiate each signal *sample* over a number of signal samples by
calling the method :meth:`~Trace.moving_differential`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'differential'`` is returned.

  >>> # differentiate the signal samples over the moving window
  >>> Trace('Signal', [1, 2, 3]).moving_differential(2)
  Trace(label='Signal:differential',
        samples=[0.0, 1.0, 1.0])

Sampling Time Based
-------------------

You can differentiate sampling time based each signal *sample* by dividing the
trace generated with the :meth:`~Trace.moving_differential` method by the
sampling time of the signal :class:`~Trace.samples`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'differential'`` is returned.

  >>> # equidistant sampling time of the signal samples
  >>> dt = 0.5
  >>> # differentiate sampling time based the signal samples
  >>> Trace('Signal', [1, 2, 3]).moving_differential(2) / dt
  Trace(label='Signal:differential:div',
        samples=[0.0, 2.0, 2.0])

Sampling Time Based with Unit Adaption
--------------------------------------

You can differentiate sampling time based each signal *sample* with unit adaption
by dividing the trace generated with the :meth:`~Trace.moving_differential`
method by the sampling time of the signal :class:`~Trace.samples`, and applying
a scaling factor to adapt the unit of the signal :class:`~Trace.samples`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'differential'`` is returned.

  >>> # equidistant sampling time of the signal samples
  >>> dt = 0.1
  >>> # differentiate sampling time based the signal samples with unit adaption
  >>> Trace('Signal', [1, 2, 3]).moving_differential(2) / (dt * 3.6)
  Trace(label='Signal:differential:div',
        samples=[0.0, 2.7777777777777772, 2.7777777777777772])
