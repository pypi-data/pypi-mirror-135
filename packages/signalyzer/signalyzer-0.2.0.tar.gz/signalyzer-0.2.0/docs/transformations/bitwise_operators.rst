.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Bitwise Operators
=================

.. _bitwise AND:

Bitwise AND
-----------

.. important:: The two operands are converted to :class:`int` before the
  operation is performed.

You can bitwise AND each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``&`` operator or by calling the method
:meth:`~Trace.bitwise_and`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'and'`` or ``'rand'`` is returned.

  >>> # bitwise AND the samples with a trace
  >>> Trace('Signal1', [-1, 0, 1]) & Trace('Signal2', [0xff, 0xff, 0xff])
  Trace(label='Signal1:and', samples=[255, 0, 1])
  >>> Trace('Signal1', [-1, 0, 1]).bitwise_and(Trace('Signal2', [0xff, 0xff, 0xff]))
  Trace(label='Signal1:and', samples=[255, 0, 1])

  >>> # bitwise AND the samples with an iterable
  >>> Trace('Signal', [-1, 0, 1]) & [0xff, 0xff, 0xff]
  Trace(label='Signal:and', samples=[255, 0, 1])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_and([0xff, 0xff, 0xff])
  Trace(label='Signal:and', samples=[255, 0, 1])
  >>> # bitwise AND an iterable with the samples
  >>> [0xff, 0xff, 0xff] & Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:rand', samples=[255, 0, 1])

  >>> # bitwise AND the samples with a number
  >>> Trace('Signal', [-1, 0, 1]) & 0xff
  Trace(label='Signal:and', samples=[255, 0, 1])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_and(0xff)
  Trace(label='Signal:and', samples=[255, 0, 1])
  >>> # bitwise AND a number with the samples
  >>> 0xff & Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:rand', samples=[255, 0, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-1, 0, 1])
  signal2 = Trace('Signal2', [0xff, 0xff, 0xff])
  trace = signal1 & signal2
  fig = go.Figure([signal1.digital.plot(),
                   signal2.digital.plot(),
                   trace.digital.plot(mode='lines+markers')])
  fig.show()

.. _bitwise OR:

Bitwise OR
----------

.. important:: The two operands are converted to :class:`int` before the
  operation is performed.

You can bitwise OR each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``|`` operator or by calling the method
:meth:`~Trace.bitwise_or`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'or'`` or ``'ror'`` is returned.

  >>> # bitwise OR the samples with a trace
  >>> Trace('Signal1', [-1, 0, 1]) | Trace('Signal2', [0x0, 0xff, 0xfe])
  Trace(label='Signal1:or', samples=[-1, 255, 255])
  >>> Trace('Signal1', [-1, 0, 1]).bitwise_or(Trace('Signal2', [0x0, 0xff, 0xfe]))
  Trace(label='Signal1:or', samples=[-1, 255, 255])

  >>> # bitwise OR the samples with an iterable
  >>> Trace('Signal', [-1, 0, 1]) | [0x0, 0xff, 0xfe]
  Trace(label='Signal:or', samples=[-1, 255, 255])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_or([0x0, 0xff, 0xfe])
  Trace(label='Signal:or', samples=[-1, 255, 255])
  >>> # bitwise OR an iterable with the samples
  >>> [0x0, 0xff, 0xfe] | Trace('Signal', [-1, 0, 1])
   Trace(label='Signal:ror', samples=[-1, 255, 255])

  >>> # bitwise OR the samples with a number
  >>> Trace('Signal', [-1, 0, 1]) | 0xfe
  Trace(label='Signal:or', samples=[-1, 254, 255])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_or(0xfe)
  Trace(label='Signal:or', samples=[-1, 254, 255])
  >>> # bitwise OR a number with the samples
  >>> 0xfe | Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:ror', samples=[-1, 254, 255])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-1, 0, 1])
  signal2 = Trace('Signal2', [0x0, 0xff, 0xfe])
  trace = signal1 | signal2
  fig = go.Figure([signal1.digital.plot(),
                   signal2.digital.plot(),
                   trace.digital.plot(mode='lines+markers')])
  fig.show()

