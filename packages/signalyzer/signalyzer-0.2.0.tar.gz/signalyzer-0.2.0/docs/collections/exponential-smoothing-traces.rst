.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _exponential smoothing trace:

Exponential Smoothing Traces
============================

The `exponential smoothing trace`_ collection is used to store the resulting
:ref:`signal traces <signal trace>` produced by the :ref:`second-order exponential
smoothing <second-order exponential smoothing>` of the signal :attr:`~Trace.samples`
of a :ref:`signal trace <signal trace>`.

Create the Trace Collection
---------------------------

You can create an `exponential smoothing trace`_ collection without
:attr:`~Trace.samples` by calling the :class:`ExponentialSmoothingTraces` class.

  >>> # create an empty exponential smoothing trace collection
  >>> traces = ExponentialSmoothingTraces()
  >>> traces
  ExponentialSmoothingTraces(forecast=Trace(label='Trace', samples=[]),
                             forecast_sign=Trace(label='Trace', samples=[]),
                             level=Trace(label='Trace', samples=[]),
                             level_sign=Trace(label='Trace', samples=[]),
                             prognosis1=Trace(label='Trace', samples=[]),
                             prognosis2=Trace(label='Trace', samples=[]),
                             prognosis=Trace(label='Trace', samples=[]),
                             smoothed1=Trace(label='Trace', samples=[]),
                             smoothed2=Trace(label='Trace', samples=[]),
                             trend=Trace(label='Trace', samples=[]),
                             trend_sign=Trace(label='Trace', samples=[]),
                             trend_inflection=Trace(label='Trace', samples=[]),
                             error=Trace(label='Trace', samples=[]),
                             correction=Trace(label='Trace', samples=[]),
                             absolute_error=Trace(label='Trace', samples=[]),
                             variance=Trace(label='Trace', samples=[]),
                             deviation=Trace(label='Trace', samples=[]),
                             skew=Trace(label='Trace', samples=[]),
                             kurtosis=Trace(label='Trace', samples=[]))

Number of Traces
----------------

You can get the number of the traces in the :class:`ExponentialSmoothingTraces`
collection with the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(traces)
  19

Names of the Traces
-------------------

You can get the :class:`list` with the names of the traces in the
:class:`ExponentialSmoothingTraces` collection.

A :class:`list` with the key names of the traces is returned.

  >>> # key names of the traces in the collection
  >>> list(traces)
  ['forecast',
   'forecast_sign',
   'level',
   'level_sign',
   'prognosis1',
   'prognosis2',
   'prognosis',
   'smoothed1',
   'smoothed2',
   'trend',
   'trend_sign',
   'trend_inflection',
   'error',
   'correction',
   'absolute_error',
   'variance',
   'deviation',
   'skew',
   'kurtosis']

  >>> # key names of the traces in the collection
  >>> list(traces.keys())
  ['forecast',
   'forecast_sign',
   'level',
   'level_sign',
   'prognosis1',
   'prognosis2',
   'prognosis',
   'smoothed1',
   'smoothed2',
   'trend',
   'trend_sign',
   'trend_inflection',
   'error',
   'correction',
   'absolute_error',
   'variance',
   'deviation',
   'skew',
   'kurtosis']

Forecast Trace
--------------

You can get the *forecast* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.forecast` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *forecast* :attr:`~Trace.samples` is returned.

  >>> # forecast trace by attribute
  >>> traces.forecast
  Trace(label='Trace', samples=[])
  >>> # forecast trace by key
  >>> traces['forecast']
  Trace(label='Trace', samples=[])

Forecast Sign Trace
-------------------

You can get the *forecast sign* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.forecast_sign` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *forecast sign* :attr:`~Trace.samples` is returned.

  >>> # forecast sign trace by attribute
  >>> traces.forecast_sign
  Trace(label='Trace', samples=[])
  >>> # forecast trace by key
  >>> traces['forecast_sign']
  Trace(label='Trace', samples=[])

Level Trace
-----------

You can get the *level* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.level` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *level* :attr:`~Trace.samples` is returned.

  >>> # level trace by attribute
  >>> traces.level
  Trace(label='Trace', samples=[])
  >>> # level trace by key
  >>> traces['level']
  Trace(label='Trace', samples=[])

Level Sign Trace
----------------

You can get the *level sign* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.level_sign` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *level* :attr:`~Trace.samples` is returned.

  >>> # level sign trace by attribute
  >>> traces.level_sign
  Trace(label='Trace', samples=[])
  >>> # level sign trace by key
  >>> traces['level_sign']
  Trace(label='Trace', samples=[])

