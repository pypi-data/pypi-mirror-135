.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Arithmetic Operators
====================

.. _addition:

Addition
--------

You can add to each signal *sample* the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*
with the ``+`` operator or by calling the method :meth:`~Trace.add`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'add'`` or ``'radd'`` is returned.

  >>> # add a trace to the samples
  >>> Trace('Signal1', [1, 2, 3]) + Trace('Signal2', [-2, -3, -4])
  Trace(label='Signal1:add', samples=[-1, -1, -1])
  >>> Trace('Signal1', [1, 2, 3]).add(Trace('Signal2', [-2, -3, -4]))
  Trace(label='Signal1:add', samples=[-1, -1, -1])

  >>> # add an iterable to the samples
  >>> Trace('Signal', [1, 2, 3]) + [-2, -3, -4]
  Trace(label='Signal:add', samples=[-1, -1, -1])
  >>> Trace('Signal', [1, 2, 3]).add([-2, -3, -4])
  Trace(label='Signal:add', samples=[-1, -1, -1])
  >>> # add to an iterable the samples
  >>> [1, 2, 3] + Trace('Signal', [-2, -3, -4])
  Trace(label='Signal:radd', samples=[-1, -1, -1])

  >>> # add a number to the samples
  >>> Trace('Signal', [1, 2, 3]) + 1
  Trace(label='Signal:add', samples=[2, 3, 4])
  >>> Trace('Signal', [1, 2, 3]).add(1)
  Trace(label='Signal:add', samples=[2, 3, 4])
  >>> # add to a number the samples
  >>> 1 + Trace('Signal', [1, 2, 3])
  Trace(label='Signal:radd', samples=[2, 3, 4])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, 2, 3])
  signal2 = Trace('Signal2', [-2, -3, -4])
  trace = signal1 + signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


.. _subtraction:

Subtraction
-----------

You can subtract from each signal *sample* the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*
with the ``-`` operator or by calling the method :meth:`~Trace.sub`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sub'`` is returned.

  >>> # subtract a trace from the samples
  >>> Trace('Signal1', [1, 2, 3]) - Trace('Signal2', [2, 3, 4])
  Trace(label='Signal1:sub', samples=[-1, -1, -1])
  >>> Trace('Signal1', [1, 2, 3]).sub(Trace('Signal2', [2, 3, 4]))
  Trace(label='Signal1:sub', samples=[-1, -1, -1])

  >>> # subtract an iterable from the samples
  >>> Trace('Signal', [1, 2, 3]) - [2, 3, 4]
  Trace(label='Signal:sub', samples=[-1, -1, -1])
  >>> Trace('Signal', [1, 2, 3]).sub([2, 3, 4])
  Trace(label='Signal:sub', samples=[-1, -1, -1])

  >>> # subtract a number from the samples
  >>> Trace('Signal', [1, 2, 3]) - 1
  Trace(label='Signal:sub', samples=[0, 1, 2])
  >>> Trace('Signal', [1, 2, 3]).sub(1)
  Trace(label='Signal:sub', samples=[0, 1, 2])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, 2, 3])
  signal2 = Trace('Signal2', [2, 3, 4])
  trace = signal1 - signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


You can subtract each signal *sample* from the corresponding *element* in an
``Iterable``, or an :class:`int` or :class:`float` *number* with the ``-``
operator.


A new :class:`Trace` instance *labeled* with the performed transformation
``'rsub'`` is returned.

  >>> # subtract from an iterable the samples
  >>> [1, 2, 3] - Trace('Signal', [2, 3, 4])
  Trace(label='Signal:rsub', samples=[-1, -1, -1])

  >>> # subtract from a number the samples
  >>> 1 - Trace('Signal', [1, 2, 3])
  Trace(label='Signal:rsub', samples=[0, -1, -2])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [1, 2, 3])
  trace = 1 - signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

.. _multiplication:

Multiplication
--------------

You can multiply each signal *sample* with the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*
with the ``*`` operator or by calling the method :meth:`~Trace.mul`.


