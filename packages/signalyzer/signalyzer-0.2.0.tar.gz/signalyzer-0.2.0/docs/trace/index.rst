.. currentmodule:: signalyzer

.. _signal trace:

Signal Trace
============

The ``signalyzer`` package provides a :class:`Trace` class to transform the
:attr:`~Trace.samples` of a time-discrete, equidistant sampled *signal*, and
:attr:`~Trace.label` the :class:`Trace` instance with the performed
:ref:`signal transformations <signal transformations>` by appending the ``names``
of the performed :ref:`signal transformation <signal transformations>` separated
by the colon ``:`` to the :attr:`~Trace.label` of the :class:`Trace`.

You can import the :class:`Trace` class from the ``signalyzer`` package.

  >>> from signalyzer import Trace

.. toctree::
   :maxdepth: 3
   :caption: Signal Trace
   :hidden:

   creations
   conversions
   operations

