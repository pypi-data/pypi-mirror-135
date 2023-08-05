.. currentmodule:: signalyzer

.. _statemachine:

Statemachine
============

The `Signalyzer` package provides a :class:`Statemachine` class to evaluate
the state transitions observed by a time-discrete, equidistant sampled
:attr:`~Statemachine.signal` containing the integer :attr:`~Statemachine.numbers`
of the :attr:`~Statemachine.states`.

A :class:`Statemachine` is a data class with mutable mapping support to iterate
over the :attr:`~Statemachine.states` or to select a state by its *number*.

You can import the :class:`Statemachine` class from the ``signalyzer``
package.

  >>> from signalyzer import Statemachine

Creation
--------

Empty Statemachine
~~~~~~~~~~~~~~~~~~

You can create an empty :class:`Statemachine` instance by calling the
:class:`Statemachine` class.

  >>> Statemachine(states={})
  Statemachine(states={},
               signal=Trace(label='Trace', samples=[]),
               labels=[],
               matrix=[])

  >>> Statemachine({})
  Statemachine(states={},
               signal=Trace(label='Trace', samples=[]),
               labels=[],
               matrix=[])

Statemachine with a Number of States
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a `statemachine`_ with the number of *states* to create by
calling the class method :meth:`~Statemachine.create`, optional with a *start*
number for the :attr:`~Statemachine.states` to create.

  >>> # create statemachine with 3 states starting with 0
  >>> Statemachine.create(states=3)
  Statemachine(states={0: 0, 1: 1, 2: 2},
               signal=Trace(label='Trace', samples=[]),
               labels=['0', '1', '2'],
               matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])

  >>> # create statemachine with 3 states starting with -1
  >>> Statemachine.create(3, start=-1)
  Statemachine(states={-1: 0, 0: 1, 1: 2},
               signal=Trace(label='Trace', samples=[]),
               labels=['0', '1', '2'],
               matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])

Statemachine from a List of State Labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a `statemachine`_ from a list with the :attr:`~Statemachine.labels`
of the *states* to create by calling the class method :meth:`Statemachine.create`,
optional with a *start* number for the :attr:`~Statemachine.states` to create.

  >>> # create statemachine from a list defining the state labels starting with 0
  >>> Statemachine.create(states=['Negative', 'Zero', 'Positive'])
  Statemachine(states={0: 'Negative', 1: 'Zero', 2: 'Positive'},
               signal=Trace(label='Trace', samples=[]),
               labels=['Negative', 'Zero', 'Positive'],
               matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])

  >>> # create statemachine from a list defining the state labels starting with -1
  >>> Statemachine.create(['Negative', 'Zero', 'Positive'], start=-1)
  Statemachine(states={-1: 'Negative', 0: 'Zero', 1: 'Positive'},
               signal=Trace(label='Trace', samples=[]),
               labels=['Negative', 'Zero', 'Positive'],
               matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])

Properties
----------

Get States
~~~~~~~~~~

You can get the *states* of the :class:`Statemachine` with the
:attr:`~Statemachine.states` attribute.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.states
  {-1: 0, 0: 1, 1: 2}

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.states
  {-1: 'Negative', 0: 'Zero', 1: 'Positive'}

Get State Numbers
~~~~~~~~~~~~~~~~~

You can get the state *numbers* of the :class:`Statemachine` with the
:attr:`~Statemachine.numbers` attribute.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.numbers
  [-1, 0, 1]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.numbers
  [-1, 0, 1]

Get State Labels
~~~~~~~~~~~~~~~~

You can get the state *labels* of the :class:`Statemachine` with the
:attr:`~Statemachine.labels` attribute.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.labels
  ['0', '1', '2']

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.labels
  ['Negative', 'Zero', 'Positive']

Get Signal Trace
~~~~~~~~~~~~~~~~

You can get the *signal* trace evaluated by the :class:`Statemachine` with the
:attr:`~Statemachine.signal` attribute.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.signal
  Trace(label='Trace', samples=[])

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.signal
  Trace(label='Trace', samples=[])

Set Signal Trace
~~~~~~~~~~~~~~~~

