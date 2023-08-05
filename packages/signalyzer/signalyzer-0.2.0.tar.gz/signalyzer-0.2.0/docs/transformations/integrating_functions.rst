.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Integrating Functions
=====================

.. _accumulate:

Accumulate
----------

You can accumulate the signal *samples* by calling the method
:func:`~Trace.accumulate`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'accumulate'`` is returned.

  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).accumulate()
  Trace(label='Signal:accumulate', samples=[-1.5, -2.0, -2.0, -1.5, 0.0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = signal.accumulate()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers', fill='tozeroy')])


.. _sums positive:

Sums Positive
-------------

You can integrate the signal *samples* limited to positive sums by calling the
method :func:`~Trace.sums_positive`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sums_positive'`` is returned.

  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).sums_positive()
  Trace(label='Signal:sums_positive', samples=[0, 0, 0, 0.5, 2.0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = signal.sums_positive()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers', fill='tozeroy')])


.. _sums negative:

Sums Negative
-------------

You can integrate the signal *samples* limited to negative sums by calling the
method :func:`~Trace.sums_negative`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sums_negative'`` is returned.

  >>> Trace('Signal', [1.5, 0.5, 0, -0.5, -1.5]).sums_negative()
  Trace(label='Signal:sums_negative', samples=[0, 0, 0, -0.5, -2.0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [1.5, 0.5, 0, -0.5, -1.5])
  trace = signal.sums_negative()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers', fill='tozeroy')])