.. _bitwise XOR:

Bitwise XOR
-----------

.. important:: The two operands are converted to :class:`int` before the
  operation is performed.

You can bitwise XOR each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* with the ``^`` operator or by calling the method
:meth:`~Trace.bitwise_xor`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'xor'`` or ``'rxor'`` is returned.

  >>> # bitwise XOR the samples with a trace
  >>> Trace('Signal1', [-1, 0, 1]) ^ Trace('Signal2', [0xfe, 0x1, 0x1])
  Trace(label='Signal1:xor', samples=[-255, 1, 0])
  >>> Trace('Signal1', [-1, 0, 1]).bitwise_xor(Trace('Signal2', [0xfe, 0x1, 0x1]))
  Trace(label='Signal1:xor', samples=[-255, 1, 0])

  >>> # bitwise XOR the samples with an iterable
  >>> Trace('Signal', [-1, 0, 1]) ^ [0xfe, 0x1, 0x1]
  Trace(label='Signal:xor', samples=[-255, 1, 0])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_xor([0xfe, 0x1, 0x1])
  Trace(label='Signal:xor', samples=[-255, 1, 0])
  >>> # bitwise XOR an iterable with the samples
  >>> [0xfe, 0x1, 0x1] ^ Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:rxor', samples=[-255, 1, 0])

  >>> # bitwise XOR the samples with a number
  >>> Trace('Signal', [-1, 0, 1]) ^ 0xfe
  Trace(label='Signal:xor', samples=[-255, 254, 255])
  >>> Trace('Signal', [-1, 0, 1]).bitwise_xor(0xfe)
  Trace(label='Signal:xor', samples=[-255, 254, 255])
  >>> # bitwise XOR a number with the samples
  >>> 0xfe ^ Trace('Signal', [-1, 0, 1])
  Trace(label='Signal:rxor', samples=[-255, 254, 255])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-1, 0, 1])
  signal2 = Trace('Signal2', [0xfe, 0x1, 0x1])
  trace = signal1 ^ signal2
  fig = go.Figure([signal1.digital.plot(),
                   signal2.digital.plot(),
                   trace.digital.plot(mode='lines+markers')])
  fig.show()

.. _bitwise NOT:

Bitwise NOT
-----------

.. important:: The each signal *sample* is converted to :class:`int` before the
  operation is performed.

You can bitwise invert each signal *sample* with the ``'~'`` operator or by
calling the method :meth:`~Trace.invert`.

A new :class:`Trace` instance *labeled* with the performed transformation
``not`` is returned.

  >>> # bitwise NOT of the samples
  >>> ~Trace('Signal', [-1, -128, 0, 1, 127])
  Trace(label='Signal:not', samples=[0, 127, -1, -2, -128])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).invert()
  Trace(label='Signal:not', samples=[0, 127, -1, -2, -128])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, -128, 0, 1, 127])
  trace = ~signal
  go.Figure([signal.digital.plot(), trace.digital.plot(mode='lines+markers')])

.. _bitwise left shift:

Bitwise Left-Shift
------------------

.. important:: The two operands are converted to :class:`int` before the
  operation is performed.

