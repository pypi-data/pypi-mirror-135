.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Trigonometric Functions
=======================

.. _sine:

Sine
----

You can compute the sine value for each signal *sample* by calling the
method :func:`~Trace.sin`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sin'`` is returned.

  >>> from math import pi
  >>> Trace('Signal', [-pi, -pi/2, 0, pi/2, pi]).sin()
  Trace(label='Signal:sin',
        samples=[-1.2246467991473532e-16, -1.0, 0.0, 1.0, 1.2246467991473532e-16])

.. plotly::

  from math import pi
  from signalyzer import Trace

  signal = Trace('Signal', [-pi, -pi/2, 0, pi/2, pi])
  trace = signal.sin()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _cosine:

Cosine
------

You can compute the cosine value for each signal *sample* by calling the
method :func:`~Trace.cos`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'cos'`` is returned.

  >>> from math import pi
  >>> Trace('Signal', [-pi, -pi/2, 0, pi/2, pi]).cos()
  Trace(label='Signal:cos',
        samples=[-1.0, 6.123233995736766e-17, 1.0, 6.123233995736766e-17, -1.0])

.. plotly::

  from math import pi
  from signalyzer import Trace

  signal = Trace('Signal', [-pi, -pi/2, 0, pi/2, pi])
  trace = signal.cos()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _tangent:

Tangent
-------

You can compute the tangent value for each signal *sample* by calling the
method :func:`~Trace.tan`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'tan'`` is returned.

  >>> from math import pi
  >>> Trace('Signal', [-pi, -pi/2, 0, pi/2, pi]).tan()
  Trace(label='Signal:tan',
        samples=[1.2246467991473532e-16,
                 -1.633123935319537e+16,
                 0.0,
                 1.633123935319537e+16,
                 -1.2246467991473532e-16])

.. plotly::

  from math import pi
  from signalyzer import Trace

  signal = Trace('Signal', [-pi, -pi/2, 0, pi/2, pi])
  trace = signal.tan()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _arc sine:

Arc Sine
--------

You can compute the arc sine value for each signal *sample* by calling the
method :func:`~Trace.asin`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'asin'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).asin()
  Trace(label='Signal:asin',
        samples=[-1.5707963267948966, 0.0, 1.5707963267948966])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.asin()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _arc cosine:

Arc Cosine
----------

You can compute the arc cosine value for each signal *sample* by calling the
method :func:`~Trace.acos`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'acos'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).acos()
  Trace(label='Signal:acos',
        samples=[3.141592653589793, 1.5707963267948966, 0.0])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.acos()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _arc tangent:

Arc Tangent
-----------

You can compute the arc tangent value for each signal *sample* by calling the
method :func:`~Trace.atan`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'atan'`` is returned.

  >>> from math import pi
  >>> Trace('Signal', [-pi, 0, pi]).atan()
  Trace(label='Signal:atan',
        samples=[-1.2626272556789115, 0.0, 1.2626272556789115])

.. plotly::

  from math import pi
  from signalyzer import Trace

  signal = Trace('Signal', [-pi, 0, pi])
  trace = signal.atan()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _hyperbolic sine:

Hyperbolic Sine
---------------

You can compute the hyperbolic sine value for each signal *sample* by calling
the method :func:`~Trace.sinh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'sinh'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).sinh()
  Trace(label='Signal:sinh',
        samples=[-1.1752011936438014, 0.0, 1.1752011936438014])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.sinh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _hyperbolic cosine:

Hyperbolic Cosine
-----------------

You can compute the hyperbolic cosine value for each signal *sample* by calling
the method :func:`~Trace.cosh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'cosh'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).cosh()
  Trace(label='Signal:cosh',
        samples=[1.5430806348152437, 1.0, 1.5430806348152437])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.cosh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _hyperbolic tangent:

Hyperbolic Tangent
------------------

You can compute the hyperbolic tangent value for each signal *sample* by calling
the method :func:`~Trace.tanh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'tanh'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).tanh()
  Trace(label='Signal:tanh',
        samples=[-0.7615941559557649, 0.0, 0.7615941559557649])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.tanh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _area hyperbolic sine:

Area Hyperbolic Sine
--------------------

You can compute the area hyperbolic sine value for each signal *sample* by
calling the method :func:`~Trace.asinh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'asinh'`` is returned.

  >>> Trace('Signal', [-1, 0, 1]).asinh()
  Trace(label='Signal:asinh',
        samples=[-0.8813735870195429, 0.0, 0.8813735870195429])

.. plotly::

  from signalyzer import Trace

  signal = Trace('Signal', [-1, 0, 1])
  trace = signal.asinh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _area hyperbolic cosine:

Area Hyperbolic Cosine
----------------------

You can compute the area hyperbolic cosine value for each signal *sample* by
calling the method :func:`~Trace.acosh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'acosh'`` is returned.

  >>> from math import pi
  >>> Trace('Signal', [1, pi/2, pi]).acosh()
  Trace(label='Signal:acosh',
        samples=[0.0, 1.0232274785475506, 1.811526272460853])

.. plotly::

  from math import pi
  from signalyzer import Trace

  signal = Trace('Signal', [1, pi/2, pi])
  trace = signal.acosh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])


.. _area hyperbolic tangent:

Area Hyperbolic Tangent
-----------------------

You can compute the area hyperbolic tangent value for each signal *sample* by
calling the method :func:`~Trace.atanh`.

A new :class:`Trace` instance *labeled* with the performed transformation
``'atanh'`` is returned.

  >>> # epsilon for a 32-bit floating-point number
  >>> epsilon = 2 ** -24
  >>> Trace('Signal', [-1.0 + epsilon, 0, 1.0 - epsilon]).atanh()
  Trace(label='Signal:atanh',
        samples=[-8.664339742098155, 0.0, 8.664339742098155])

.. plotly::

  from signalyzer import Trace

  epsilon = 2 ** -24
  signal = Trace('Signal', [-1.0 + epsilon, 0, 1.0 - epsilon])
  trace = signal.atanh()
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])
