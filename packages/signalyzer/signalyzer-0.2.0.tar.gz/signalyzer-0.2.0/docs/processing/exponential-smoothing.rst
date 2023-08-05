.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _second-order exponential smoothing:

Second-Order Exponential Smoothing
==================================

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with a `second-order exponential smoothing`_ algorithm.

Create the Trace Collection
---------------------------

You can smooth the signal :attr:`~Trace.samples` with a `second-order exponential
smoothing`_ algorithm by calling the method :meth:`~Trace.exponential`.

An :ref:`exponential smoothing trace <exponential smoothing trace>` collection
is returned.

  >>> # smooth the signal samples [0.0:freeze..1.0:transparent]
  >>> traces = Trace('Signal', [1, 2, 3]).exponential(0.3)
  >>> traces
  ExponentialSmoothingTraces(forecast=Trace(label='Signal:exponential:forecast',
                                      samples=[1.0, 1.5999999999999999, 2.53]),
    forecast_sign=Trace(label='Signal:exponential:forecast_sign',
                        samples=[1.0, 1.0, 1.0]),
    level=Trace(label='Signal:exponential:level',
                samples=[1.0, 1.5099999999999998, 2.3139999999999996]),
    level_sign=Trace(label='Signal:exponential:level_sign',
                     samples=[1.0, 1.0, 1.0]),
    prognosis1=Trace(label='Signal:exponential:prognosis1',
                     samples=[1.0, 1.0, 1.2999999999999998]),
    prognosis2=Trace(label='Signal:exponential:prognosis2',
                     samples=[1.0, 1.0, 1.0899999999999999]),
    prognosis=Trace(label='Signal:exponential:prognosis',
                    samples=[1.0, 1.0, 1.5099999999999998]),
    smoothed1=Trace(label='Signal:exponential:smoothed1',
                    samples=[1.0, 1.2999999999999998, 1.8099999999999996]),
    smoothed2=Trace(label='Signal:exponential:smoothed2',
                    samples=[1.0, 1.0899999999999999, 1.3059999999999996]),
    trend=Trace(label='Signal:exponential:trend',
                samples=[0.0, 0.09, 0.21600000000000003]),
    trend_sign=Trace(label='Signal:exponential:trend_sign',
                     samples=[0.0, 1.0, 1.0]),
    trend_inflection=Trace(label='Signal:exponential:trend_inflection',
                           samples=[0.0, 1.0, 1.0]),
    error=Trace(label='Signal:exponential:error',
                samples=[0.0, 1.0, 1.4000000000000001]),
    correction=Trace(label='Signal:exponential:correction',
                     samples=[0.0, 0.3, 0.42000000000000004]),
    absolute_error=Trace(label='Signal:exponential:absolute_error',
                         samples=[0.0, 0.21, 0.294]),
    variance=Trace(label='Signal:exponential:variance',
                   samples=[0.0, 0.21, 0.5586]),
    deviation=Trace(label='Signal:exponential:deviation',
                    samples=[0.0, 0.458257569495584, 0.7473954776421918]),
    skew=Trace(label='Signal:exponential:skew',
                   samples=[0.0, 2.182178902359923, 2.9077569539828634]),
    kurtosis=Trace(label='Signal:exponential:kurtosis',
                   samples=[0.0, 4.76190476190476, 5.918744228993535]))

.. note::

  The `second-order exponential smoothing`_ algorithm uses for the first
  *prognosis* the first signal sample as the initial *level*, and the initial
  *trend* is set by default to zero.

Figure
------

You can visualize the trace collection with a figure containing the subplots of
the traces in the collection by calling the method
:meth:`~ExponentialSmoothingTraces.figure`.

  >>> figure = Trace('Signal', [1, 2, 3]).exponential(2).figure()

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', range(20))
  traces = signal.exponential(0.3)
  fig = traces.figure(original=signal)

  fig.show()
