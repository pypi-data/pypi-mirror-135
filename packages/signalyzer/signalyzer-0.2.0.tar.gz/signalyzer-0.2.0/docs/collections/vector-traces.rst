.. _plotly: https://plotly.com/python/

.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _vector trace:

Vector Traces
=============

The `vector trace`_ collection is used to transform the signal :attr:`~Trace.samples`
of two :ref:`signal traces <signal trace>` representing the *x* and *y-coordinates*
of the 2-dimensional points within the cartesian coordinate system into polar
coordinate traces representing the *radius* and the *angle* of the vectors in the
polar coordinate system.

Polar Transformation of two Traces
----------------------------------

You can transform with the :func:`polar` function the signal :attr:`~Trace.samples`
of two :ref:`signal traces <signal trace>` representing the *x* and *y-coordinates*
of the 2-dimensional points within the cartesian coordinate system into polar
coordinate :ref:`signal traces <signal trace>` for the *radius* and *angle* of
the vectors in the polar coordinate system.

A :class:`dict` with the produced :ref:`signal traces <signal trace>` is returned.

  >>> polar(x=Trace('Signal', [1, 0, -1, 0]), y=[0, 1, 0, -1])
  {'r': Trace(label='Vector:r',
              samples=[1.0, 1.0, 1.0, 1.0]),
   'phi': Trace(label='Vector:phi',
                samples=[0.0,
                         1.5707963267948966,
                         3.141592653589793,
                         -1.5707963267948966]),
   'theta': Trace(label='Vector:theta',
                  samples=[0.0, 90.0, 180.0, 270.0])}

Create the Trace Collection
---------------------------

You can create a `vector trace`_ collection without *x,y-coordinates* by
calling the :class:`VectorTraces` class.

  >>> # create an empty vector trace collection
  >>> traces = VectorTraces()
  >>> traces
  VectorTraces(x=Trace(label='Trace', samples=[]),
               y=Trace(label='Trace', samples=[]),
               r=Trace(label='Vector:r', samples=[]),
               phi=Trace(label='Vector:phi', samples=[]),
               theta=Trace(label='Vector:theta', samples=[]),
               distance=Trace(label='Vector:distance', samples=[]),
               dot=Trace(label='Vector:dot', samples=[]))

Number of Traces
----------------

You can get the number of the traces in the :class:`VectorTraces` collection
with the built-in function :func:`len`.

  >>> # number of traces in the collection
  >>> len(traces)
  7

Names of the Traces
-------------------

You can get the :class:`list` with the names of the traces in the
:class:`VectorTraces` collection.

A :class:`list` with the key names of the traces is returned.

  >>> # key names of the traces in the collection
  >>> list(traces)
  ['x', 'y', 'r', 'phi', 'theta', 'distance', 'dot']

  >>> # key names of the traces in the collection
  >>> list(traces.keys())
  ['x', 'y', 'r', 'phi', 'theta', 'distance', 'dot']

x-Coordinate Trace
------------------

You can get the vector *x-coordinate* :class:`Trace` with the
:attr:`~VectorTraces.x` attribute from the :class:`VectorTraces` collection.

The :class:`Trace` with the vector *x-coordinates* is returned.

  >>> # vector x-coordinate trace by attribute
  >>> traces.x
  Trace(label='Trace', samples=[])
  >>> # vector x-coordinate trace by key
  >>> traces['x']
  Trace(label='Trace', samples=[])

y-Coordinate Trace
------------------

You can get the vector *y-coordinate*:class:`Trace` with the
:attr:`~VectorTraces.y` attribute from the :class:`VectorTraces` collection.

The :class:`Trace` with the vector *y-coordinates* is returned.

  >>> # vector y-coordinate trace by attribute
  >>> traces.y
  Trace(label='Trace', samples=[])
  >>> # vector y-coordinate trace by key
  >>> traces['y']
  Trace(label='Trace', samples=[])

