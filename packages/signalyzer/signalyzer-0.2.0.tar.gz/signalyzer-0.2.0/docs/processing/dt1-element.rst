.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _dt1 element:

DT1-Element
===========

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with the transfer function of a time-discrete DT1-element over a number
of signal :attr:`~Trace.samples` or with a damping factor, and a proportional
*gain*.

Sample Based Damping
--------------------

You can differentiate and damp the signal :attr:`~Trace.samples` with a DT1-element
by calling the method :meth:`~Trace.dt1`, and define the *time constant*
:math:`\tau` of the DT1-element by the number of signal samples.

A new :class:`Trace` instance *labeled* with the performed transformation
``'dt1'`` is returned.

  >>> # differentiate and damp the signal samples sample based [.., 1:impulse, ..]
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).dt1(ratio=2, gain=1)
  Trace(label='Signal:dt1',
        samples=[0.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125,
                 0.015625, 0.0078125, 0.00390625, 0.001953125])
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).dt1(2)
  Trace(label='Signal:dt1',
        samples=[0.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125,
                 0.015625, 0.0078125, 0.00390625, 0.001953125])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  trace = signal.dt1(2)
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()

Factor Based Damping
--------------------

You can differentiate and damp the signal :attr:`~Trace.samples` with a
DT1-element by calling the method :meth:`~Trace.dt1`, and define the inverted
*time constant* :math:`\frac{1}{\tau}` of the DT1-element with a damping factor
between ``0.0`` and ``1.0``.

A new :class:`Trace` instance *labeled* with the performed transformation
``'dt1'`` is returned.

  >>> # differentiate and damp signal samples factor based [0.0:transparent..1.0:impulse]
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).dt1(ratio=0.5, gain=1)
  Trace(label='Signal:dt1',
        samples=[0.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125,
                 0.015625, 0.0078125, 0.00390625, 0.001953125])
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).dt1(0.5)
  Trace(label='Signal:dt1',
        samples=[0.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125,
                 0.015625, 0.0078125, 0.00390625, 0.001953125])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  trace = signal.dt1(0.5)
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()
