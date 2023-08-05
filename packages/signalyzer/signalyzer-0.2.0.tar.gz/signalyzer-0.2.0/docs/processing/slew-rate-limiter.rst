.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _slew-rate limiter:

Slew-Rate Limiter
=================

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with a `slew-rate limiter`_.

Create the Trace Collection
---------------------------

You can limit the slew-rates of the signal :attr:`~Trace.samples` with a
`slew-rate limiter`_ by calling the method :meth:`~Trace.slew`.

An :ref:`slew-rate limiter trace <slew-rate limiter trace>` collection is
returned.

  >>> # slew-rate limited signal samples
  >>> traces = Trace('Signal', [0, 1, 1, -1, -1]).slew(limits=(0.5, -0.5), hold=1)
  >>> traces
  SlewRateLimiterTraces(level=Trace(label='Signal:slew:level',
                                    samples=[0, 0, 0.5, 0.0, -0.5]),
    deviation=Trace(label='Signal:slew:deviation',
                    samples=[0, 1, 0.5, -1.0, -0.5]),
    active=Trace(label='Signal:slew:active',
                  samples=[0, 1, 1, 1, 1]))

.. note::

  The `slew-rate limiter`_ uses the first signal sample as the *preset* value
  of the `slew-rate limiter`_.

Figure
------

You can visualize the trace collection with a figure containing the subplots of
the traces in the collection by calling the method
:meth:`~SlewRateLimiterTraces.figure`.

  >>> figure = Trace('Signal', [0, 1, 1, -1, -1]).slew(
  ...   limits=(0.5, -0.5), hold=1).figure()

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, -1, -1])
  traces = signal.slew(limits=(0.5, -0.5), hold=1)
  fig = traces.figure(original=signal)

  fig.show()
