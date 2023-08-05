.. _plotly: https://plotly.com/python/

.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Trace Operations
================

Get Trace Label
---------------

You can get the *label* string of the :class:`Trace` with the
:attr:`~Trace.label` attribute.

  >>> Trace('Signal', [1, 2, 3]).label
  'Signal'


Set Trace Label
---------------

You can set a new *label* string by assigning a new string to the
:attr:`~Trace.label` attribute.

  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace.label='NewLabel'
  >>> trace.label
  'NewLabel'


.. warning:: No ``value`` validations or ``value`` conversions are performed
  when you assign a new ``value`` to the attribute!

You can relabel a :class:`Trace` by calling the method :meth:`~Trace.relabel`.
The relabeled :class:`Trace` is returned.

  >>> Trace('Signal', [1, 2, 3]).relabel('NewLabel')
  Trace(label='NewLabel', samples=[1, 2, 3])


Get Trace Samples
-----------------

You can get the list of the signal *samples* with the :attr:`~Trace.samples`
attribute.

  >>> Trace('Signal', [1, 2, 3]).samples
  [1, 2, 3]


Set Trace Samples
-----------------

You can set a new :class:`list` of signal *samples* by assigning a new
:class:`list` to the signal :attr:`~Trace.samples` attribute.

  >>> trace = Trace('Signal', [1, 2, 3])
  >>> trace.samples=[-1, -2, -3]
  >>> trace.samples
  [-1, -2, -3]

.. warning:: No ``value`` validations or ``value`` conversions are performed
  when you assign a new ``value`` to the attribute!


Get Trace Fields
----------------

You can get the :class:`dataclasses.Field` properties of the :class:`Trace`
*data class* with the function :func:`~dataclasses.fields` from the
:mod:`dataclasses` module.

  >>> from dataclasses import fields
  >>> fields(Trace('Signal', [1, 2, 3])) #doctest: +SKIP
  (Field(name='label',
         type='str',
         default='Trace',
         default_factory=<dataclasses._MISSING_TYPE object at 0x0000000000000000>,
         init=True,
         repr=True,
         hash=None,
         compare=True,
         metadata=mappingproxy({}),_field_type=_FIELD),
  Field(name='samples',
        type='SamplesType',
        default=<dataclasses._MISSING_TYPE object at 0x0000000000000000>,
        default_factory=<class 'list'>,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=mappingproxy({}),_field_type=_FIELD))


Get Trace Length
----------------

Your can get the length of a :class:`Trace`, respectively the number of signal
:attr:`~Trace.samples` in a :class:`Trace`, with the built-in function
:func:`len`.

  >>> len(Trace('Signal', [1, 2, 3]))
  3


Check Trace is Empty or Not
---------------------------

Your can check if a :class:`Trace` is empty or not, respectively has signal
:attr:`~Trace.samples` or not, with the built-in operator :obj:`not`.

  >>> not Trace()
  True
  >>> not Trace('Signal', [1, 2, 3])
  False


Create Trace Iterator
---------------------

You can create an iterator over the signal :attr:`~Trace.samples` in a
:class:`Trace` with the built-in function :func:`iter`.

  >>> iter(Trace('Signal', [1, 2, 3])) #doctest: +SKIP
  <list_iterator at 0x00000000000>

You can create a reverse iterator over the signal :attr:`~Trace.samples` in a
:class:`Trace` with the built-in function :func:`reversed`.

  >>> reversed(Trace('Signal', [1, 2, 3])) #doctest: +SKIP
  <list_iterator at 0x00000000000>

You can create an iterator repeating each signal sample in a :class:`Trace`
n-*times* by calling the method :meth:`~Trace.repeat`.

  >>> Trace('Signal', [1, 2, 3]).repeat(3) #doctest: +SKIP
  <itertools.chain at 0x00000000000>

Copy Trace Samples
------------------

You can copy the signal :attr:`~Trace.samples` in a :class:`Trace` into a new
:class:`list` of signal samples.

  >>> list(Trace('Signal', [1, 2, 3]))
  [1, 2, 3]

