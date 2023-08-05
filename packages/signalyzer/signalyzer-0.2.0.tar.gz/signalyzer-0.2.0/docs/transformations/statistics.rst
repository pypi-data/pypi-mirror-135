.. _plotly: https://plotly.com/python/
.. _numpy: https://numpy.org/doc/stable/reference

.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _signal statistics:

Statistics
==========

The aim of the **descriptive** statistics is to provide

- measures of central tendency for the signal :attr:`~Trace.samples` including
  `mean`_, `weighted mean`_, `winsor mean`_, `median`_, `mode`_ and `midrange`_.
- measures of variability or dispersion for the signal :attr:`~Trace.samples`
  including `minimum`_, `maximum`_, `range`_, `average absolute deviation`_,
  `median absolute deviation`_, `variance`_, `standard deviation`_,
  `coefficient of variation`_, `skew`_ and `kurtosis`_.

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  go.Figure([signal.plot(mode='markers+lines')])

.. _number of samples:

Number of Sample
----------------

You can compute the *number* of the signal :attr:`~Trace.samples` with the
built-in function :func:`len`.

  >>> # number of signal samples
  >>> len(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  6

.. _sum:

Sum of the Samples
------------------

You can compute the *sum* :math:`x_{sum} = \sum\limits_{i=0}^{N}{x_i}` of the
signal :attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.sum`.

  >>> # sum of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).sum()
  10.0

You can compute the *sum* :math:`x_{sum}` of the signal :attr:`~Trace.samples`
with the built-in function :func:`sum`.

  >>> # sum of the signal samples
  >>> sum(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  10.0

.. _count:

Count Occurrences in the Samples
--------------------------------

You can count the occurrences of a sample :math:`x` in the signal
:attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.count`.

  >>> # count occurrences in the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).count(1.5)
  1

.. _sort:

Sort the Samples
----------------

You can sort the signal :attr:`~Trace.samples` in ascending order by calling the
method :meth:`~Trace.sort`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sort'`` is returned.

  >>> Trace('Signal', [1.3, 1.4, 1.5, 1.6, 1.7, 2.5]).sort()
  Trace(label='Signal:sort', samples=[1.3, 1.4, 1.5, 1.6, 1.7, 2.5])

You can sort the signal :attr:`~Trace.samples` in ascending order with the
built-in function :func:`sorted`.

  >>> sorted(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  [1.3, 1.4, 1.5, 1.6, 1.7, 2.5]

.. _winsorize:

Winsorize the Samples
---------------------

You can winsorize the signal :attr:`~Trace.samples` by calling the
method :meth:`~Trace.winsorize`, either with the percentage *limits* of the
`number of samples`_ shall be "trimmed" for each side of the ascending sorted
signal :attr:`~Trace.samples`, or with the percentage limit of the `number of
samples`_ shall be "trimmed" from both sides.

  >>> # winsorized signal samples with 20% of the largest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsorize((None, 0.2))
  Trace(label='Signal:winsorize', samples=[1.5, 1.6, 1.4, 1.7, 1.3, 1.7])

  >>> # winsorized signal samples with 20% of the smallest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsorize((0.2, None))
  Trace(label='Signal:winsorize', samples=[1.5, 1.6, 1.4, 2.5, 1.4, 1.7])

  >>> # winsorized signal samples with 20% of smallest and largest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsorize(0.2)
  Trace(label='Signal:winsorize', samples=[1.5, 1.6, 1.4, 1.7, 1.4, 1.7])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = signal.winsorize(0.2)

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')


.. _mean:

Mean of the Samples
-------------------

.. note::

  The *mean* :math:`\overline{x}` is the 1st common moment :math:`\mu_1` in the
  descriptive statistics.

You can compute the arithmetic *mean*
:math:`\overline{x} = \frac{1}{N} \cdot \sum\limits_{i=0}^{N}{x_i}` of the signal
:attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.mean`.

  >>> # arithmetic mean of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).mean()
  1.6666666666666667

You can compute the arithmetic *mean* :math:`\overline{x}` of the signal
:attr:`~Trace.samples` :math:`N` with the function :func:`~statistics.mean`
of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # arithmetic mean of the signal samples
  >>> stats.mean(list(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])))
  1.6666666666666667

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Mean', [signal.mean()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _weighted mean:

Weighted Mean of the Samples
----------------------------

You can compute the linear *weighted mean*
:math:`\overline{x_w} = \frac{2}{N \cdot (N + 1)} \cdot
\sum\limits_{i=0}^{N}{(i+1) \cdot x_i}` of the signal :attr:`~Trace.samples`
:math:`N` by calling the method :meth:`~Trace.weighted_mean`.

  >>> # linear weighted mean of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).weighted_mean()
  1.6952380952380948

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Linear-Weighted Mean', [signal.weighted_mean()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _winsor mean:

Winsor Mean of the Samples
--------------------------

You can compute the *winsor mean* :math:`\overline{x}_{w\alpha}` of the signal
:attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.winsor_mean`,
either with the percentage *limits* of the `number of samples`_ shall be "trimmed"
for each side of the ascending sorted signal :attr:`~Trace.samples`, or with the
percentage limit of the `number of samples`_ shall be "trimmed" from both sides.

  >>> # mean of the signal samples with 20% of the largest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsor_mean((None, 0.2))
  1.5333333333333332

  >>> # mean of the signal samples with 20% of the smallest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsor_mean((0.2, None))
  1.6833333333333333

  >>> # mean of the signal samples with 20% of smallest and largest samples trimmed
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).winsor_mean(0.2)
  1.55

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Winsor Mean', [signal.winsor_mean(0.2)] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _median:

Median of the Samples
---------------------

You can compute the *median* :math:`\overline{x}_{med}` of the signal
:attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.median`.

  >>> # median of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).median()
  1.55

You can compute the *median* :math:`\overline{x}_{med}` of the signal
:attr:`~Trace.samples` :math:`N` with the function :func:`~statistics.median`
of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # median of the signal samples
  >>> stats.median(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  1.55

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Median', [signal.median()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _mode:

Mode of the Samples
-------------------

You can compute the *mode* :math:`\overline{x}_{mod}` of the signal
:attr:`~Trace.samples` :math:`N` by calling the method :meth:`~Trace.mode`.

  >>> # mode of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).mode()
  1.5

You can compute the *mode* :math:`\overline{x}_{mod}` of the signal
:attr:`~Trace.samples` :math:`N` with the function :func:`~statistics.mode`
of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # mode of the signal samples
  >>> stats.mode(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  1.5

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Mode', [signal.mode()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _rms:

Root mean square of the Samples
-------------------------------

You can compute the *root mean square*
:math:`x_{rms} = \sqrt{\frac{1}{N} \cdot \sum\limits_{i=0}^{N}{x_i^2}}`
of the signal :attr:`~Trace.samples` :math:`N` by calling the method
:meth:`~Trace.rms`.

  >>> # median of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).rms()
  1.7126976771553504

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Rms', [signal.rms()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _minimum:

Minimum Sample
--------------

You can get the *minimum* :math:`x_{min}` within the signal :attr:`~Trace.samples`
:math:`N` by calling the method :meth:`~Trace.min`.

  >>> # minimum signal value in the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).min()
  1.3

You can get the *minimum* :math:`x_{min}` within the signal :attr:`~Trace.samples`
:math:`N` with the built-in function :func:`min`.

  >>> # minimum signal value in the signal samples
  >>> min(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  1.3

.. _maximum:

Maximum Sample
--------------

You can get the *maximum* :math:`x_{max}` within the signal :attr:`~Trace.samples`
:math:`N` by calling the method :meth:`~Trace.max`.

  >>> # maximum signal value in the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).max()
  2.5

You can get the *maximum*  :math:`x_{max}` within the signal :attr:`~Trace.samples`
:math:`N` with the built-in function :func:`max`.

  >>> # maximum signal value in the signal samples
  >>> max(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  2.5

.. _range:

Range of the Samples
--------------------

You can compute the *range* :math:`x_{max} - x_{min}` of the signal
:attr:`~Trace.samples` :math:`N`  by calling the method :meth:`~Trace.range`.

  >>> # range of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).range()
  1.2

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Range', [signal.min()] * len(signal) + [signal.max()] * len(signal))

  plots = [
    signal.plot(),
    trace.plot(
      x=signal.x_values + list(reversed(signal.x_values)),
      fill='toself',
      line_color='rgba(255,255,255,0)',
      fillcolor='rgba(0,176,246,0.2)')]

  go.Figure(plots).update_traces(mode='markers+lines')

.. _midrange:

Mid-Range of the Samples
------------------------

You can compute the *midrange* :math:`\frac{x_{max} + x_{min}}{2}` of the signal
:attr:`~Trace.samples` :math:`N`  by calling the method :meth:`~Trace.midrange`.

  >>> # mid-range of the signal samples
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).midrange()
  1.9

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Mid-Range', [signal.midrange()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _average absolute deviation:
.. _AAD:

Average Absolute Deviation of the Samples
-----------------------------------------

.. note::

  The *average absolute deviation* is the 1st central moment :math:`m_1`
  in the descriptive statistics.

You can compute the *absolute error* or *average absolute deviation*
:math:`D_{mean} = m_1 = \frac{1}{N} \cdot \sum\limits_{i=0}^{N}
{\left| x_i - \overline{x} \right|}`
of the signal :attr:`~Trace.samples` :math:`N` distribution.

  >>> # average absolute deviation of the distribution
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).aad()
  0.2888888888888889

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('AAD', [signal.aad()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')


.. _median absolute deviation:
.. _MAD:

Median Absolute Deviation of the Samples
----------------------------------------

You can compute the *median absolute deviation*
:math:`D_{med} = \frac{1}{N} \cdot \sum\limits_{i=0}^{N}
{\left| x_i - \overline{x}_{med} \right|}`
of the signal :attr:`~Trace.samples` :math:`N` distribution.

  >>> # median absolute deviation of the distribution
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).mad()
  0.26666666666666666

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('MAD', [signal.mad()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _variance:

Variance of the Samples
-----------------------

.. note::

  The *variance* :math:`\sigma^2` is the 2nd central moment :math:`m_2` in the
  descriptive statistics.

You can compute the biased sample *variance*
:math:`s^2 = \sigma^2 = m_2 = \frac{1}{N} \cdot \sum\limits_{i=0}^{N}
{(x_i - \overline{x})^2}`
of the signal :attr:`~Trace.samples` :math:`N` distribution by calling the method
:meth:`~Trace.variance`.

  >>> # biased sample variance
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).variance()
  0.15555555555555553

You can compute the biased sample *variance* :math:`s^2` of the signal
:attr:`~Trace.samples` :math:`N` distribution with the function
:func:`~statistics.pvariance` of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # biased sample variance
  >>> stats.pvariance(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  0.15555555555555556

You can compute the unbiased sample *variance* :math:`s^2` of the signal
:attr:`~Trace.samples` :math:`N - 1` distribution with the function
:func:`~statistics.variance` of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # unbiased sample variance
  >>> stats.variance(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  0.18666666666666668

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Variance', [signal.variance()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _standard deviation:

Standard deviation of the Samples
---------------------------------

You can compute the biased sample *standard deviation*
:math:`s = \sigma= \sqrt{\sigma^2} = \sqrt{m_2}` of the signal
:attr:`~Trace.samples` :math:`N` distribution  by calling the method
:meth:`~Trace.std`.

  >>> # biased sample standard deviation
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).std()
  0.3944053188733077

You can compute the unbiased sample *standard deviation* :math:`s` of the signal
:attr:`~Trace.samples` :math:`N - 1` distribution with the function
:func:`~statistics.stdev` of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # unbiased sample standard deviation
  >>> stats.stdev(Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]))
  0.43204937989385733

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Deviation', [signal.std()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _coefficient of variation:

Coefficient of Variation of the Samples
---------------------------------------

You can compute the *coefficient of variation*
:math:`c_v = \frac{\sigma}{\overline{x}}` of the signal :attr:`~Trace.samples`
:math:`N` distribution by calling the method :meth:`~Trace.coefficient`.

  >>> # coefficient of variation of the distribution
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).coefficient()
  0.23664319132398462

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Coefficient', [signal.coefficient()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _skew:

Skew of the Samples
-----------------------

.. note::

  The *skew* is the 3rd central moment :math:`m_3` in the descriptive
  statistics.

You can compute the biased sample *skew*
:math:`{m}_3 = \sum\limits_{i=0}^{N}{(\frac{x_i - \overline{x}}{\sigma})^3}`
of the signal :attr:`~Trace.samples` :math:`N` distribution by calling the
method :meth:`~Trace.skew`.

  >>> # biased sample skew
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).skew()
  1.3733756639338395

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Skew', [signal.skew()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _kurtosis:

Kurtosis of the Samples
-----------------------

.. note::

  The *kurtosis* is the 4th central moment :math:`m_4` in the descriptive
  statistics.

You can compute the biased sample *kurtosis*
:math:`{m}_4 = \sum\limits_{i=0}^{N}{(\frac{x_i - \overline{x}}{\sigma})^4}`
of the signal :attr:`~Trace.samples` :math:`N` distribution by calling the
method :meth:`~Trace.kurtosis`.

  >>> # biased sample kurtosis
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).kurtosis()
  3.4864285714285725

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = Trace('Kurtosis', [signal.kurtosis()] * len(signal))

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

.. _distribution:

Distribution of the Samples
---------------------------

Histogram Plot
~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  go.Figure([go.Histogram(x=list(trace), nbinsy=7)])

Empirical Cumulative Distribution Plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  px.ecdf(trace, markers=True, marginal="histogram")

Distribution Plot
~~~~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace
  import plotly.figure_factory as ff

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  ff.create_distplot([trace.samples], [trace.label], bin_size=trace.range() / len(trace))


.. _quantiles:

Quantiles of the Samples
------------------------

You can compute the *nth-quantile* :math:`q_n` of the signal :attr:`~Trace.samples`
with the function :func:`~statistics.quantiles` of the :mod:`statistics` module.

  >>> import statistics as stats
  >>> # quartiles of the samples maximal value excluded
  >>> stats.quantiles(Trace('Signal', range(11)))
  [2.0, 5.0, 8.0]
  >>> # quartiles of the samples maximal value included
  >>> stats.quantiles(Trace('Signal', range(11)), method='inclusive')
  [2.5, 5.0, 7.5]
  >>> # deciles of the samples maximal value excluded
  >>> stats.quantiles(Trace('Signal', range(11)), n=10)
  [0.2, 1.4, 2.6, 3.8, 5.0, 6.2, 7.4, 8.6, 9.8]

Quartiles: Box Plot
~~~~~~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  go.Figure([go.Box(name=trace.label, x=list(trace), quartilemethod='inclusive', boxpoints='all', boxmean='sd')])


Quartiles: Violin Plot
~~~~~~~~~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])

  go.Figure([go.Violin(name=trace.label, x=list(trace), box_visible=True, points='all', meanline_visible=True)])

.. _zscore:

Z-Score of the Samples
----------------------

You can compute for each signal *sample* :math:`x` the *zscore*
:math:`z = \frac{x - \bar{x}}{\sigma}` by calling the method
:meth:`~Trace.zscore`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'zscore'`` is returned.

  >>> # score for each signal sample
  >>> Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).zscore()
  Trace(label='Signal:zscore',
        samples=[-0.4225771273642585, -0.16903085094570328, -0.6761234037828138,
                 2.1128856368212916, -0.9296696802013684, 0.08451542547285136])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7])
  trace = signal.zscore(label='Zscore')

  go.Figure([signal.plot(), trace.plot()]).update_traces(mode='markers+lines')

Z-Score: Histogram Plot
~~~~~~~~~~~~~~~~~~~~~~~

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1.5, 1.6, 1.4, 2.5, 1.3, 1.7]).zscore(label='Zscore')

  go.Figure([go.Histogram(x=list(trace), nbinsx=7)])