You can set a new *signal* trace to be evaluated by the :class:`Statemachine`
by assigning a new :class:`Trace` to the :attr:`~Statemachine.signal` attribute.

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.signal
  Trace(label='Trace', samples=[])

  >>> from signalyzer import Trace
  >>> trace =Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1])
  >>> machine.signal = trace
  >>> machine.signal
  Trace(label='States', samples=[-1, -1, 0, 0, 1, -1, 0, -1])

.. warning:: No ``value`` validations or ``value`` conversions are performed
  when you assign a new ``value`` to the attribute!

.. plotly::

   from signalyzer import Trace

   trace = Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1])
   go.Figure(trace.digital.plot(mode='lines+markers'))

Iterators
---------

Get Number of States
~~~~~~~~~~~~~~~~~~~~

Your can get the number :attr:`~Statemachine.states` in a :class:`Statemachine`
with the built-in function :func:`len`.

  >>> machine = Statemachine.create(3, -1)
  >>> len(machine)
  3

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> len(machine)
  3

State Items Iterator
~~~~~~~~~~~~~~~~~~~~

You can get the :class:`list` with the state *items* of the :class:`Statemachine`.

A :class:`list` with the state *items* is returned.

  >>> # list of the state items
  >>> machine = Statemachine.create(3, -1)
  >>> list(machine.items())
  [(-1, 0), (0, 1), (1, 2)]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> list(machine.items())
  [(-1, 'Negative'), (0, 'Zero'), (1, 'Positive')]

State Keys Iterator
~~~~~~~~~~~~~~~~~~~

You can get the :class:`list` with the state *keys* of the :class:`Statemachine`.

A :class:`list` with the state *keys* is returned.

  >>> machine = Statemachine.create(3, -1)
  >>> list(machine.keys())
  [-1, 0, 1]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> list(machine.keys())
  [-1, 0, 1]

State Values Iterator
~~~~~~~~~~~~~~~~~~~~~

You can get the :class:`list` with the state *values* of the
:class:`Statemachine`.

A :class:`list` with the state *values* is returned.

  >>> machine = Statemachine.create(3, -1)
  >>> list(machine.values())
  [0, 1, 2]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> list(machine.values())
  ['Negative', 'Zero', 'Positive']

State Transitions
-----------------

Get Transition Matrix
~~~~~~~~~~~~~~~~~~~~~

Your can get the state transition *matrix* of a :class:`Statemachine` with
the :attr:`~Statemachine.matrix` attribute.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.matrix
  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.matrix
  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


Zeroed Transition Matrix
~~~~~~~~~~~~~~~~~~~~~~~~

Your can create a zeroed state transition *matrix* of a :class:`Statemachine` by
calling the method :meth:`~Statemachine.zeroed_matrix`.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.zeroed_matrix()
  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.zeroed_matrix()
  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

Zeroed State Transition Counters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your can create a dictionary with zeroed state transition counters of a
:class:`Statemachine` by calling the method :meth:`~Statemachine.zeroed_counters`.

  >>> machine = Statemachine.create(3, -1)
  >>> machine.zeroed_counters()
  {(-1, 0): 0, (-1, 1): 0, (0, -1): 0, (0, 1): 0, (1, -1): 0, (1, 0): 0}

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.zeroed_counters()
  {(-1, 0): 0, (-1, 1): 0, (0, -1): 0, (0, 1): 0, (1, -1): 0, (1, 0): 0}

Evaluation
----------

Evaluate at Creation-Point
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can evaluate a signal *trace* with the observed *states* of a
:class:`Statemachine` at creation-point by calling the class method
:meth:`Statemachine.create` with the *signal* trace to evaluate.

  >>> # evaluate signal trace at creation-point
  >>> Statemachine.create(
  ...   states=3,
  ...   start=-1,
  ...   signal=Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1]))
  Statemachine(states={-1: 0, 0: 1, 1: 2},
               signal=Trace(label='States',
                            samples=[-1, -1, 0, 0, 1, -1, 0, -1]),
               labels=['0', '1', '2'],
               matrix=[[0, 2, 0], [1, 0, 1], [1, 0, 0]])

  >>> # evaluate signal trace at creation-point
  >>> Statemachine.create(
  ...   states=['Negative', 'Zero', 'Positive'],
  ...   start=-1,
  ...   signal=Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1]))
  Statemachine(states={-1: 'Negative', 0: 'Zero', 1: 'Positive'},
               signal=Trace(label='States',
                            samples=[-1, -1, 0, 0, 1, -1, 0, -1]),
               labels=['Negative', 'Zero', 'Positive'],
               matrix=[[0, 2, 0], [1, 0, 1], [1, 0, 0]])