You can copy the signal :attr:`~Trace.samples` in a :class:`Trace` into a new
:class:`tuple` of signal samples.

  >>> tuple(Trace('Signal', [1, 2, 3]))
  (1, 2, 3)


Check Trace for a Sample
------------------------

Your can check if an explicit *sample* value is in the signal :attr:`~Trace.samples`
of the :class:`Trace` or not.

  >>> # check for 0 in the signal samples
  >>> 0 in Trace('Signal', [1, 2, 3])
  False
  >>> # check for 1 in the signal samples
  >>> 1 in Trace('Signal', [1, 2, 3])
  True


Slice from the Trace Samples
----------------------------

You can slice the signal :attr:`~Trace.samples` of a :class:`Trace` into a new
:class:`list` of signal samples.

  >>> # slice of all samples
  >>> Trace('Signal', [1, 2, 3])[:]
  [1, 2, 3]
  >>> # slice the last two samples
  >>> Trace('Signal', [1, 2, 3])[-2:]
  [2, 3]
  >>> # slice the first two samples
  >>> Trace('Signal', [1, 2, 3])[:2]
  [1, 2]
  >>> # slice between the first and the last sample
  >>> Trace('Signal', [1, 2, 3])[1:-1]
  [2]


Get Sample by Index
-------------------

You can get a sampled value in the signal :attr:`~Trace.samples` of the
:class:`Trace` by its index.

  >>> # First sample
  >>> Trace('Signal', [1, 2, 3])[0]
  1
  >>> # Last sample
  >>> Trace('Signal', [1, 2, 3])[-1]
  3

Set Sample by Index
-------------------

You can set a sampled value in the signal :attr:`~Trace.samples` of the
:class:`Trace` by its index.

  >>> trace = Trace('Signal', [1, 2, 3])
  >>> # Set first sample
  >>> trace[0] = -1
  >>> trace[0]
  -1
  >>> # Set last sample
  >>> trace[-1] = -3
  >>> trace[-1]
  -3
  >>> trace
  Trace(label='Signal', samples=[-1, 2, -3])


Create Trace Plot
-----------------

You can create the :class:`Trace` plot by calling the method :meth:`~Trace.plot`.

A new `plotly`_ :class:`~plotly.graph_objects.Scatter` trace is returned.

  >>> Trace('Signal', map(lambda x: x**2, range(-4, 5))).plot()
  Scatter({
      'mode': 'lines',
      'name': 'Signal',
      'x': [0, 1, 2, 3, 4, 5, 6, 7, 8],
      'y': [16, 9, 4, 1, 0, 1, 4, 9, 16]
  })

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', map(lambda x: x**2, range(-4, 5)))
  go.Figure(trace.plot())


Get Digital Trace Plot
----------------------

You can get the *digital* trace of the :class:`Trace` with the
:attr:`~Trace.digital` attribute to plot a digital signal.

  >>> # get the digital trace
  >>> Trace('Signal', [-1, -1, 0, 0, 1, 1]).digital
  Digital(label='Signal', samples=[-1, -1, 0, 0, 1, 1])

  >>> # create the digital trace plot
  >>> Trace('Signal', [-1, -1, 0, 0, 1, 1]).digital.plot()
  Scatter({
    'line': {'shape': 'hv'},
    'mode': 'lines',
    'name': 'Signal',
    'x': [0, 1, 2, 3, 4, 5],
    'y': [-1, -1, 0, 0, 1, 1]
  })

.. plotly::

  from signalyzer import Trace

  trace = Trace('Signal', [-1, -1, 0, 0, 1, 1])
  go.Figure([trace.plot(), trace.digital.relabel('Digital Signal').plot()])


Create Trace Figure
-------------------

You can create the :class:`Trace` figure by calling the method
:meth:`~Trace.figure`.

A new `plotly`_ :class:`~plotly.graph_objects.Figure` with the
:class:`~plotly.graph_objects.Scatter` plot of the :class:`Trace` is returned.

  >>> figure = Trace('Signal', map(lambda x: x**2, range(-4, 5))).figure()

.. plotly::

  from signalyzer import Trace

  Trace('Signal', map(lambda x: x**2, range(-4, 5))).figure()
