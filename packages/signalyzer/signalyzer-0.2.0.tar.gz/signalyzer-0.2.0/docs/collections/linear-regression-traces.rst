.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _linear regression trace:

Linear Regression Traces
========================

The `linear regression trace`_ collection is used to store the resulting
:ref:`signal traces <signal trace>` produced by the :ref:`moving linear regression
<moving linear regression>` over the :attr:`~Trace.samples` of a
:ref:`signal trace <signal trace>`.

Create the Trace Collection
---------------------------

You can create a `linear regression trace`_  collection without
:attr:`~Trace.samples` by calling the :class:`LinearRegressionTraces` class.

  >>> # create an empty linear regression trace collection
  >>> traces = LinearRegressionTraces()
  >>> traces
  LinearRegressionTraces(level=Trace(label='Trace', samples=[]),
                         slope=Trace(label='Trace', samples=[]),
                         intercept=Trace(label='Trace', samples=[]),
                         mean=Trace(label='Trace', samples=[]),
                         median=Trace(label='Trace', samples=[]),
                         minimum=Trace(label='Trace', samples=[]),
                         maximum=Trace(label='Trace', samples=[]),
                         range=Trace(label='Trace', samples=[]),
                         error=Trace(label='Trace', samples=[]),
                         negative_error=Trace(label='Trace', samples=[]),
                         positive_error=Trace(label='Trace', samples=[]),
                         absolute_error=Trace(label='Trace', samples=[]),
                         variance=Trace(label='Trace', samples=[]),
                         deviation=Trace(label='Trace', samples=[]),
                         skew=Trace(label='Trace', samples=[]),
                         kurtosis=Trace(label='Trace', samples=[]))

Number of Traces
----------------

You can get the number of the traces in the :class:`LinearRegressionTraces`
collection with the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(traces)
  16

Names of the Traces
-------------------

You can get the :class:`list` with the names of the traces in the
:class:`LinearRegressionTraces` collection.

A :class:`list` with the key names of the traces is returned.

  >>> # key names of the traces in the collection
  >>> list(traces)
  ['level',
   'slope',
   'intercept',
   'mean',
   'median',
   'minimum',
   'maximum',
   'range',
   'error',
   'negative_error',
   'positive_error',
   'absolute_error',
   'variance',
   'deviation',
   'skew',
   'kurtosis']

  >>> # key names of the traces in the collection
  >>> list(traces.keys())
  ['level',
   'slope',
   'intercept',
   'mean',
   'median',
   'minimum',
   'maximum',
   'range',
   'error',
   'negative_error',
   'positive_error',
   'absolute_error',
   'variance',
   'deviation',
   'skew',
   'kurtosis']

Level Trace
-----------

You can get the *level* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.level` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *level* :attr:`~Trace.samples` is returned.

  >>> # level trace by attribute
  >>> traces.level
  Trace(label='Trace', samples=[])
  >>> # level trace by key
  >>> traces['level']
  Trace(label='Trace', samples=[])

Slope Trace
-----------

You can get the *slope* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.slope` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *slope* :attr:`~Trace.samples` is returned.

  >>> # slope trace by attribute
  >>> traces.slope
  Trace(label='Trace', samples=[])
  >>> # slope trace by key
  >>> traces['slope']
  Trace(label='Trace', samples=[])

Intercept Trace
---------------

You can get the *intercept* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.intercept` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *intercept* :attr:`~Trace.samples` is returned.

  >>> # intercept trace by attribute
  >>> traces.intercept
  Trace(label='Trace', samples=[])
  >>> # intercept trace by key
  >>> traces['intercept']
  Trace(label='Trace', samples=[])

Mean Trace
----------

You can get the *mean* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.mean` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *mean* :attr:`~Trace.samples` is returned.

  >>> # mean trace by attribute
  >>> traces.mean
  Trace(label='Trace', samples=[])
  >>> # mean trace by key
  >>> traces['mean']
  Trace(label='Trace', samples=[])

Median Trace
------------

