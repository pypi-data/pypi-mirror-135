.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Assignment Operators
====================

.. _assigning addition:

Assigning Addition
------------------

You can add to each signal *sample* the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or float *number*, and assign
the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'iadd'``.

  >>> # add a trace to the samples
  >>> trace = Trace('Signal1', [1, 2, 3])
  >>> trace += Trace('Signal2', [-2, -3, -4])
  >>> trace
  Trace(label='Signal1:iadd', samples=[-1, -1, -1])

  >>> # add an iterable to the samples
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace += [-2, -3, -4]
  >>> trace
  Trace(label='Signal:iadd', samples=[-1, -1, -1])

  >>> # add a number to the samples
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace += 1
  >>> trace
  Trace(label='Signal:iadd', samples=[2, 3, 4])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3])
  trace += 1
  go.Figure(trace.plot(mode='lines+markers'))


.. _assigning subtraction:

Assigning Subtraction
---------------------

You can subtract from each signal *sample* the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*,
and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'isub'``.

  >>> # subtract a trace from the samples
  >>> trace = Trace('Signal1', [1, 2, 3])
  >>> trace -= Trace('Signal2', [2, 3, 4])
  >>> trace
  Trace(label='Signal1:isub', samples=[-1, -1, -1])

  >>> # subtract an iterable from the samples
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace -= [2, 3, 4]
  >>> trace
  Trace(label='Signal:isub', samples=[-1, -1, -1])

  >>> # subtract a number from the samples
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace -= 1
  >>> trace
  Trace(label='Signal:isub', samples=[0, 1, 2])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3])
  trace -= 1
  go.Figure(trace.plot(mode='lines+markers'))

.. _assigning multiplication:

Assigning Multiplication
------------------------

You can multiply each signal *sample* with the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*,
and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'imul'``.

  >>> # multiply the samples with a trace
  >>> trace = Trace('Signal1', [1, 2, 3])
  >>> trace *= Trace('Signal2', [2, 3, 4])
  >>> trace
  Trace(label='Signal1:imul', samples=[2, 6, 12])

  >>> # multiply the samples with an iterable
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace *= [2, 3, 4]
  >>> trace
  Trace(label='Signal:imul', samples=[2, 6, 12])

  >>> # multiply the samples with a number
  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace *= 2
  >>> trace
  Trace(label='Signal:imul', samples=[2, 4, 6])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [1, 2, 3])
  trace *= 2
  go.Figure(trace.plot(mode='lines+markers'))


.. _assigning division:

Assigning Division
------------------

