.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Differentiating Functions
=========================

.. _delta:

Delta
-----

You can compute the deltas between the consecutive signal *samples* by calling
the method :func:`~Trace.delta`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'delta'`` is returned.

  >>> Trace('Signal', [-1.5, -0.5, 0 , 0.5, -1.5]).delta()
  Trace(label='Signal:delta', samples=[0.0, 1.0, 0.5, 0.5, -2.0])

.. note:: The first signal sample is used as the *preset* value (previous value)
  to compute the delta for the first signal sample.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0 , 0.5, -1.5])
  trace = signal.delta()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _enter_positives:

Enter Positive
--------------

You can check when the signal *samples* enters the positive numbers by calling
the method :func:`~Trace.enter_positive`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'enter_positive'`` is returned.

  >>> Trace('Signal', [0, 1, 1, 1, -1, 1, 1, 1, 0]).enter_positive()
  Trace(label='Signal:enter_positive', samples=[0, 1, 0, 0, 0, 1, 0, 0, 0])


.. note:: The first signal sample is used as the *preset* value (previous value)
  to compute the delta for the first signal sample.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, 1, 1, -1, 1, 1, 1, 0])
  trace = signal.enter_positive()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _left_positives:

Left Positive
-------------

You can check when the signal *samples* left the positive numbers by calling
the method :func:`~Trace.left_positive`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'left_positive'`` is returned.

  >>> Trace('Signal', [1, 1, -1, 0, 1, 1, 0, -1]).left_positive()
  Trace(label='Signal:left_positive', samples=[0, 0, 1, 0, 0, 0, 1, 0])

.. note:: The first signal sample is used as the *preset* value (previous value)
  to compute the delta for the first signal sample.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [1, 1, -1, 0, 1, 1, 0, -1])
  trace = signal.left_positive()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _enter_negatives:

Enter Negative
--------------

You can check when the signal *samples* enters the negative numbers by calling
the method :func:`~Trace.enter_negative`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'enter_negative'`` is returned.

  >>> Trace('Signal', [0, -1, -1, -1, 1, -1, -1, -1, 0]).enter_negative()
  Trace(label='Signal:enter_negative', samples=[0, 1, 0, 0, 0, 1, 0, 0, 0])

.. note:: The first signal sample is used as the *preset* value (previous value)
  to compute the delta for the first signal sample.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [0, -1, -1, -1, 1, -1, -1, -1, 0])
  trace = signal.enter_negative()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _left_negatives:

Left Negative
-------------

You can check when the signal *samples* left the negative numbers by calling
the method :func:`~Trace.left_negative`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'left_negative'`` is returned.

.. note:: The first signal sample is used as the *preset* value (previous value)
  to compute the delta for the first signal sample.

  >>> Trace('Signal', [-1, -1, 1, 0, -1, -1, 0, 1]).left_negative()
  Trace(label='Signal:left_negative', samples=[0, 0, 1, 0, 0, 0, 1, 0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1, -1, 1, 0, -1, -1, 0, 1])
  trace = signal.left_negative()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])
