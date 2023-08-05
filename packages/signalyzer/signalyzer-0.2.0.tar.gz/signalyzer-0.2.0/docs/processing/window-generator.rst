.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

.. _moving window:

Window Generator
================

You can generate for each signal *sample* a `moving window`_ with the *size* of
the number of signal samples over the signal :class:`~Trace.samples` itself by
calling the method :meth:`~Trace.window`.

  >>> trace = Trace('Signal', [1 , 2, 3, 4, 5, 6, 7, 8, 9])
  >>> # windows with the size of 3 signal samples
  >>> list(trace.window(3))
  [(1, 1, 1),
   (1, 1, 2),
   (1, 2, 3),
   (2, 3, 4),
   (3, 4, 5),
   (4, 5, 6),
   (5, 6, 7),
   (6, 7, 8),
   (7, 8, 9)]

.. note::

  The `moving window`_ generator uses the first signal sample as the *preset*
  value to generate the windows for the first *number* of signal
  :class:`~Trace.samples`.