Evaluate after Creation-Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can evaluate a signal *trace* with the observed *states* of a
:class:`Statemachine` by calling the method :meth:`~Statemachine.evaluate`.

  >>> # evaluate signal trace after creation-point
  >>> machine = Statemachine.create(3, -1)
  >>> machine.evaluate(Trace(label='States',
  ...                        samples=[-1, -1, 0, 0, 1, -1, 0, -1]))
  Statemachine(states={-1: 0, 0: 1, 1: 2},
               signal=Trace(label='States',
                            samples=[-1, -1, 0, 0, 1, -1, 0, -1]),
               labels=['0', '1', '2'],
               matrix=[[0, 2, 0], [1, 0, 1], [1, 0, 0]])

  >>> # evaluate signal trace after creation-point
  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.evaluate(Trace(label='States',
  ...                        samples=[-1, -1, 0, 0, 1, -1, 0, -1]))
  Statemachine(states={-1: 'Negative', 0: 'Zero', 1: 'Positive'},
               signal=Trace(label='States',
                            samples=[-1, -1, 0, 0, 1, -1, 0, -1]),
               labels=['Negative', 'Zero', 'Positive'],
               matrix=[[0, 2, 0], [1, 0, 1], [1, 0, 0]])

Transition Table
----------------

Data Table
~~~~~~~~~~

You can create the *data* table for the transition :attr:`~Statemachine.matrix`
of a :class:`Statemachine` by calling the method :meth:`~Statemachine.data`

  >>> machine = Statemachine.create(3, -1)
  >>> machine.data()
  [['', '0', '1', '2'], ['0', 0, 0, 0], ['1', 0, 0, 0], ['2', 0, 0, 0]]

  >>> machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1)
  >>> machine.data()
  [['', 'Negative', 'Zero', 'Positive'],
   ['Negative', 0, 0, 0], ['Zero', 0, 0, 0], ['Positive', 0, 0, 0]]

Table Figure
~~~~~~~~~~~~

You can create a table figure for the transition :attr:`~Statemachine.matrix`
of a :class:`Statemachine` by calling the method :meth:`~Statemachine.table`

  >>> # table figure of the transition matrix of the state machine
  >>> figure = machine.table()

.. plotly::

   from signalyzer import Statemachine, Trace

   trace = Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1])
   machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1, signal=trace)
   fig = machine.table()
   fig.show()

Transition Heatmap
------------------

Heatmap Figure
~~~~~~~~~~~~~~

You can create a heatmap figure for the transition :attr:`~Statemachine.matrix`
of a :class:`Statemachine` by calling the method :meth:`~Statemachine.heatmap`

  >>> # heatmap figure of the transition matrix of the state machine
  >>> figure = machine.heatmap()

.. plotly::

   from signalyzer import Statemachine, Trace

   trace = Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1])
   machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1, signal=trace)
   fig = machine.heatmap()
   fig.show()

Heatmap Plot
~~~~~~~~~~~~

You can create a heatmap plot for the transition :attr:`~Statemachine.matrix`
of a :class:`Statemachine` by calling the method :meth:`~Statemachine.plot`

  >>> # heatmap plot of the transition matrix of the state machine
  >>> plot = machine.plot()

.. plotly::

   from signalyzer import Statemachine, Trace

   trace = Trace('States', [-1, -1, 0, 0, 1, -1, 0, -1])
   machine = Statemachine.create(['Negative', 'Zero', 'Positive'], -1, signal=trace)
   go.Figure(machine.plot())
