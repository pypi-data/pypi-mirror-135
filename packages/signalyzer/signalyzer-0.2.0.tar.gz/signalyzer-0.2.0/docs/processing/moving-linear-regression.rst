.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _moving linear regression:

Moving Linear Regression
========================

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with a `moving linear regression`_ over a number of signal
:attr:`~Trace.samples`, whereby each window of the signal :attr:`~Trace.samples`
is statistically analyzed, and a :ref:`linear regression trace
<linear regression trace>` collection is returned.

Create the Trace Collection
---------------------------

You can process the signal :attr:`~Trace.samples` with a statistically analyzed
`moving linear regression`_ by calling the method
:meth:`~Trace.moving_regression`.

An :ref:`linear regression trace <linear regression trace>` collection is
returned.

  >>> # moving linear regression over a number of samples
  >>> traces = Trace('Signal', [1, 2, 3]).moving_regression(2)
  >>> traces
  LinearRegressionTraces(level=Trace(label='Signal:regression:level',
                                     samples=[1.0, 2.0, 3.0]),
    slope=Trace(label='Signal:regression:slope',
                samples=[0.0, 1.0, 1.0]),
    intercept=Trace(label='Signal:regression:intercept',
                    samples=[1.0, 1.0, 2.0]),
    mean=Trace(label='Signal:regression:mean',
                 samples=[1, 1.5, 2.5]),
    median=Trace(label='Signal:regression:median',
                   samples=[1.0, 1.5, 2.5]),
    minimum=Trace(label='Signal:regression:minimum',
                  samples=[1, 1, 2]),
    maximum=Trace(label='Signal:regression:maximum',
                  samples=[1, 2, 3]),
    range=Trace(label='Signal:regression:range',
                samples=[0, 1, 1]),
    error=Trace(label='Signal:regression:error',
                samples=[0.0, 0.0, 0.0]),
    negative_error=Trace(label='Signal:regression:negative_error',
                         samples=[0.0, 0.0, 0.0]),
    positive_error=Trace(label='Signal:regression:positive_error',
                         samples=[0.0, 0.0, 0.0]),
    absolute_error=Trace(label='Signal:regression:absolute_error',
                         samples=[0.0, 0.0, 0.0]),
    variance=Trace(label='Signal:regression:variance',
                   samples=[0.0, 0.0, 0.0]),
    deviation=Trace(label='Signal:regression:deviation',
                    samples=[0.0, 0.0, 0.0]),
    skew=Trace(label='Signal:regression:skew',
               samples=[0.0, 0.0, 0.0]),
    kurtosis=Trace(label='Signal:regression:kurtosis',
                   samples=[0.0, 0.0, 0.0]))

.. note::

  The `moving linear regression`_ uses the first signal sample as the *preset*
  value to generate the :ref:`windows <moving window>` for the first *number*
  of signal :class:`~Trace.samples`.

Figure
------

You can visualize the trace collection with a figure containing the subplots of
the traces in the collection by calling the method
:meth:`~LinearRegressionTraces.figure`.

  >>> figure = Trace('Signal', [1, 2, 3]).moving_regression(2).figure()

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', range(20))
  traces = signal.moving_regression(5)
  fig = traces.figure(original=signal)

  fig.show()
