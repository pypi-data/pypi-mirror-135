.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _pt1 element:

PT1-Element
===========

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with the transfer function of a time-discrete PT1-element over a number
of signal :attr:`~Trace.samples` or with a smoothing factor, and a proportional
*gain*.

Sample Based Smoothing
----------------------

You can smooth the signal :attr:`~Trace.samples` with a PT1-element by calling
the method :meth:`~Trace.pt1`, and define the *time constant* :math:`\tau` of
the PT1-element by the number of signal samples.

A new :class:`Trace` instance *labeled* with the performed transformation
``'pt1'`` is returned.

  >>> # smooth the signal samples sample based [.., 1:transparent, ..]
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).pt1(ratio=2, gain=1)
  Trace(label='Signal:pt1',
        samples=[0.0, 0.5, 0.75, 0.875, 0.9375, 0.96875, 0.984375,
                 0.9921875, 0.99609375, 0.998046875, 0.9990234375])
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).pt1(2)
  Trace(label='Signal:pt1',
        samples=[0.0, 0.5, 0.75, 0.875, 0.9375, 0.96875, 0.984375,
                 0.9921875, 0.99609375, 0.998046875, 0.9990234375])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  trace = signal.pt1(2)
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()

Factor Based Smoothing
----------------------

You can smooth the signal :attr:`~Trace.samples` with a PT1-element by calling
the method :meth:`~Trace.pt1`, and define the inverted *time constant*
:math:`\frac{1}{\tau}` of the PT1-element with a smoothing factor between
``0.0`` and ``1.0``.

A new :class:`Trace` instance *labeled* with the performed transformation
``'pt1'`` is returned.

  >>> # smooth the signal samples factor based [0.0:freeze..1.0:transparent]
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).pt1(ratio=0.5, gain=1)
  Trace(label='Signal:pt1',
        samples=[0.0, 0.5, 0.75, 0.875, 0.9375, 0.96875, 0.984375,
                 0.9921875, 0.99609375, 0.998046875, 0.9990234375])
  >>> Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).pt1(0.5)
  Trace(label='Signal:pt1',
        samples=[0.0, 0.5, 0.75, 0.875, 0.9375, 0.96875, 0.984375,
                 0.9921875, 0.99609375, 0.998046875, 0.9990234375])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  trace = signal.pt1(0.5)
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()