You can bitwise shift left each signal *sample* with the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* by pushing zeros in from the right and let the leftmost bits fall off
with the ``<<`` operator or by calling the method :meth:`~Trace.left_shift`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'shl'`` or ``'rshl'`` is returned.

  >>> # left shift the samples by a trace
  >>> Trace('Signal1', [-1, -128, 0, 1, 127]) << Trace('Signal2', [1, 1, 1, 0, 1])
  Trace(label='Signal1:shl', samples=[-2, -256, 0, 1, 254])
  >>> Trace('Signal1', [-1, -128, 0, 1, 127]).left_shift(Trace('Signal2', [1, 1, 1, 0, 1]))
  Trace(label='Signal1:shl', samples=[-2, -256, 0, 1, 254])

  >>> # left shift the samples by an iterable
  >>> Trace('Signal', [-1, -128, 0, 1, 127]) << [1, 1, 1, 0, 1]
  Trace(label='Signal:shl', samples=[-2, -256, 0, 1, 254])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).left_shift([1, 1, 1, 0, 1])
  Trace(label='Signal:shl', samples=[-2, -256, 0, 1, 254])

  >>> # left shift the samples by a number
  >>> Trace('Signal', [-1, -128, 0, 1, 127]) << 1
  Trace(label='Signal:shl', samples=[-2, -256, 0, 2, 254])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).left_shift(1)
  Trace(label='Signal:shl', samples=[-2, -256, 0, 2, 254])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-1, -128, 0, 1, 127])
  signal2 = Trace('Signal2', [1, 1, 1, 0, 1])
  trace = signal1 << signal2
  fig = go.Figure([signal1.digital.plot(),
                   signal2.digital.plot(),
                   trace.digital.plot(mode='lines+markers')])
  fig.show()

.. _bitwise right shift:

Bitwise Right-Shift
-------------------

.. important:: The two operands are converted to :class:`int` before the
  operation is performed.

You can bitwise shift right each signal *sample* with the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* by pushing copies of the leftmost bit in from the left, and let the
rightmost bits fall off with the ``>>`` operator or by calling the method
:meth:`~Trace.right_shift`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'shr'`` or ``'rshr'`` is returned.

  >>> # right shift the samples by a trace
  >>> Trace('Signal1', [-1, -128, 0, 1, 127]) >> Trace('Signal2', [1, 1, 1, 0, 1])
  Trace(label='Signal1:shr', samples=[-1, -64, 0, 1, 63])
  >>> Trace('Signal1', [-1, -128, 0, 1, 127]).right_shift(Trace('Signal2', [1, 1, 1, 0, 1]))
  Trace(label='Signal1:shr', samples=[-1, -64, 0, 1, 63])

  >>> # right shift the samples by an iterable
  >>> Trace('Signal', [-1, -128, 0, 1, 127]) >> [1, 1, 1, 0, 1]
  Trace(label='Signal:shr', samples=[-1, -64, 0, 1, 63])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).right_shift([1, 1, 1, 0, 1])
  Trace(label='Signal:shr', samples=[-1, -64, 0, 1, 63])

  >>> # right shift the samples by a number
  >>> Trace('Signal', [-1, -128, 0, 1, 127]) >> 1
  Trace(label='Signal:shr', samples=[-1, -64, 0, 0, 63])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).right_shift(1)
  Trace(label='Signal:shr', samples=[-1, -64, 0, 0, 63])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` is returned!

.. plotly::

  from signalyzer import Trace

  signal1 = Trace('Signal1', [-1, -128, 0, 1, 127])
  signal2 = Trace('Signal2', [1, 1, 1, 0, 1])
  trace = signal1 >> signal2
  fig = go.Figure([signal1.digital.plot(),
                   signal2.digital.plot(),
                   trace.digital.plot(mode='lines+markers')])
  fig.show()


.. _bitwise unpacking:

Bitwise Unpacking
-----------------

.. important:: The operand is converted to :class:`int` before the operation is
  performed.

You can unpack a subset of consecutive bits from each signal *sample* by calling
the method :meth:`~Trace.bits`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'bits'`` is returned.

  >>> # unpacking of the least significant bit in the samples
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).bits(0)
  Trace(label='Signal:bits', samples=[1, 0, 0, 1, 1])

  >>> # unpacking of the most significant bit in the samples
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).bits(31)
  Trace(label='Signal:bits', samples=[1, 1, 0, 0, 0])

  >>> # unpacking of a subset of consecutive bits in the samples
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).bits(index=1, number=4)
  Trace(label='Signal:bits', samples=[15, 0, 0, 0, 15])
  >>> Trace('Signal', [-1, -128, 0, 1, 127]).bits(1, 4)
  Trace(label='Signal:bits', samples=[15, 0, 0, 0, 15])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, -128, 0, 1, 127])
  trace = signal.bits(1, 4)
  go.Figure([signal.digital.plot(), trace.digital.plot(mode='lines+markers')])