Radius Trace
------------

You can get the vector *radius* :class:`Trace` with the :attr:`~VectorTraces.r`
attribute from the :class:`VectorTraces` collection.

The :class:`Trace` with the vector *radii* computed from the
*x-coordinate*, *y-coordinate* :attr:`~Trace.samples` is returned.

  >>> # radius trace by attribute
  >>> traces.r
  Trace(label='Vector:r', samples=[])
  >>> # radius trace by key
  >>> traces['r']
  Trace(label='Vector:r', samples=[])

Angle Trace in Radians
----------------------

You can get the vector *angle* :class:`Trace` from :math:`-\pi` to :math:`+\pi`
with the :attr:`~VectorTraces.phi` attribute from the :class:`VectorTraces`
collection.

The :class:`Trace` with the vector *angles* in radians computed from the
*x-coordinate*, *y-coordinate* :attr:`~Trace.samples` is returned.

  >>> # vector angle trace in radians by attribute
  >>> traces.phi
  Trace(label='Vector:phi', samples=[])
  >>> # vector angle trace in radians by key
  >>> traces['phi']
  Trace(label='Vector:phi', samples=[])

Angle Trace in Degree
---------------------

You can get the vector *angle* :class:`Trace` from ``0`` to ``360`` degree
with the :attr:`~VectorTraces.theta` attribute from the :class:`VectorTraces`
collection.

The :class:`Trace` with the vector *angles* in degree computed from the
*x-coordinate*, *y-coordinate* :attr:`~Trace.samples` is returned.

  >>> # vector angle trace in degree by attribute
  >>> traces.theta
  Trace(label='Vector:theta', samples=[])
  >>> # vector angle trace in degree by key
  >>> traces['theta']
  Trace(label='Vector:theta', samples=[])

Euclidean Distance Trace
------------------------

You can get the euclidean *distance* :class:`Trace` with the
:attr:`~VectorTraces.distance` attribute from the :class:`VectorTraces`
collection.

The :class:`Trace` with the euclidean *distances* of the consecutive x,y-points
computed from the *x-coordinate*, *y-coordinate* :attr:`~Trace.samples` is
returned.

  >>> # euclidean distance trace by attribute
  >>> traces.distance
  Trace(label='Vector:distance', samples=[])
  >>> # euclidean distance trace by key
  >>> traces['distance']
  Trace(label='Vector:distance', samples=[])

Dot Product Trace
------------------

You can get the *dot* product :class:`Trace` with the
:attr:`~VectorTraces.dot` attribute from the :class:`VectorTraces`
collection.

The :class:`Trace` with the *dot* products of the consecutive x,y-points
computed from the *x-coordinate*, *y-coordinate* :attr:`~Trace.samples` is
returned.

  >>> # dot product trace by attribute
  >>> traces.dot
  Trace(label='Vector:dot', samples=[])
  >>> # dot product trace by key
  >>> traces['dot']
  Trace(label='Vector:dot', samples=[])

Create a Polar Plot
-------------------

You can create a *polar* plot of the :class:`VectorTraces` by calling the method
:meth:`~VectorTraces.plot`.

A new `plotly`_ :class:`~plotly.graph_objects.Scatterpolar` trace is returned.

  >>> VectorTraces(Trace('x', [1, 0, -1, 0.5]),
  ...              Trace('y', [0, 0.75, 0, -0.5])).plot()
  Scatterpolar({
      'mode': 'lines+markers',
      'name': 'Vector',
      'r': [1.0, 0.75, 1.0, 0.7071067811865476],
      'theta': [0.0, 90.0, 180.0, 315.0]
  })

.. plotly::

  from signalyzer import Trace, VectorTraces

  x = Trace('Signal', [1, 0, -1, 0.5])
  y = Trace('Signal', [0, 0.75, 0, -0.5])
  traces = VectorTraces(x, y)
  go.Figure(traces.plot())
