.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Value Conversions
=================

.. _booleans:

Convert to Booleans
-------------------

.. important::

  Boolean literals are strings and **not** values!

You can convert each signal *sample* to :class:`bool` by calling the method
:meth:`~Trace.bool`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'bool'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).bool()
  Trace(label='Signal:bool', samples=[True, False, True])
  >>> Trace('Signal', [-1, 0, 1]).bool().int()
  Trace(label='Signal:bool:int', samples=[1, 0, 1])


.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1]).bool()
  go.Figure(trace.digital.plot(mode='lines+markers'))


.. _integers:

Convert to Integers
-------------------

You can convert each signal *sample* to :class:`int` by calling the method
:meth:`~Trace.int`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'int'`` is returned.

  >>> Trace('Signal', [-0.5, 0.0, 0.5]).int()
  Trace(label='Signal:int', samples=[0, 0, 0])

  >>> Trace('Signal', [-0.5, 0.0, 0.5]).int().float()
  Trace(label='Signal:int:float', samples=[0.0, 0.0, 0.0])

.. plotly::

   from signalyzer import Trace

   trace = Trace('Signal', [-0.5, 0.0, 0.5]).int()
   go.Figure(trace.plot(mode='lines+markers'))


.. _floats:

Convert to Floats
-----------------

You can convert the signal :attr:`~Trace.samples` to :class:`float` by calling
the method :meth:`~Trace.float`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'float'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).float()
  Trace(label='Signal:float', samples=[-1.0, 0.0, 1.0])

  >>> Trace('Signal', [-1, 0, 1]).float().int()
  Trace(label='Signal:float:int', samples=[-1, 0, 1])

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1]).float()
  go.Figure(trace.plot(mode='lines+markers'))


.. _binary:

Convert to Binary
-----------------

.. important::

  Binary number literals are strings and **not** values!

You can convert each signal *sample* to binary literals by calling the method
:meth:`~Trace.bin`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'bin'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).bin()
  Trace(label='Signal:bin', samples=['-0b1', '0b0', '0b1'])

  >>> Trace('Signal', [-1, 0, 1]).bin().int(0)
  Trace(label='Signal:bin:int', samples=[-1, 0, 1])

  >>> Trace('Signal', [-1, 0, 1]).bin().int(2)
  Trace(label='Signal:bin:int', samples=[-1, 0, 1])

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1]).bin()
  go.Figure(trace.digital.plot(mode='lines+markers'))


.. _octal:

Convert to Octal
----------------

.. important::

  Octal number literals are strings and **not** values!

You can convert each signal *sample* to octal literals by calling the method
:meth:`~Trace.oct`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'oct'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).oct()
  Trace(label='Signal:oct', samples=['-0o1', '0o0', '0o1'])

  >>> Trace('Signal', [-1, 0, 1]).oct().int(0)
  Trace(label='Signal:oct:int', samples=[-1, 0, 1])

  >>> Trace('Signal', [-1, 0, 1]).oct().int(8)
  Trace(label='Signal:oct:int', samples=[-1, 0, 1])

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1]).oct()
  go.Figure(trace.digital.plot(mode='lines+markers'))


.. _hexadecimal:

Convert to Hexadecimal
----------------------

.. important::

  Hexadecimal literals are strings and **not** values!

You can convert each signal *sample* to hexadecimal literals by calling the
method :meth:`~Trace.hex`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'hex'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).hex()
  Trace(label='Signal:hex', samples=['-0x1', '0x0', '0x1'])

  >>> Trace('Signal', [-1, 0, 1]).hex().int(0)
  Trace(label='Signal:hex:int', samples=[-1, 0, 1])

  >>> Trace('Signal', [-1, 0, 1]).hex().int(16)
  Trace(label='Signal:hex:int', samples=[-1, 0, 1])

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, 0, 1]).hex()
  go.Figure(trace.digital.plot(mode='lines+markers'))
