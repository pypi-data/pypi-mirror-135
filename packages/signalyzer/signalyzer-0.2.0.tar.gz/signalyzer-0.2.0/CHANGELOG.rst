Change Log
**********

These are the enhancements, breaking changes and bug fixes of note between each
release.

.. _v0.2.0:

`0.2.0`_ - 2022-01-18
=====================

.. _0.2.0: https://gitlab.com/signalytics/signalyzer/compare/v0.1.0...v0.2.0

Enhancements
------------

* Add method :meth:`~Trace.ramp` to limit the slew-rates of a measured signal.
* Add method :meth:`~Trace.slew` to process a measured signal with a
  slew-rate limiter.
* Add dataclass :class:`SlewRateLimiterTraces` for the trace collection produced
  by the slew-rate limiter.
* Add dataclass :class:`SlewRateLimiter` for the results produced by the
  slew-rate limiter.
* Add method :meth:`~Trace.pt1` to process a measured signal with the transfer
  function of a PT1-element.
* Add method :meth:`~Trace.dt1` to process a measured signal with the transfer
  function of a DT1-element.
* Add method :meth:`~Trace.figure` to create a figure with the scatter plot of
  the trace.

Breaking Changes
----------------

* Remove method :meth:`~Trace.lag` in favour of the new method :meth:`~Trace.pt1`.

.. _v0.1.0:

`0.1.0`_ - 2022-01-15
=====================

.. _0.1.0: https://gitlab.com/signalytics/signalyzer/compare

* First release.
