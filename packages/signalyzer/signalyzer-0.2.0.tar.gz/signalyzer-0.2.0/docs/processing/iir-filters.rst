.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

IIR-Filters
===========

The `Signalyzer` package provides a second-order :class:`IIRFilter` factory
class to compute the normalized filter coefficients for common filter
configurations according to the sampling-time *dt* in seconds of the
:class:`~Trace.samples` for the given cutoff or center frequency *f0* in Hertz
and quality factor *q* of the second-order IIR filter to create.

.. warning::

  The :class:`IIRFilter` factory does neither check if the given parameters are
  valid nor the filter is stable.

.. _band-pass:

Band-Pass Filter
----------------

You can filter the signal :attr:`~Trace.samples` of a :ref:`signal trace
<signal trace>` with a second-order band-pass IIR filter by calling the method
:meth:`~Trace.band_pass` and providing the sampling-time *dt*, the center
frequency *f0*, and the quality factor *q* of the filter.

A new :class:`Trace` instance *labeled* with the performed transformation
``'band-pass'`` is returned.

  >>> # normalized filter coefficients of a second-order band-pass IIR-filter
  >>> IIRFilter.band_pass(dt=0.02, f0=5, q=0.707)
  IIRFilter(b0=0.2936305238633031, b1=0.0, b2=-0.2936305238633031,
            a1=-1.1429298210046335, a2=0.41273895227339397,
            s1=0.0, s2=0.0)

  >>> # signal samples
  >>> signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  >>> # band-pass filtered signal samples
  >>> signal.band_pass(dt=0.02, f0=5, q=0.707)
  Trace(label='Signal:band-pass',
        samples=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.2936305238633031, 0.6292296059438849, 0.5979725261174329,
                 0.4237330639444065, 0.2374906010097415, 0.0965439492463373,
                 0.012321336795657334, -0.025765025201870573, -0.03453311128180103,
                 -0.028834693188924287, -0.018702870555949658, -0.00947486744086301,
                 -0.003109705350460623, 0.00035647188089199533, 0.001690918871249114,
                 0.0017854717722157742, 0.0013427608497287302, 0.0007977476690543828,
                 0.0003575598943283964])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  trace = signal.band_pass(dt=0.02, f0=5, q=0.707)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _low-pass:

Low-Pass Filter
---------------

You can filter the signal :attr:`~Trace.samples` of a :ref:`signal trace
<signal trace>` with a second-order low-pass IIR filter by calling the method
:meth:`~Trace.low_pass` and providing the sampling-time *dt*, the cutoff
frequency *f0*, and the quality factor *q* of the filter.

A new :class:`Trace` instance *labeled* with the performed transformation
``'low-pass'`` is returned.

  >>> # normalized filter coefficients of a second-order low-pass IIR-filter
  >>> IIRFilter.low_pass(dt=0.02, f0=5, q=0.707)
  IIRFilter(b0=0.06745228281719011, b1=0.13490456563438022, b2=0.06745228281719011,
            a1=-1.1429298210046335, a2=0.41273895227339397,
            s1=0.0, s2=0.0)

  >>> # signal samples
  >>> signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  >>> # low-pass filtered signal samples
  >>> signal.low_pass(dt=0.02, f0=5, q=0.707)
  Trace(label='Signal:low-pass',
        samples=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.06745228281719011, 0.27945007397817534, 0.5613607697619523,
                 0.7960651646253372, 0.947960291423087, 1.024694115475641,
                 1.0497024557750898, 1.0466141955337798, 1.0327626146356725,
                 1.0182058750555134, 1.0072856302799662, 1.0008126903161547,
                 0.9979217845891701, 0.9972893166828786, 0.9977596396528264,
                 0.9985582299416725, 0.9992768419877129, 0.9997685558057517,
                 1.0000339510088148])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  trace = signal.low_pass(dt=0.02, f0=5, q=0.707)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _high-pass:

High-Pass Filter
----------------

You can filter the signal :attr:`~Trace.samples` of a :ref:`signal trace
<signal trace>` with a second-order high-pass IIR filter by calling the method
:meth:`~Trace.high_pass` and providing the sampling-time *dt*, the cutoff
frequency *f0*, and the quality factor *q* of the filter.