You can divide each signal *sample* by the corresponding *element* in another
:class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float` *number*,
and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'idiv'``.

  >>> # divide the samples by a trace
  >>> trace = Trace('Signal1', [3, 6, 9])
  >>> trace /= Trace('Signal2', [2, 4, 6])
  >>> trace
  Trace(label='Signal1:idiv', samples=[1.5, 1.5, 1.5])

  >>> # divide the samples by an iterable
  >>> trace = Trace('Signal', [3, 6, 9])
  >>> trace /= [2, 4, 6]
  >>> trace
  Trace(label='Signal:idiv', samples=[1.5, 1.5, 1.5])

  >>> # divide the samples by a number
  >>> trace = Trace('Signal', [3, 6, 9])
  >>> trace /= 2
  >>> trace
  Trace(label='Signal:idiv', samples=[1.5, 3.0, 4.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [3, 6, 9])
  trace /= 2
  go.Figure(trace.plot(mode='lines+markers'))


.. _assigning floor division:

Assigning Floor Division
------------------------

You can integer divide each signal *sample* by the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ifloordiv'``.

  >>> # integer divide the samples by a trace
  >>> trace = Trace('Signal1', [3, 6, 9])
  >>> trace //= Trace('Signal2', [2, 4, 6])
  >>> trace
  Trace(label='Signal1:ifloordiv', samples=[1, 1, 1])

  >>> # integer divide the samples by an iterable
  >>> trace = Trace('Signal', [3, 6, 9])
  >>> trace //= [2, 4, 6]
  >>> trace
  Trace(label='Signal:ifloordiv', samples=[1, 1, 1])

  >>> # integer divide the samples by a number
  >>> trace = Trace('Signal', [3, 6, 9])
  >>> trace //= 2
  >>> trace
  Trace(label='Signal:ifloordiv', samples=[1, 3, 4])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [3, 6, 9])
  trace //= 2
  go.Figure(trace.plot(mode='lines+markers'))


.. _assigning modulo:

Assigning Modulo
----------------

You can modulo divide each signal *sample* by the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'imod'``.

  >>> # modulo divide the samples by a trace
  >>> trace = Trace('Signal1', [-3, 6, 9.5])
  >>> trace %= Trace('Signal2', [2, 4, -6])
  >>> trace
  Trace(label='Signal1:imod', samples=[1, 2, -2.5])

  >>> # modulo divide the samples by an iterable
  >>> trace = Trace('Signal', [-3, 6, 9.5])
  >>> trace %= [2, 4, -6]
  >>> trace
  Trace(label='Signal:imod', samples=[1, 2, -2.5])

  >>> # modulo divide the samples by a number
  >>> trace = Trace('Signal', [-3, 6, 9.5])
  >>> trace %= 2
  >>> trace
  Trace(label='Signal:imod', samples=[1, 0, 1.5])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. note:: Zero-divisions between the samples are resolved by returning zero for
  the samples where the divisor is zero!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-3, 6, 9.5])
  trace %= 2
  go.Figure(trace.plot(mode='lines+markers'))


.. _assigning exponentiation:

Assigning Exponentiation
------------------------

You can raise each signal *sample* to the power of the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ipow'``.

  >>> # raise the samples to the power of a trace
  >>> trace = Trace('Signal1', [1, 0, -1])
  >>> trace **= Trace('Signal2', [-2, 0, 2])
  >>> trace
  Trace(label='Signal1:ipow', samples=[1.0, 1, 1])

  >>> # raise the samples to the power of an iterable
  >>> trace = Trace('Signal', [1, 0, -1])
  >>> trace **= [-2, 0, 2]
  >>> trace
  Trace(label='Signal:ipow', samples=[1.0, 1, 1])

  >>> #raise the samples to the power of a number
  >>> trace = Trace('Signal', [1, 0, -1])
  >>> trace **= 2
  >>> trace
  Trace(label='Signal:ipow', samples=[1, 0, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1])
  trace **= 2
  go.Figure(trace.plot(mode='lines+markers'))

.. _assigning bitwise AND:

Assigning Bitwise AND
---------------------

You can bitwise AND each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'iand'``.

  >>> # bitwise AND the samples with a trace
  >>> trace = Trace('Signal1', [-1, 0, 1])
  >>> trace &= Trace('Signal2', [0xff, 0xff, 0xff])
  >>> trace
  Trace(label='Signal1:iand', samples=[255, 0, 1])

  >>> # bitwise AND the samples with an iterable
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace &= [0xff, 0xff, 0xff]
  >>> trace
  Trace(label='Signal:iand', samples=[255, 0, 1])

  >>> # bitwise AND the samples with a number
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace &= 0xff
  >>> trace
  Trace(label='Signal:iand', samples=[255, 0, 1])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1])
  trace &= 0xff
  go.Figure(trace.digital.plot(mode='lines+markers'))

.. _assigning bitwise OR:

Assigning Bitwise OR
--------------------

You can bitwise OR each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ior'``.

  >>> # bitwise OR the samples with a trace
  >>> trace = Trace('Signal1', [-1, 0, 1])
  >>> trace |= Trace('Signal2', [0x0, 0xff, 0xfe])
  >>> trace
  Trace(label='Signal1:ior', samples=[-1, 255, 255])

  >>> # bitwise OR the samples with an iterable
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace |= [0x0, 0xff, 0xfe]
  >>> trace
  Trace(label='Signal:ior', samples=[-1, 255, 255])

  >>> # bitwise OR the samples with a number
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace |= 0xfe
  >>> trace
  Trace(label='Signal:ior', samples=[-1, 254, 255])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1])
  trace |= 0xfe
  go.Figure(trace.digital.plot(mode='lines+markers'))

.. _assigning bitwise XOR:

Assigning Bitwise XOR
---------------------

You can bitwise XOR each signal *sample* with the corresponding *element* in
another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number*, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ixor'``.

  >>> # bitwise XOR the samples with a trace
  >>> trace = Trace('Signal1', [-1, 0, 1])
  >>> trace ^= Trace('Signal2', [0xfe, 0x1, 0x1])
  >>> trace
  Trace(label='Signal1:ixor', samples=[-255, 1, 0])

  >>> # bitwise XOR the samples with an iterable
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace ^= [0xfe, 0x1, 0x1]
  >>> trace
  Trace(label='Signal:ixor', samples=[-255, 1, 0])

  >>> # bitwise XOR the samples with a number
  >>> trace = Trace('Signal', [-1, 0, 1])
  >>> trace ^= 0xfe
  >>> trace
  Trace(label='Signal:ixor', samples=[-255, 254, 255])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1])
  trace ^= 0xfe
  go.Figure(trace.digital.plot(mode='lines+markers'))

.. _assigning bitwise left shift:

Assigning Bitwise Left-Shift
-----------------------------

You can bitwise shift left each signal *sample* with the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* by pushing zeros in from the right and let the leftmost bits fall off,
and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ishl'``.

  >>> # left shift the samples by a trace
  >>> trace = Trace('Signal1', [-1, -128, 0, 1, 127])
  >>> trace <<= Trace('Signal2', [1, 1, 1, 0, 1])
  >>> trace
  Trace(label='Signal1:ishl', samples=[-2, -256, 0, 1, 254])

  >>> # left shift the samples by an iterable
  >>> trace = Trace('Signal', [-1, -128, 0, 1, 127])
  >>> trace <<= [1, 1, 1, 0, 1]
  >>> trace
  Trace(label='Signal:ishl', samples=[-2, -256, 0, 1, 254])

  >>> # left shift the samples by a number
  >>> trace = Trace('Signal', [-1, -128, 0, 1, 127])
  >>> trace <<= 1
  >>> trace
  Trace(label='Signal:ishl', samples=[-2, -256, 0, 2, 254])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, -128, 0, 1, 127])
  trace <<= 1
  go.Figure(trace.digital.plot(mode='lines+markers'))

.. _assigning bitwise right shift:

Assigning Bitwise Right-Shift
-----------------------------

You can bitwise shift right each signal *sample* with the corresponding *element*
in another :class:`Trace` or ``Iterable``, or an :class:`int` or :class:`float`
*number* by pushing copies of the leftmost bit in from the left, and let the
rightmost bits fall off, and assign the result to the signal *sample*.

The :class:`Trace` is *labeled* with the performed transformation ``'ishr'``.


  >>> # right shift the samples by a trace
  >>> trace = Trace('Signal1', [-1, -128, 0, 1, 127])
  >>> trace >>= Trace('Signal2', [1, 1, 1, 0, 1])
  >>> trace
  Trace(label='Signal1:ishr', samples=[-1, -64, 0, 1, 63])

  >>> # right shift the samples by an iterable
  >>> trace = Trace('Signal', [-1, -128, 0, 1, 127])
  >>> trace >>= [1, 1, 1, 0, 1]
  >>> trace
  Trace(label='Signal:ishr', samples=[-1, -64, 0, 1, 63])

  >>> # right shift the samples by a number
  >>> trace = Trace('Signal', [-1, -128, 0, 1, 127])
  >>> trace >>= 1
  >>> trace
  Trace(label='Signal:ishr', samples=[-1, -64, 0, 0, 63])

.. note:: An *iterable* should have at least the same length as the signal
  :attr:`~Trace.samples`, otherwise only a subset of the signal
  :attr:`~Trace.samples` are updated!

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, -128, 0, 1, 127])
  trace >>= 1
  go.Figure(trace.digital.plot(mode='lines+markers'))
