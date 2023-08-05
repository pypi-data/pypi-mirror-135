.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Mathematical Functions
======================

.. _negation:

Negation
--------

You can negate each signal *sample* with the ``'-'`` operator or by calling
the method :meth:`~Trace.neg`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'neg'`` is returned.

  >>> # negate samples with operator
  >>> -Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:neg', samples=[1, 0, -1])
  >>> # negate samples with method call
  >>> Trace('Signal', [-1, 0, 1]).neg()
  Trace(label='Signal:neg', samples=[1, 0, -1])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = -signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _absolute:

Absolute
--------

You can compute the absolute value for each signal *sample* with the built-in
function :func:`abs` or by calling the method :meth:`~Trace.abs`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'abs'`` is returned.

  >>> abs(Trace('Signal', [-1, 0, 1]))
  Trace(label='Signal:abs', samples=[1, 0, 1])
  >>> Trace('Signal', [-1, 0, 1]).abs()
  Trace(label='Signal:abs', samples=[1, 0, 1])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = abs(signal)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _rounding:

Rounding
--------

You can round each signal *sample* with the built-in function :func:`round` or
by calling the method :meth:`~Trace.round`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'round'`` is returned.

  >>> round(Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]))
  Trace(label='Signal:round', samples=[-2, 0, 0, 0, 2])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).round()
  Trace(label='Signal:round', samples=[-2, 0, 0, 0, 2])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = round(signal)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _truncation:

Truncation
----------

You can truncate each signal *sample* with the function :func:`~math.trunc`
from the :mod:`math` module or by calling the method :meth:`~Trace.trunc`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'trunc'`` is returned.

  >>> import math
  >>> math.trunc(Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]))
  Trace(label='Signal:trunc', samples=[-1, 0, 0, 0, 1])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).trunc()
  Trace(label='Signal:trunc', samples=[-1, 0, 0, 0, 1])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = math.trunc(signal)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _floor:

Round to the Floor
------------------

You can round each signal *sample* to its floor integer with the function
:func:`~math.floor` from the :mod:`math` module or by calling the method
:meth:`~Trace.floor`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'floor'`` is returned.

  >>> import math
  >>> math.floor(Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]))
  Trace(label='Signal:floor', samples=[-2, -1, 0, 0, 1])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).floor()
  Trace(label='Signal:floor', samples=[-2, -1, 0, 0, 1])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = math.floor(signal)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _ceil:

Round to the Ceil
-----------------

You can round each signal *sample* to its ceil integer with the function
:func:`~math.ceil` from the :mod:`math` module or by calling the method
:meth:`~Trace.ceil`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ceil'`` is returned.

  >>> import math
  >>> math.ceil(Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]))
  Trace(label='Signal:ceil', samples=[-1, 0, 0, 1, 2])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).ceil()
  Trace(label='Signal:ceil', samples=[-1, 0, 0, 1, 2])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = math.ceil(signal)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _signum:

Signum
------

You can compute the signum value for each signal *sample* by calling the
method :func:`~Trace.sign`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sign'`` is returned.

  >>> Trace('Signal', [-1.5, -0.5, 0 , 0.5, 1.5]).sign()
  Trace(label='Signal:sign', samples=[-1.0, -1.0, 0, 1.0, 1.0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0 , 0.5, 1.5])
  trace = signal.sign()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])

.. _zeros:

Zeros
-----

You can check each signal *sample* is zero or not by calling the
method :func:`~Trace.zero`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'zero'`` is returned.

  >>> Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5]).zero()
  Trace(label='Signal:zero', samples=[0, 1, 1, 1, 0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5])
  trace = signal.zero()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _positives:

Positives
---------

You can check each signal *sample* is positive or not by calling the
method :func:`~Trace.positive`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'positive'`` is returned.

  >>> Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5]).positive()
  Trace(label='Signal:positive', samples=[0, 0, 0, 0, 1])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5])
  trace = signal.positive()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _negatives:

Negatives
---------

You can check each signal *sample* is negative or not by calling the
method :func:`~Trace.negative`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'negative'`` is returned.

  >>> Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5]).negative()
  Trace(label='Signal:negative', samples=[1, 0, 0, 0, 0])

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [-0.5, -0.0, 0, +0.0, 0.5])
  trace = signal.negative()
  go.Figure([signal.plot(), trace.digital.plot(mode='lines+markers')])


.. _min:

Min
---

You can get the *minimum* of each signal *sample* and the corresponding *element*
in other :class:`Trace`'s or ``Iterables``, or an :class:`int` or :class:`float`
*numbers* by calling the method :meth:`~Trace.min`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'min'`` is returned.

  >>> # minimum of samples
  >>> Trace('Signal1', [1, -2, 3]).min(Trace('Signal2', [-1, 2, -3]))
  Trace(label='Signal1:min', samples=[-1, -2, -3])

  >>> # minimum of samples and iterables
  >>> Trace('Signal', [1, -2, 3]).min([-1, 2, -3])
  Trace(label='Signal:min', samples=[-1, -2, -3])

  >>> # minimum of samples and numbers
  >>> Trace('Signal', [1, 2, 3]).min(2)
  Trace(label='Signal:min', samples=[1, 2, 2])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, -2, 3])
  signal2 = Trace('Signal2', [-1, 2, -3])
  trace = signal1.min(signal2)
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


.. _max:

Max
---

You can get the *maximum* of each signal *sample* and the corresponding *element*
in other :class:`Trace`'s or ``Iterables``, or an :class:`int` or :class:`float`
*numbers* by calling the method :meth:`~Trace.max`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'max'`` is returned.

  >>> # maximum of samples
  >>> Trace('Signal1', [1, -2, 3]).max(Trace('Signal2', [-1, 2, -3]))
  Trace(label='Signal1:max', samples=[1, 2, 3])

  >>> # maximum of samples and iterables
  >>> Trace('Signal', [1, -2, 3]).max([-1, 2, -3])
  Trace(label='Signal:max', samples=[1, 2, 3])

  >>> # maximum of samples and numbers
  >>> Trace('Signal', [1, 2, 3]).max(2)
  Trace(label='Signal:max', samples=[2, 2, 3])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, -2, 3])
  signal2 = Trace('Signal2', [-1, 2, -3])
  trace = signal1.max(signal2)
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


.. _average:

Average
-------

You can get the *average* of each signal *sample* and the corresponding *element*
in other :class:`Trace`'s or ``Iterables``, or an :class:`int` or :class:`float`
*numbers* by calling the method :meth:`~Trace.average`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'avg'`` is returned.

  >>> # average of samples
  >>> Trace('Signal1', [1, -2, 3]).average(Trace('Signal2', [-1, 2, -3]))
  Trace(label='Signal1:avg', samples=[0.0, 0.0, 0.0])

  >>> # average of samples and iterables
  >>> Trace('Signal', [1, -2, 3]).average([-1, 2, -3])
  Trace(label='Signal:avg', samples=[0.0, 0.0, 0.0])

  >>> # maximum of samples and numbers
  >>> Trace('Signal', [1, -2, 3]).average(2)
  Trace(label='Signal:avg', samples=[1.5, 0.0, 2.5])

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, -2, 3])
  signal2 = Trace('Signal2', [-1, 2, -3])
  trace = signal1.average(signal2)
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])