A new :class:`Trace` instance *labeled* with the performed transformation
``'high-pass'`` is returned.

  >>> # normalized filter coefficients of a second-order high-pass IIR-filter
  >>> IIRFilter.high_pass(dt=0.02, f0=5, q=0.707)
  IIRFilter(b0=0.6389171933195069, b1=-1.2778343866390138, b2=0.6389171933195069,
            a1=-1.1429298210046335, a2=0.41273895227339397,
            s1=0.0, s2=0.0)

  >>> # signal samples
  >>> signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  >>> # high-pass filtered signal samples
  >>> signal.high_pass(dt=0.02, f0=5, q=0.707)
  Trace(label='Signal:high-pass',
        samples=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.6389171933195069, 0.09132032007793989, -0.15933329587938505,
                 -0.21979822856974374, -0.18545089243282875, -0.1212380647219784,
                 -0.062023792570747305, -0.020849170331909583, 0.0017704966461280502,
                 0.010628818133410434, 0.011417240275983231, 0.008662177124708292,
                 0.005187920761290377, 0.002354211436229048, 0.0005494414759238397,
                 -0.00034370171388908854, -0.0006196028374425566,
                 -0.0005663034748070173, -0.0003915109031438213])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  trace = signal.high_pass(dt=0.02, f0=5, q=0.707)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _notch:

Notch Filter
------------

You can filter the signal :attr:`~Trace.samples` of a :ref:`signal trace
<signal trace>` with a second-order notch IIR filter by calling the method
:meth:`~Trace.notch` and providing the sampling-time *dt*, the center frequency
*f0*, and the quality factor *q* of the filter.

A new :class:`Trace` instance *labeled* with the performed transformation
``'notch'`` is returned.

  >>> # normalized filter coefficients of a second-order notch IIR-filter
  >>> IIRFilter.notch(dt=0.02, f0=5, q=0.707)
  IIRFilter(b0=0.706369476136697, b1=-1.1429298210046335, b2=0.706369476136697,
            a1=-1.1429298210046335, a2=0.41273895227339397,
            s1=0.0, s2=0.0)

  >>> # signal samples
  >>> signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  >>> # notch filtered signal samples
  >>> signal.notch(dt=0.02, f0=5, q=0.707)
  Trace(label='Signal:notch',
        samples=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.706369476136697, 0.37077039405611534, 0.4020274738825673,
                 0.5762669360555936, 0.7625093989902586, 0.9034560507536628,
                 0.9876786632043427, 1.0257650252018704, 1.0345331112818008,
                 1.028834693188924, 1.0187028705559493, 1.0094748674408627,
                 1.0031097053504603, 0.9996435281191077, 0.9983090811287505,
                 0.9982145282277839, 0.9986572391502712, 0.9992022523309455,
                 0.9996424401056714])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  trace = signal.notch(dt=0.02, f0=5, q=0.707)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _all-pass:

All-Pass Filter
---------------

You can filter the signal :attr:`~Trace.samples` of a :ref:`signal trace
<signal trace>` with a second-order all-pass IIR filter by calling the method
:meth:`~Trace.all_pass` and providing the sampling-time *dt*, the center
frequency *f0*, and the quality factor *q* of the filter.

A new :class:`Trace` instance *labeled* with the performed transformation
``'all-pass'`` is returned.

  >>> # normalized filter coefficients of a second-order all-pass IIR-filter
  >>> IIRFilter.all_pass(dt=0.02, f0=5, q=0.707)
  IIRFilter(b0=0.41273895227339397, b1=-1.1429298210046335, b2=1.0,
            a1=-1.1429298210046335, a2=0.41273895227339397,
            s1=0.0, s2=0.0)

  >>> # signal samples
  >>> signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  >>> # all-pass filtered signal samples
  >>> signal.all_pass(dt=0.02, f0=5, q=0.707)
  Trace(label='Signal:all-pass',
        samples=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.41273895227339397, -0.2584592118877693, -0.19594505223486536,
                 0.1525338721111873, 0.5250187979805172, 0.8069121015073255,
                 0.9753573264086853, 1.051530050403741, 1.0690662225636018,
                 1.0576693863778486, 1.0374057411118995, 1.0189497348817262,
                 1.0062194107009212, 0.9992870562382159, 0.9966181622575014,
                 0.9964290564555681, 0.9973144783005423, 0.9984045046618911,
                 0.9992848802113432])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', map(lambda x: 0 if x <= 5 else 1, range(25)))
  trace = signal.all_pass(dt=0.02, f0=5, q=0.707)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])
