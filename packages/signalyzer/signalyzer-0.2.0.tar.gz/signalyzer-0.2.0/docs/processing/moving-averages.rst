.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _moving average:

Moving Averages
===============

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with a simple `moving average`_ over a number of signal
:attr:`~Trace.samples`, whereby each window of the signal :attr:`~Trace.samples`
is statistically analyzed, and a :class:`MovingAverageTraces` collection in form
of the :ref:`statistics trace <statistics trace>` collection is returned.

Create the Trace Collection
---------------------------

You can process the signal :attr:`~Trace.samples` with a statistically analyzed
`moving average`_ by calling the method :meth:`~Trace.moving_average`.

An :ref:`statistics trace <statistics trace>` collection is returned.

  >>> # simple moving average over a number of samples
  >>> traces = Trace('Signal', [1, 2, 3]).moving_average(2)
  >>> traces
  MovingAverageTraces(mean=Trace(label='Signal:average:mean',
                                 samples=[1, 1.5, 2.5]),
    weighted_mean=Trace(label='Signal:average:weighted_mean',
           samples=[1.0, 1.6666666666666665, 2.6666666666666665]),
    median=Trace(label='Signal:average:median',
           samples=[1.0, 1.5, 2.5]),
    mode=Trace(label='Signal:average:mode',
               samples=[1, 1, 2]),
    rms=Trace(label='Signal:average:rms',
              samples=[1.0, 1.5811388300841898, 2.5495097567963922]),
    minimum=Trace(label='Signal:average:minimum',
                  samples=[1, 1, 2]),
    maximum=Trace(label='Signal:average:maximum',
                  samples=[1, 2, 3]),
    range=Trace(label='Signal:average:range',
                samples=[0, 1, 1]),
    midrange=Trace(label='Signal:average:midrange',
                   samples=[1.0, 1.5, 2.5]),
    absolute_error=Trace(label='Signal:average:absolute_error',
                         samples=[0, 1.0, 1.0]),
    variance=Trace(label='Signal:average:variance',
                   samples=[0.0, 0.25, 0.25]),
    deviation=Trace(label='Signal:average:deviation',
                    samples=[0.0, 0.5, 0.5]),
    coefficient=Trace(label='Signal:average:coefficient',
                      samples=[0.0, 0.3333333333333333, 0.2]),
    skew=Trace(label='Signal:average:skew',
               samples=[0.0, 0.0, 0.0]),
    kurtosis=Trace(label='Signal:average:kurtosis',
                   samples=[0.0, 1.0, 1.0]))

.. note::

  The `moving average`_ uses the first signal sample as the *preset* value
  to generate the :ref:`windows <moving window>` for the first *number* of
  signal :class:`~Trace.samples`.

Figure
------

You can visualize the trace collection with a figure containing the subplots of
the traces in the collection by calling the method
:meth:`~MovingAverageTraces.figure`.

  >>> figure = Trace('Signal', [1, 2, 3]).moving_average(2).figure()

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', range(10))
  traces = signal.moving_average(3)
  fig = traces.figure(original=signal)

  fig.show()