1st-order Prognosis Trace
-------------------------

You can get the *1st-order prognosis* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.prognosis1` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *1st-order prognosis* :attr:`~Trace.samples`
is returned.

  >>> # 1st-order prognosis trace by attribute
  >>> traces.prognosis1
  Trace(label='Trace', samples=[])
  >>> # 1st-order prognosis trace by key
  >>> traces['prognosis1']
  Trace(label='Trace', samples=[])

2nd-order Prognosis Trace
-------------------------

You can get the *2nd-order prognosis* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.prognosis2` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *2nd-order prognosis* :attr:`~Trace.samples`
is returned.

  >>> # 2nd-order prognosis trace by attribute
  >>> traces.prognosis2
  Trace(label='Trace', samples=[])
  >>> # 2nd-order prognosis trace by key
  >>> traces['prognosis2']
  Trace(label='Trace', samples=[])

1st-order Smoothed Trace
------------------------

You can get the *1st-order smoothed* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.smoothed1` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *1st-order smoothed* :attr:`~Trace.samples`
is returned.

  >>> # 1st-order smoothed trace by attribute
  >>> traces.smoothed1
  Trace(label='Trace', samples=[])
  >>> # 1st-order smoothed trace by key
  >>> traces['smoothed1']
  Trace(label='Trace', samples=[])

2nd-order Smoothed Trace
------------------------

You can get the *2nd-order smoothed* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.smoothed2` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *2nd-order prognosis* :attr:`~Trace.samples`
is returned.

  >>> # 2nd-order smoothed trace by attribute
  >>> traces.smoothed2
  Trace(label='Trace', samples=[])
  >>> # 2nd-order smoothed trace by key
  >>> traces['smoothed2']
  Trace(label='Trace', samples=[])

Trend Trace
-----------

You can get the *trend* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.trend` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *trend* :attr:`~Trace.samples` is returned.

  >>> # trend trace by attribute
  >>> traces.trend
  Trace(label='Trace', samples=[])
  >>> # trend trace by key
  >>> traces['trend']
  Trace(label='Trace', samples=[])

Trend Sign Trace
----------------

You can get the *trend sign* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.trend_sign` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *trend sign* :attr:`~Trace.samples` is returned.

  >>> # trend sign trace by attribute
  >>> traces.trend_sign
  Trace(label='Trace', samples=[])
  >>> # trend sign trace by key
  >>> traces['trend_sign']
  Trace(label='Trace', samples=[])

Absolute Error Trace
--------------------

You can get the *absolute error* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.absolute_error` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *absolute error* :attr:`~Trace.samples` is returned.

  >>> # absolute error trace by attribute
  >>> traces.absolute_error
  Trace(label='Trace', samples=[])
  >>> # absolute error trace by key
  >>> traces['absolute_error']
  Trace(label='Trace', samples=[])

Variance Trace
--------------

You can get the *variance* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.variance` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *variance* :attr:`~Trace.samples` is returned.

  >>> # variance trace by attribute
  >>> traces.variance
  Trace(label='Trace', samples=[])
  >>> # variance trace by key
  >>> traces['variance']
  Trace(label='Trace', samples=[])

Standard Deviation Trace
------------------------

You can get the *standard deviation* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.deviation` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *standard deviation* :attr:`~Trace.samples`
is returned.

  >>> # standard deviation trace by attribute
  >>> traces.deviation
  Trace(label='Trace', samples=[])
  >>> # standard deviation trace by key
  >>> traces['deviation']
  Trace(label='Trace', samples=[])

Skew Trace
----------

You can get the *skew* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.skew` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *skew* :attr:`~Trace.samples` is returned.

  >>> # biased skew trace by attribute
  >>> traces.skew
  Trace(label='Trace', samples=[])
  >>> # biased skew trace by key
  >>> traces['skew']
  Trace(label='Trace', samples=[])

Kurtosis Trace
--------------

You can get the *kurtosis* :class:`Trace` with the
:attr:`~ExponentialSmoothingTraces.kurtosis` attribute from the
:class:`ExponentialSmoothingTraces` collection.

The :class:`Trace` with the *kurtosis* :attr:`~Trace.samples` is returned.

  >>> # biased kurtosis trace by attribute
  >>> traces.kurtosis
  Trace(label='Trace', samples=[])
  >>> # biased kurtosis trace by key
  >>> traces['kurtosis']
  Trace(label='Trace', samples=[])