A new :class:`Trace` instance *labeled* with the performed transformation
``'mul'`` or ``'rmul'`` is returned.

  >>> # multiply the samples with a trace
  >>> Trace('Signal1', [1, 2, 3]) * Trace('Signal2', [2, 3, 4])
  Trace(label='Signal1:mul', samples=[2, 6, 12])
  >>> Trace('Signal1', [1, 2, 3]).mul(Trace('Signal2', [2, 3, 4]))
  Trace(label='Signal1:mul', samples=[2, 6, 12])

  >>> # multiply the samples with an iterable
  >>> Trace('Signal', [1, 2, 3]) * [2, 3, 4]
  Trace(label='Signal:mul', samples=[2, 6, 12])
  >>> Trace('Signal', [1, 2, 3]).mul([2, 3, 4])
  Trace(label='Signal:mul', samples=[2, 6, 12])
  >>> # multiply an iterable with the samples
  >>> [1, 2, 3] * Trace('Signal', [2, 3, 4])
  Trace(label='Signal:rmul', samples=[2, 6, 12])

  >>> # multiply the samples with a number
  >>> Trace('Signal', [1, 2, 3]) * 2
  Trace(label='Signal:mul', samples=[2, 4, 6])
  >>> Trace('Signal', [1, 2, 3]).mul(2)
  Trace(label='Signal:mul', samples=[2, 4, 6])
  >>> # multiply a number with the samples
  >>> 2 * Trace('Signal', [1, 2, 3])
  Trace(label='Signal:rmul', samples=[2, 4, 6])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, 2, 3])
  signal2 = Trace('Signal2', [2, 3, 4])
  trace = signal1 * signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


.. _division:

Division
--------

You can divide each signal *sample* by the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*
with the ``/`` operator or by calling the method :meth:`~Trace.div`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'div'`` is returned.

  >>> # divided the samples by a trace
  >>> Trace('Signal1', [3, 6, 9]) / Trace('Signal2', [2, 4, 6])
  Trace(label='Signal1:div', samples=[1.5, 1.5, 1.5])
  >>> Trace('Signal1', [3, 6, 9]).div(Trace('Signal2', [2, 4, 6]))
  Trace(label='Signal1:div', samples=[1.5, 1.5, 1.5])

  >>> # divide the samples by an iterable
  >>> Trace('Signal', [3, 6, 9]) / [2, 4, 6]
  Trace(label='Signal:div', samples=[1.5, 1.5, 1.5])
  >>> Trace('Signal', [3, 6, 9]).div([2, 4, 6])
  Trace(label='Signal:div', samples=[1.5, 1.5, 1.5])

  >>> # divide the samples by a number
  >>> Trace('Signal', [3, 6, 9]) / 2
  Trace(label='Signal:div', samples=[1.5, 3.0, 4.5])
  >>> Trace('Signal', [3, 6, 9]).div(2)
  Trace(label='Signal:div', samples=[1.5, 3.0, 4.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [3, 6, 9])
  signal2 = Trace('Signal2', [2, 4, 6])
  trace = signal1 / signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


You can divide the corresponding *element* in an ``Iterable``, or an :class:`int`
or :class:`float` *number* by each signal *sample* with the ``/`` operator.

A new :class:`Trace` instance *labeled* with the performed transformation
``'rdiv'`` is returned.

  >>> # divide an iterable by the samples
  >>> [3, 6, 9] / Trace('Signal', [2, 4, 6])
  Trace(label='Signal:rdiv', samples=[1.5, 1.5, 1.5])

  >>> # divide a number by the samples
  >>> 4.5 / Trace('Signal', [3, 6, 9])
  Trace(label='Signal:rdiv', samples=[1.5, 0.75, 0.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [3, 6, 9])
  trace = 4.5 / signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _floor division:

Floor Division
--------------

You can integer divide each signal *sample* by the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``//`` operator or by calling the method:meth:`~Trace.floordiv`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'floordiv'`` is returned.

  >>> # integer divide the samples by a trace
  >>> Trace('Signal1', [3, 6, 9]) // Trace('Signal2', [2, 4, 6])
  Trace(label='Signal1:floordiv', samples=[1, 1, 1])
  >>> Trace('Signal1', [3, 6, 9]).floordiv(Trace('Signal2', [2, 4, 6]))
  Trace(label='Signal1:floordiv', samples=[1, 1, 1])

  >>> # integer divide the samples by an iterable
  >>> Trace('Signal', [3, 6, 9]) // [2, 4, 6]
  Trace(label='Signal:floordiv', samples=[1, 1, 1])
  >>> Trace('Signal', [3, 6, 9]).floordiv([2, 4, 6])
  Trace(label='Signal:floordiv', samples=[1, 1, 1])

  >>> # integer divide the samples by a number
  >>> Trace('Signal', [3, 6, 9]) // 2
  Trace(label='Signal:floordiv', samples=[1, 3, 4])
  >>> Trace('Signal', [3, 6, 9]).floordiv(2)
  Trace(label='Signal:floordiv', samples=[1, 3, 4])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [3, 6, 9])
  signal2 = Trace('Signal2', [2, 4, 6])
  trace = signal1 // signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


You can integer divide the corresponding *element* in an ``Iterable``, or an
:class:`int` or :class:`float` *number* by each signal *sample* with the ``//``
operator.

A new :class:`Trace` instance *labeled* with the performed transformation
``'rfloordiv'`` is returned.

  >>> # integer divide an iterable by the samples
  >>> [3, 6, 9] // Trace('Signal', [2, 4, 6])
  Trace(label='Signal:rfloordiv', samples=[1, 1, 1])

  >>> # integer divide a number by the samples
  >>> 4.5 // Trace('Signal', [3, 6, 9])
  Trace(label='Signal:rfloordiv', samples=[1.0, 0.0, 0.0])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [3, 6, 9])
  trace = 4.5 // signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _modulo:

Modulo
------

You can modulo divide each signal *sample* by the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``%`` operator or by calling the method:meth:`~Trace.mod`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'mod'`` is returned.

  >>> # modulo divide the samples by a trace
  >>> Trace('Signal1', [-3, 6, 9.5]) % Trace('Signal2', [2, 4, -6])
  Trace(label='Signal1:mod', samples=[1, 2, -2.5])
  >>> Trace('Signal1', [-3, 6, 9.5]).mod(Trace('Signal2', [2, 4, -6]))
  Trace(label='Signal1:mod', samples=[1, 2, -2.5])

  >>> # modulo divide the samples by an iterable
  >>> Trace('Signal', [-3, 6, 9.5]) % [2, 4, -6]
  Trace(label='Signal:mod', samples=[1, 2, -2.5])
  >>> Trace('Signal', [-3, 6, 9.5]).mod([2, 4, -6])
  Trace(label='Signal:mod', samples=[1, 2, -2.5])

  >>> # modulo divide the samples by a number
  >>> Trace('Signal', [-3, 6, 9.5]) % 2
  Trace(label='Signal:mod', samples=[1, 0, 1.5])
  >>> Trace('Signal', [-3, 6, 9.5]).mod(2)
  Trace(label='Signal:mod', samples=[1, 0, 1.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-3, 6, 9.5])
  signal2 = Trace('Signal2', [2, 4, -6])
  trace = signal1 % signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


You can modulo divide the corresponding *element* in an ``Iterable``, or an
:class:`int` or :class:`float` *number* by each signal *sample* with the ``%``
operator.

A new :class:`Trace` instance *labeled* with the performed transformation
``'rmod'`` is returned.

  >>> # modulo divide an iterable by the samples
  >>> [3, 6, 9] % Trace('Signal', [2, 4, 6])
  Trace(label='Signal:rmod', samples=[1, 2, 3])

  >>> # modulo divide a number by the samples
  >>> 4.5 % Trace('Signal', [3, 6, 9])
  Trace(label='Signal:rmod', samples=[1.5, 4.5, 4.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [3, 6, 9])
  trace = 4.5 % signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _exponentiation:

Exponentiation
--------------

You can raise each signal *sample* to the power of the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``**`` operator or by calling the method :meth:`~Trace.pow`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'pow'`` is returned.

  >>> # raise the samples to the power of a trace
  >>> Trace('Signal1', [1, 0, -1]) ** Trace('Signal2', [-2, 0, 2])
  Trace(label='Signal1:pow', samples=[1.0, 1, 1])
  >>> Trace('Signal1', [1, 0, -1]).pow(Trace('Signal2', [-2, 0, 2]))
  Trace(label='Signal1:pow', samples=[1.0, 1, 1])

  >>> # raise the samples to the power of an iterable
  >>> Trace('Signal', [1, 0, -1]) ** [-2, 0, 2]
  Trace(label='Signal:pow', samples=[1.0, 1, 1])
  >>> Trace('Signal', [1, 0, -1]).pow([-2, 0, 2])
  Trace(label='Signal:pow', samples=[1.0, 1, 1])

  >>> # raise the samples to the power of a number
  >>> Trace('Signal', [1, 0, 1]) ** 2
  Trace(label='Signal:pow', samples=[1, 0, 1])
  >>> Trace('Signal', [1, 0, 1]).pow(2)
  Trace(label='Signal:pow', samples=[1, 0, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [1, 0, -1])
  signal2 = Trace('Signal2', [-2, 0, 2])
  trace = signal1 ** signal2
  go.Figure([signal1.plot(), signal2.plot(), trace.plot(mode='lines+markers')])


You can raise the corresponding *element* in an ``Iterable``, or an :class:`int`
or :class:`float` *number* to the power of each signal *sample* with the ``**``
operator.

A new :class:`Trace` instance *labeled* with the performed transformation
``'rpow'`` is returned.

  >>> # raise an iterable to the power of the samples
  >>> [1, 0, -1] ** Trace('Signal', [-2, 0, 2])
  Trace(label='Signal:rpow', samples=[1.0, 1, 1])

  >>> # raise a number to the power of the samples
  >>> (-1) ** Trace('Signal', [-2, 0, 2])
  Trace(label='Signal:rpow', samples=[1.0, 1, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-2, 0, 2])
  trace = (-1) ** signal
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])