You can get the *median* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.median` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *median* :attr:`~Trace.samples` is returned.

  >>> # median trace by attribute
  >>> traces.median
  Trace(label='Trace', samples=[])
  >>> # median trace by key
  >>> traces['median']
  Trace(label='Trace', samples=[])

Minimum Trace
-------------

You can get the *minimum* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.minimum` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *minimum* :attr:`~Trace.samples` is returned.

  >>> # minimum trace by attribute
  >>> traces.minimum
  Trace(label='Trace', samples=[])
  >>> # minimum trace by key
  >>> traces['minimum']
  Trace(label='Trace', samples=[])

Maximum Trace
-------------

You can get the *maximum* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.maximum` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *maximum* :attr:`~Trace.samples` is returned.

  >>> # maximum trace by attribute
  >>> traces.maximum
  Trace(label='Trace', samples=[])
  >>> # maximum trace by key
  >>> traces['maximum']
  Trace(label='Trace', samples=[])

Range Trace
-----------

You can get the *range* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.range` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *range* :attr:`~Trace.samples` is returned.

  >>> # range trace by attribute
  >>> traces.range
  Trace(label='Trace', samples=[])
  >>> # range trace by key
  >>> traces['range']
  Trace(label='Trace', samples=[])

Error Trace
-----------

You can get the *error* :class:`Trace` for the approximated lines with
the :attr:`~LinearRegressionTraces.error` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *error* :attr:`~Trace.samples` is returned.

  >>> # error trace by attribute
  >>> traces.error
  Trace(label='Trace', samples=[])
  >>> # error trace by key
  >>> traces['error']
  Trace(label='Trace', samples=[])

Maximal Negative Error Trace
----------------------------

You can get the maximal *negative error* :class:`Trace` for the approximated
lines with the :attr:`~LinearRegressionTraces.error` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *negative error* :attr:`~Trace.samples` is returned.

  >>> # maximal negative error trace by attribute
  >>> traces.negative_error
  Trace(label='Trace', samples=[])
  >>> # maximal negative error trace by key
  >>> traces['negative_error']
  Trace(label='Trace', samples=[])

Maximal Positive Error Trace
----------------------------

You can get the maximal *positive error* :class:`Trace` for the approximated
lines with the :attr:`~LinearRegressionTraces.error` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *positive error* :attr:`~Trace.samples` is returned.

  >>> # maximal positive error trace by attribute
  >>> traces.positive_error
  Trace(label='Trace', samples=[])
  >>> # maximal positive error trace by key
  >>> traces['positive_error']
  Trace(label='Trace', samples=[])

Absolute Error Trace
--------------------

You can get the *absolute error* :class:`Trace` for the approximated lines with
the :attr:`~LinearRegressionTraces.absolute_error` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *absolute error* :attr:`~Trace.samples` is returned.

  >>> # absolute error trace by attribute
  >>> traces.absolute_error
  Trace(label='Trace', samples=[])
  >>> # absolute error trace by key
  >>> traces['absolute_error']
  Trace(label='Trace', samples=[])

Variance Trace
--------------

You can get the *variance* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.variance` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *variance* :attr:`~Trace.samples` is returned.

  >>> # variance trace by attribute
  >>> traces.variance
  Trace(label='Trace', samples=[])
  >>> # variance trace by key
  >>> traces['variance']
  Trace(label='Trace', samples=[])

Standard Deviation Trace
------------------------

You can get the *standard deviation* :class:`Trace` for the approximated lines
with the :attr:`~LinearRegressionTraces.deviation` attribute from the
:class:`LinearRegressionTraces` collection.

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

You can get the *skew* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.skew` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *skew* :attr:`~Trace.samples` is returned.

  >>> # biased skew trace by attribute
  >>> traces.skew
  Trace(label='Trace', samples=[])
  >>> # biased skew trace by key
  >>> traces['skew']
  Trace(label='Trace', samples=[])

Kurtosis Trace
--------------

You can get the *kurtosis* :class:`Trace` for the approximated lines with the
:attr:`~LinearRegressionTraces.kurtosis` attribute from the
:class:`LinearRegressionTraces` collection.

The :class:`Trace` with the *kurtosis* :attr:`~Trace.samples` is returned.

  >>> # biased kurtosis trace by attribute
  >>> traces.kurtosis
  Trace(label='Trace', samples=[])
  >>> # biased kurtosis trace by key
  >>> traces['kurtosis']
  Trace(label='Trace', samples=[])
