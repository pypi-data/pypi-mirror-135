.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _slew-rate limiting:

Slew-Rate Limiting
==================

The signal :attr:`~Trace.samples` of a :ref:`signal trace <signal trace>` can be
processed with a linear `slew-rate limiting`_ algorithm.

Limiting Slew-Rates
-------------------

You can limit the *positive* and *negative* slew-rate of the signal
:attr:`~Trace.samples` by calling the method :meth:`~Trace.ramp`, and providing
the maximal allowed *positive* and *negative* delta limits between consecutive
:attr:`~Trace.samples`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ramp'`` is returned.

  >>> # slew-rate of the signal samples limited by numbers
  >>> Trace('Signal', [-1, 1, 1, 1, 1, -1, -1, -1, -1]).ramp(limits=(0.5, -0.5))
  Trace(label='Signal:ramp', samples=[-1, -0.5, 0.0, 0.5, 1, 0.5, 0.0, -0.5, -1])

  >>> # slew-rate of the signal samples limited by traces
  >>> Trace('Signal', [0, 1, -1, 1, -1, 1, -1, 1, 0]).ramp(
  ...   limits=(Trace('Positive Limit',
  ...                  [0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 0]),
  ...           Trace('Negative Limit',
  ...                  [0, 0, -1.0, -1.0, -0.75, -0.75, -0.5, -0.5, -0.25])))
  Trace(label='Signal:ramp', samples=[0, 0.25, -0.75, -0.25, -1, -0.25, -0.75, 0.25, 0])

  >>> # slew-rate of the signal samples limited by iterables
  >>> Trace('Signal', [0, 1, -1, 1, -1, 1, -1, 1, 0]).ramp(
  ...   limits=(
  ...     [0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 0],
  ...     [0, 0, -1.0, -1.0, -0.75, -0.75, -0.5, -0.5, -0.25]))
  Trace(label='Signal:ramp', samples=[0, 0.25, -0.75, -0.25, -1, -0.25, -0.75, 0.25, 0])

.. note:: An *iterable* limit should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 1, 1, 1, 1, -1, -1, -1, -1])
  trace = signal.ramp(limits=(0.5, -0.5))
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()


Limiting Positive Slew-Rate
---------------------------

You can limit the *positive* slew-rate of the signal :attr:`~Trace.samples` by
calling the method :meth:`~Trace.ramp`, and providing the maximal allowed
*positive* delta limits between consecutive :attr:`~Trace.samples`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ramp'`` is returned.

  >>> # positive slew-rate of the signal samples limited by a number
  >>> Trace('Signal', [0, -1, 1, 1, 1, 1, 1, 0, -1]).ramp(limits=(0.5, None))
  Trace(label='Signal:ramp', samples=[0, -1, -0.5, 0.0, 0.5, 1, 1, 0, -1])

  >>> # positive slew-rate of the signal samples limited by a trace
  >>> Trace('Signal', [0, -1, 1, 1, 1, 1, 1, 0, -1]).ramp(
  ...   limits=(Trace('Positive Limit',
  ...                 [0, 0, 0.25, 0.5, 0, 0.75, 0.5, 0, 0]), None))
  Trace(label='Signal:ramp', samples=[0, -1, -0.75, -0.25, -0.25, 0.5, 1, 0, -1])

  >>> # positive slew-rate of the signal samples limited by an iterable
  >>> Trace('Signal', [0, -1, 1, 1, 1, 1, 1, 0, -1]).ramp(
  ...   limits=([0, 0, 0.25, 0.5, 0, 0.75, 0.5, 0, 0], None))
  Trace(label='Signal:ramp', samples=[0, -1, -0.75, -0.25, -0.25, 0.5, 1, 0, -1])

.. note:: An *iterable* limit should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, -1, 1, 1, 1, 1, 1, 0, -1])
  trace = signal.ramp(limits=(0.5, None))
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()

Limiting Negative Slew-Rate
---------------------------

You can limit the *negative* slew-rate of the signal :attr:`~Trace.samples` by
calling the method :meth:`~Trace.ramp`, and providing the maximal allowed
*negative* delta limits between consecutive :attr:`~Trace.samples`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ramp'`` is returned.

  >>> # negative slew-rate of the signal samples limited by a number
  >>> Trace('Signal', [0, 1, -1, -1, -1, -1, -1, 0, 1]).ramp(limits=(None, -0.5))
  Trace(label='Signal:ramp', samples=[0, 1, 0.5, 0.0, -0.5, -1, -1, 0, 1])

  >>> # negative slew-rate of the signal samples limited by a trace
  >>> Trace('Signal', [0, 1, -1, -1, -1, -1, -1, 0, 1]).ramp(
  ...   limits=(None, Trace('Negative Limit',
  ...                       [0, 0, -0.25, -0.5, 0, -0.75, -0.5, 0, 0])))
  Trace(label='Signal:ramp', samples=[0, 1, 0.75, 0.25, 0.25, -0.5, -1, 0, 1])

  >>> # negative slew-rate of the signal samples limited by an iterable
  >>> Trace('Signal', [0, 1, -1, -1, -1, -1, -1, 0, 1]).ramp(
  ...   limits=(None, [0, 0, -0.25, -0.5, 0, -0.75, -0.5, 0, 0]))
  Trace(label='Signal:ramp', samples=[0, 1, 0.75, 0.25, 0.25, -0.5, -1, 0, 1])

.. note:: An *iterable* limit should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [0, 1, -1, -1, -1, -1, -1, 0, 1])
  trace = signal.ramp((None, -0.5))
  fig = go.Figure([signal.digital.plot(),
                   trace.plot(mode='lines+markers')])
  fig.show()
