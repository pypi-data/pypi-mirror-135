.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _clip:

Clipping
========

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
clipped by another set of :attr:`~Trace.samples` or a number at a *lower* and/or
*upper* bound.

Lower Bound Clipping
--------------------

You can hard clip each signal *sample* at the corresponding *element* in another
:class:`Trace` or ``Iterable``, or at an :class:`int` or :class:`float` *number*
assigned as lower bound for the signal :attr:`~Trace.samples` by calling the
method :meth:`~Trace.clip`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'clip'`` is returned.

  >>> # clip samples at lower bound trace samples
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(
  ... lower=Trace('Lower', [1, 0, 0, 0, -1]))
  Trace(label='Signal:clip', samples=[1, 0, 0, 0.5, 1.5])

  >>> # clip samples at lower bound iterable items
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(lower=[1, 0, 0, 0, -1])
  Trace(label='Signal:clip', samples=[1, 0, 0, 0.5, 1.5])

  >>> # clip samples at lower bound number
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(0)
  Trace(label='Signal:clip', samples=[0, 0, 0, 0.5, 1.5])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(lower=0)
  Trace(label='Signal:clip', samples=[0, 0, 0, 0.5, 1.5])

.. note:: An *iterable* bound should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

Upper Bound Clipping
--------------------

You can hard clip each signal *sample* at the corresponding *element* in another
:class:`Trace` or ``Iterable``, or at an :class:`int` or :class:`float` *number*
assigned as upper bound for the signal :attr:`~Trace.samples` by calling the
method :meth:`~Trace.clip`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'clip'`` is returned.

  >>> # clip samples at upper bound trace samples
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(
  ... upper=Trace('Upper', [1, 0, 0, 0, -1]))
  Trace(label='Signal:clip', samples=[-1.5, -0.5, 0, 0, -1])

  >>> # clip samples at upper bound iterable items
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(upper=[1, 0, 0, 0, -1])
  Trace(label='Signal:clip', samples=[-1.5, -0.5, 0, 0, -1])

  >>> # clip samples at upper bound number
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(upper=0)
  Trace(label='Signal:clip', samples=[-1.5, -0.5, 0, 0, 0])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(None, 0)
  Trace(label='Signal:clip', samples=[-1.5, -0.5, 0, 0, 0])

.. note:: An *iterable* bound should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!


Lower & Upper Bound Clipping
----------------------------

You can hard clip each signal *sample* at the corresponding *element* in another
:class:`Trace` or ``Iterable``, or at an :class:`int` or :class:`float` *number*
assigned as lower bound or upper bound for the signal :attr:`~Trace.samples` by
calling the method :meth:`~Trace.clip`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'clip'`` is returned.


  >>> # clip samples at lower & upper bound trace samples
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(
  ... lower=Trace('Lower', [-1, 0, 0.5, 0, -1]),
  ... upper=Trace('Upper', [1, 0, -0.5, 0, 1]))
  Trace(label='Signal:clip', samples=[-1, 0, -0.5, 0, 1])

  >>> # clip samples at lower & upper bound iterable items
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(
  ... lower=[-1, 0, 0,5, 0, -1],
  ... upper=[1, 0, -0.5, 0, 1])
  Trace(label='Signal:clip', samples=[-1, 0, -0.5, 0, 1])

  >>> # clip samples at lower & upper bound numbers
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(-0.5, 1.0)
  Trace(label='Signal:clip', samples=[-0.5, -0.5, 0, 0.5, 1.0])
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clip(lower=-0.5, upper=1.0)
  Trace(label='Signal:clip', samples=[-0.5, -0.5, 0, 0.5, 1.0])

.. note:: The *upper* bound is dominant over the *lower* bound.

.. note:: An *iterable* bound should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = signal.clip(-0.5, 1.0)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _clamp:

Symmetrically Clamping
----------------------

You can symmetrically clamp each signal *sample* at the corresponding *element*
in another :class:`Trace` or ``Iterable``, or at an :class:`int` or :class:`float`
*number* by calling the method :meth:`~Trace.clamp`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'clamp'`` is returned.

  >>> # clip samples at trace samples
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clamp(
  ... Trace('Bound', [1, 0, 0, 0, -1]))
  Trace(label='Signal:clamp', samples=[-1, 0, 0, 0, 1])

  >>> # clip samples at iterable items
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clamp([1, 0, 0, 0, -1])
  Trace(label='Signal:clamp', samples=[-1, 0, 0, 0, 1])

  >>> # clip samples at number
  >>> Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5]).clamp(-1.0)
  Trace(label='Signal:clamp', samples=[-1.0, -0.5, 0, 0.5, 1.0])

.. note:: An *iterable* bound should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1.5, -0.5, 0, 0.5, 1.5])
  trace = signal.clamp(-1.0)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])
