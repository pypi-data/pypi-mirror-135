.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _statistics trace:

Statistics Traces
=================

The `statistics trace`_ collection is used to store the resulting :ref:`signal
traces <signal trace>` produced by the :ref:`signal statistics <signal statistics>`
analysis of sets of signal :attr:`~Trace.samples`.

Combination of Traces
---------------------

You can combine with the :func:`combine` function the signal :attr:`~Trace.samples`
of multiple :ref:`signal traces <signal trace>` to statistically analyze each
set of the combined signal :attr:`~Trace.samples` according to the
:ref:`signal statistics <signal statistics>`.

A :class:`dict` with the produced :ref:`signal traces <signal trace>` is returned.

  >>> combine(Trace('Signal', [1, 2, 3]), [3, 2, 1], range(3), 2)
  {'mean': Trace(label='SetTrace:mean',
                 samples=[1.5, 1.75, 2]),
   'weighted_mean': Trace(label='SetTrace:weighted_mean',
                    samples=[1.5, 1.7000000000000002, 1.9000000000000001]),
   'median': Trace(label='SetTrace:median',
                    samples=[1.5, 2.0, 2.0]),
   'mode': Trace(label='SetTrace:mode',
                 samples=[1, 2, 2]),
   'rms': Trace(label='SetTrace:rms',
                samples=[1.8708286933869707,
                         1.8027756377319946,
                         2.1213203435596424]),
   'minimum': Trace(label='SetTrace:minimum',
                    samples=[0, 1, 1]),
   'maximum': Trace(label='SetTrace:maximum',
                    samples=[3, 2, 3]),
   'range': Trace(label='SetTrace:range',
                  samples=[3, 1, 2]),
   'midrange': Trace(label='SetTrace:midrange',
                     samples=[1.5, 1.5, 2.0]),
   'absolute_error': Trace(label='SetTrace:absolute_error',
                           samples=[4.0, 1.5, 2]),
   'variance': Trace(label='SetTrace:variance',
                     samples=[1.25, 0.1875, 0.5]),
   'deviation': Trace(label='SetTrace:deviation',
                      samples=[1.118033988749895,
                               0.4330127018922193,
                               0.7071067811865476]),
   'coefficient': Trace(label='SetTrace:coefficient',
                        samples=[0.7453559924999299,
                                 0.24743582965269675,
                                 0.3535533905932738]),
   'skew': Trace(label='SetTrace:skew',
                     samples=[0.0, -1.1547005383792517, 0.0]),
   'kurtosis': Trace(label='SetTrace:kurtosis',
                     samples=[1.6400000000000001,
                              2.333333333333334,
                              1.9999999999999993])}

.. note::

  The linear *weighted mean* is computed with the order of the provided operands
  to combine. The lowest weight has the first operand the highest weight has the
  last operand.

Create the Trace Collection
---------------------------

You can create a `statistics trace`_ collection without :attr:`~Trace.samples`
by calling the :class:`StatisticsTraces` class.

  >>> # create an empty statistic trace collection
  >>> traces = StatisticsTraces()
  >>> traces
  StatisticsTraces(mean=Trace(label='Trace', samples=[]),
                   weighted_mean=Trace(label='Trace', samples=[]),
                   median=Trace(label='Trace', samples=[]),
                   mode=Trace(label='Trace', samples=[]),
                   rms=Trace(label='Trace', samples=[]),
                   minimum=Trace(label='Trace', samples=[]),
                   maximum=Trace(label='Trace', samples=[]),
                   range=Trace(label='Trace', samples=[]),
                   midrange=Trace(label='Trace', samples=[]),
                   absolute_error=Trace(label='Trace', samples=[]),
                   variance=Trace(label='Trace', samples=[]),
                   deviation=Trace(label='Trace', samples=[]),
                   coefficient=Trace(label='Trace', samples=[]),
                   skew=Trace(label='Trace', samples=[]),
                   kurtosis=Trace(label='Trace', samples=[]))

Number of Traces
----------------

You can get the number of the traces in the :class:`StatisticsTraces` collection
with the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(traces)
  15

Names of the Traces
-------------------

You can get the :class:`list` with the names of the traces in the
:class:`StatisticsTraces` collection.

A :class:`list` with the key names of the traces is returned.

  >>> # key names of the traces in the collection
  >>> list(traces)
  ['mean',
   'weighted_mean',
   'median',
   'mode',
   'rms',
   'minimum',
   'maximum',
   'range',
   'midrange',
   'absolute_error',
   'variance',
   'deviation',
   'coefficient',
   'skew',
   'kurtosis']

  >>> # key names of the traces in the collection
  >>> list(traces.keys())
  ['mean',
   'weighted_mean',
   'median',
   'mode',
   'rms',
   'minimum',
   'maximum',
   'range',
   'midrange',
   'absolute_error',
   'variance',
   'deviation',
   'coefficient',
   'skew',
   'kurtosis']

Mean Trace
----------

You can get the arithmetic *mean* :class:`Trace` with the
:attr:`~StatisticsTraces.mean` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the arithmetic *mean* :attr:`~Trace.samples`
is returned.

  >>> # mean trace by attribute
  >>> traces.mean
  Trace(label='Trace', samples=[])
  >>> # mean trace by key
  >>> traces['mean']
  Trace(label='Trace', samples=[])

