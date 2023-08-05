.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Comparison Operators
====================

.. _lesser:

Samples Lesser Than
-------------------

You can compare each signal *sample* to be less than the corresponding *element*
in another :class:`Trace` or ``Iterable``, or to an :class:`int` or :class:`float`
*number* with the ``<`` operator or by calling the method :meth:`~Trace.less`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'lt'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) < Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:lt', samples=[1, 1, 0, 0, 0])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).less(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:lt', samples=[1, 1, 0, 0, 0])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) < [3, 3, 3, 3, 3]
  Trace(label='Signal:lt', samples=[1, 1, 0, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).less([3, 3, 3, 3, 3])
  Trace(label='Signal:lt', samples=[1, 1, 0, 0, 0])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) < 3
  Trace(label='Signal:lt', samples=[1, 1, 0, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).less(3)
  Trace(label='Signal:lt', samples=[1, 1, 0, 0, 0])


.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) < 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))


.. _lesser or equal:

Samples Less Than or Equal to
-----------------------------

You can compare each signal *sample* to be less than or equal to the corresponding
*element* in another :class:`Trace` or ``Iterable``, or to an :class:`int` or
:class:`float` *number* with the ``<=`` operator or by calling the method
:meth:`~Trace.less_equal`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'le'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) <= Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:le', samples=[1, 1, 1, 0, 0])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).less_equal(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:le', samples=[1, 1, 1, 0, 0])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) <= [3, 3, 3, 3, 3]
  Trace(label='Signal:le', samples=[1, 1, 1, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).less_equal([3, 3, 3, 3, 3])
  Trace(label='Signal:le', samples=[1, 1, 1, 0, 0])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) <= 3
  Trace(label='Signal:le', samples=[1, 1, 1, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).less_equal(3)
  Trace(label='Signal:le', samples=[1, 1, 1, 0, 0])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) <= 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))


.. _equal:

Samples Equal to
----------------

You can compare each signal *sample* to be equal to the corresponding *element*
in another :class:`Trace` or ``Iterable``, or to an :class:`int` or :class:`float`
*number* with the ``==`` operator or by calling the method :meth:`~Trace.equal`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'eq'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) == Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:eq', samples=[0, 0, 1, 0, 0])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).equal(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:eq', samples=[0, 0, 1, 0, 0])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) == [3, 3, 3, 3, 3]
  Trace(label='Signal:eq', samples=[0, 0, 1, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).equal([3, 3, 3, 3, 3])
  Trace(label='Signal:eq', samples=[0, 0, 1, 0, 0])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) == 3
  Trace(label='Signal:eq', samples=[0, 0, 1, 0, 0])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).equal(3)
  Trace(label='Signal:eq', samples=[0, 0, 1, 0, 0])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) == 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))


.. _not equal:

Samples Not Equal to
--------------------

You can compare each signal *sample* to be not equal to the corresponding *element*
in another :class:`Trace` or ``Iterable``, or to an :class:`int` or :class:`float`
*number* with the ``!=`` operator or by calling the method :meth:`~Trace.not_equal`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ne'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) != Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:ne', samples=[1, 1, 0, 1, 1])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).not_equal(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:ne', samples=[1, 1, 0, 1, 1])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) != [3, 3, 3, 3, 3]
  Trace(label='Signal:ne', samples=[1, 1, 0, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).not_equal([3, 3, 3, 3, 3])
  Trace(label='Signal:ne', samples=[1, 1, 0, 1, 1])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) != 3
  Trace(label='Signal:ne', samples=[1, 1, 0, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).not_equal(3)
  Trace(label='Signal:ne', samples=[1, 1, 0, 1, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) != 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))


.. _greater or equal:

Samples Greater or Equal to
---------------------------

You can compare each signal *sample* to be greater than or equal to the corresponding
*element* in another :class:`Trace` or ``Iterable``, or to an :class:`int` or
:class:`float` *number* with the ``>=`` operator or by calling the method
:meth:`~Trace.greater_equal`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'ge'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) >= Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:ge', samples=[0, 0, 1, 1, 1])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).greater_equal(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:ge', samples=[0, 0, 1, 1, 1])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) >= [3, 3, 3, 3, 3]
  Trace(label='Signal:ge', samples=[0, 0, 1, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).greater_equal([3, 3, 3, 3, 3])
  Trace(label='Signal:ge', samples=[0, 0, 1, 1, 1])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) >= 3
  Trace(label='Signal:ge', samples=[0, 0, 1, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).greater_equal(3)
  Trace(label='Signal:ge', samples=[0, 0, 1, 1, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) >= 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))


.. _greater:

Samples Greater Than
--------------------

You can compare each signal *sample* to be greater than the corresponding *element*
in another :class:`Trace` or ``Iterable``, or to an :class:`int` or :class:`float`
*number* with the ``>`` operator or by calling the method :meth:`~Trace.greater`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'gt'`` is returned.

  >>> # compare trace samples
  >>> Trace('Signal1', [1, 2, 3, 4, 5]) > Trace('Signal2', [3, 3, 3, 3, 3])
  Trace(label='Signal1:gt', samples=[0, 0, 0, 1, 1])
  >>> Trace('Signal1', [1, 2, 3, 4, 5]).greater(Trace('Signal2', [3, 3, 3, 3, 3]))
  Trace(label='Signal1:gt', samples=[0, 0, 0, 1, 1])

  >>> # compare trace samples with iterable items
  >>> Trace('Signal', [1, 2, 3, 4, 5]) > [3, 3, 3, 3, 3]
  Trace(label='Signal:gt', samples=[0, 0, 0, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).greater([3, 3, 3, 3, 3])
  Trace(label='Signal:gt', samples=[0, 0, 0, 1, 1])

  >>> # compare trace samples with a number
  >>> Trace('Signal', [1, 2, 3, 4, 5]) > 3
  Trace(label='Signal:gt', samples=[0, 0, 0, 1, 1])
  >>> Trace('Signal', [1, 2, 3, 4, 5]).greater(3)
  Trace(label='Signal:gt', samples=[0, 0, 0, 1, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the samples is returned!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3, 4, 5]) > 3
  go.Figure(trace.digital.plot(mode='lines+markers', fill='tozeroy'))
