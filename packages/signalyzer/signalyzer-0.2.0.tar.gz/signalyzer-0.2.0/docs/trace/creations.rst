.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Trace Creation
==============

Create empty Trace
------------------

You can create an empty *unlabeled* :class:`Trace` instance by calling the
:class:`Trace` class.

  >>> Trace()
  Trace(label='Trace', samples=[])

You can create an empty *labeled* :class:`Trace` instance by calling the
:class:`Trace` class with a *label*.

  >>> Trace(label='Signal')
  Trace(label='Signal', samples=[])
  >>> Trace('Signal')
  Trace(label='Signal', samples=[])


Create Trace from Iterable
--------------------------

You can create an *unlabeled* :class:`Trace` from any iterable returning a list
of signal :attr:`~Trace.samples`.

  >>> # Trace from a list of samples
  >>> Trace(samples=[0, 1, 2, 3])
  Trace(label='Trace', samples=[0, 1, 2, 3])

  >>> # Trace from a tuple of samples
  >>> Trace(samples=(0, 1, 2, 3))
  Trace(label='Trace', samples=[0, 1, 2, 3])

  >>> # Trace from an iterator of samples
  >>> Trace(samples=range(4))
  Trace(label='Trace', samples=[0, 1, 2, 3])

.. plotly::

   from signalyzer import Trace

   signal = Trace(samples=range(4))
   go.Figure(signal.plot())


You can create a *labeled* :class:`Trace` from any iterables returning a list of
signal :attr:`~Trace.samples`.

  >>> # Trace from a list of samples
  >>> Trace(label='Signal', samples=[0, 1, 2, 3])
  Trace(label='Signal', samples=[0, 1, 2, 3])
  >>> Trace('Signal', [0, 1, 2, 3])
  Trace(label='Signal', samples=[0, 1, 2, 3])

  >>> # Trace from a tuple of samples
  >>> Trace(label='Signal', samples=(0, 1, 2, 3))
  Trace(label='Signal', samples=[0, 1, 2, 3])
  >>> Trace('Signal', (0, 1, 2, 3))
  Trace(label='Signal', samples=[0, 1, 2, 3])

  >>> # Trace from an iterator of samples
  >>> Trace(label='Signal', samples=range(4))
  Trace(label='Signal', samples=[0, 1, 2, 3])
  >>> Trace('Signal', range(4))
  Trace(label='Signal', samples=[0, 1, 2, 3])

.. plotly::

   from signalyzer import Trace

   signal = Trace('Signal', range(4))
   go.Figure(signal.plot())


Create Trace from Dictionary
----------------------------

You can create a :class:`Trace` from a dictionary returning an iterable of
signal :attr:`~Trace.samples` by calling the class method :meth:`~Trace.from_dict`.

  >>> # dictionary with two signals and their samples to analyze
  >>> signals = {'Signal1': range(4), 'Signal2': [0, -1, -2 , -3]}

  >>> # create trace for signal 1 with the key name as the label
  >>> Trace.from_dict('Signal1', signals)
  Trace(label='Signal1', samples=[0, 1, 2, 3])

  >>> # create trace for signal 2 with an explicit label
  >>> Trace.from_dict('Signal2', signals, label='MyLabel')
  Trace(label='MyLabel', samples=[0, -1, -2, -3])

.. plotly::

   from signalyzer import Trace

   signals = {'Signal1': range(4), 'Signal2': [0, -1, -2 , -3]}
   signal1 = Trace.from_dict('Signal1', signals)
   signal2 = Trace.from_dict('Signal2', signals, label='MyLabel')
   go.Figure([signal1.plot(), signal2.plot()])