Weighted Mean Trace
-------------------

You can get the linear *weighted mean* :class:`Trace` with the
:attr:`~StatisticsTraces.weighted_mean` attribute from the
:class:`StatisticsTraces` collection.

The :class:`Trace` with the linear *weighted mean* :attr:`~Trace.samples`
is returned.

  >>> # linear weighted mean trace by attribute
  >>> traces.weighted_mean
  Trace(label='Trace', samples=[])
  >>> # linear weighted mean trace by key
  >>> traces['weighted_mean']
  Trace(label='Trace', samples=[])

Median Trace
------------

You can get the *median* :class:`Trace` with the
:attr:`~StatisticsTraces.median` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *median* :attr:`~Trace.samples`
is returned.

  >>> # median trace by attribute
  >>> traces.median
  Trace(label='Trace', samples=[])
  >>> # median trace by key
  >>> traces['median']
  Trace(label='Trace', samples=[])

Mode Trace
----------

You can get the *mode* :class:`Trace` with the
:attr:`~StatisticsTraces.mode` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *mode* :attr:`~Trace.samples`
is returned.

  >>> # mode trace by attribute
  >>> traces.mode
  Trace(label='Trace', samples=[])
  >>> # mode trace by key
  >>> traces['mode']
  Trace(label='Trace', samples=[])

Root Mean Square Trace
----------------------

You can get the *root mean square* :class:`Trace` with the
:attr:`~StatisticsTraces.rms` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *root mean square* :attr:`~Trace.samples`
is returned.

  >>> # root mean square (rms) trace by attribute
  >>> traces.rms
  Trace(label='Trace', samples=[])
  >>> # root mean square (rms) trace by key
  >>> traces['rms']
  Trace(label='Trace', samples=[])

Minimum Trace
-------------

You can get the *minimum* :class:`Trace` with the
:attr:`~StatisticsTraces.minimum` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *minimum* :attr:`~Trace.samples` is returned.

  >>> # minimum trace by attribute
  >>> traces.minimum
  Trace(label='Trace', samples=[])
  >>> # minimum trace by key
  >>> traces['minimum']
  Trace(label='Trace', samples=[])

Maximum Trace
-------------

You can get the *maximum* :class:`Trace` with the
:attr:`~StatisticsTraces.maximum` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *maximum* :attr:`~Trace.samples` is returned.

  >>> # maximum trace by attribute
  >>> traces.maximum
  Trace(label='Trace', samples=[])
  >>> # maximum trace by key
  >>> traces['maximum']
  Trace(label='Trace', samples=[])

Range Trace
-----------

You can get the *range* :class:`Trace` with the
:attr:`~StatisticsTraces.maximum` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *range* :attr:`~Trace.samples` is returned.

  >>> # range trace by attribute
  >>> traces.range
  Trace(label='Trace', samples=[])
  >>> # range trace by key
  >>> traces['range']
  Trace(label='Trace', samples=[])

Mid-Range Trace
---------------

You can get the *midrange* :class:`Trace` with the
:attr:`~StatisticsTraces.midrange` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *midrange* :attr:`~Trace.samples`
is returned.

  >>> # mid-range trace by attribute
  >>> traces.midrange
  Trace(label='Trace', samples=[])
  >>> # mid-range trace by key
  >>> traces['midrange']
  Trace(label='Trace', samples=[])

Absolute Error Trace
--------------------

You can get the *absolute error* :class:`Trace` with the
:attr:`~StatisticsTraces.absolute_error` attribute from the
:class:`StatisticsTraces` collection.

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
:attr:`~StatisticsTraces.variance` attribute from the :class:`StatisticsTraces`
collection.

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
:attr:`~StatisticsTraces.deviation` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *standard deviation* :attr:`~Trace.samples`
is returned.

  >>> # standard deviation trace by attribute
  >>> traces.deviation
  Trace(label='Trace', samples=[])
  >>> # standard deviation trace by key
  >>> traces['deviation']
  Trace(label='Trace', samples=[])

Coefficient of Variation Trace
------------------------------

You can get the *coefficient of variation* :class:`Trace` with the
:attr:`~StatisticsTraces.coefficient` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *coefficient of variation* :attr:`~Trace.samples`
is returned.

  >>> # coefficient of variation trace by attribute
  >>> traces.coefficient
  Trace(label='Trace', samples=[])
  >>> # coefficient of variation trace by key
  >>> traces['coefficient']
  Trace(label='Trace', samples=[])

Skew Trace
----------

You can get the *skew* :class:`Trace` with the
:attr:`~StatisticsTraces.skew` attribute from the :class:`StatisticsTraces`
collection.

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
:attr:`~StatisticsTraces.kurtosis` attribute from the :class:`StatisticsTraces`
collection.

The :class:`Trace` with the *kurtosis* :attr:`~Trace.samples` is returned.

  >>> # biased kurtosis trace by attribute
  >>> traces.kurtosis
  Trace(label='Trace', samples=[])
  >>> # biased kurtosis trace by key
  >>> traces['kurtosis']
  Trace(label='Trace', samples=[])
