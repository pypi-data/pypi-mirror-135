.. currentmodule:: signalyzer

.. _signal transformations:

Signal Transformations
======================

The :class:`Trace` class supports *operators* and provides *methods* to transform
the :attr:`~Trace.samples` of a :class:`Trace` into a new :class:`Trace` instance
labeled with the performed signal transformation.

.. toctree::
   :maxdepth: 3
   :caption: Signal Transformations
   :hidden:

   value_conversions
   comparison_operators
   arithmetic_operators
   bitwise_operators
   assignment_operators
   mathematical_functions
   trigonometric_functions
   differentiating_functions
   integrating_functions
   statistics
   x-axis_transformations


Value Conversions
-----------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 30, 50, 20
   :align: left

   :meth:`~Trace.bool`, :ref:`Boolean <booleans>`, ``'bool'``
   :meth:`~Trace.int`, :ref:`Integer <integers>`, ``'int'``
   :meth:`~Trace.float`, :ref:`Float<floats>`, ``'float'``
   :meth:`~Trace.bin`, :ref:`Binary <binary>`, ``'bin'``
   :meth:`~Trace.oct`, :ref:`Octal <octal>`, ``'oct'``
   :meth:`~Trace.hex`, :ref:`Hexadecimal <hexadecimal>`, ``'hex'``


Comparison Operations
---------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 30, 50, 20
   :align: left

   :meth:`~Trace.less`, :ref:`Less Than <lesser>`, ``'lt'``
   :meth:`~Trace.less_equal`, :ref:`Less than or Equal to <lesser or equal>`, ``'le'``
   :meth:`~Trace.equal`, :ref:`Equal <equal>`, ``'eq'``
   :meth:`~Trace.not_equal`, :ref:`Not Equal <not equal>`, ``'ne'``
   :meth:`~Trace.greater_equal`, :ref:`Greater than or Equal to <greater or equal>`, ``'ge'``
   :meth:`~Trace.greater`, :ref:`Greater Than <greater>`, ``'gt'``


Arithmetic Operations
---------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 40, 40
   :align: left

   :meth:`~Trace.add`, :ref:`Addition <addition>`, ``'add'`` or ``'radd'``
   :meth:`~Trace.sub`, :ref:`Subtraction <subtraction>`, ``'sub'`` or ``'rsub'``
   :meth:`~Trace.mul`, :ref:`Multiplication <multiplication>`, ``'mul'`` or ``'rmul'``
   :meth:`~Trace.div`, :ref:`Division <division>`, ``'div'`` or ``'rdiv'``
   :meth:`~Trace.floordiv`, :ref:`Floor Division <floor division>`, ``'floordiv'`` or ``'rfloordiv'``
   :meth:`~Trace.mod`, :ref:`Modulo <modulo>`, ``'mod'`` or ``'rmod'``
   :meth:`~Trace.pow`, :ref:`Exponentiation <exponentiation>`, ``'pow'`` or ``'rpow'``


Bitwise Operations
------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 30, 50, 30
   :align: left

   :meth:`~Trace.bitwise_and`, :ref:`Bitwise AND <bitwise AND>`, ``'and'`` or ``'rand'``
   :meth:`~Trace.bitwise_or`,:ref:`Bitwise OR <bitwise OR>`, ``'or'`` or ``'ror'``
   :meth:`~Trace.bitwise_xor`, :ref:`Bitwise XOR <bitwise XOR>`, ``'xor'`` or ``'rxor'``
   :meth:`~Trace.invert`, :ref:`Bitwise NOT <bitwise NOT>`, ``'not'``
   :meth:`~Trace.left_shift`, :ref:`Bitwise Left Shift <bitwise left shift>`, ``'shl'`` or ``'rshl'``
   :meth:`~Trace.right_shift`, :ref:`Bitwise Right Shift <bitwise right shift>`, ``'shr'`` or ``'rshr'``
   :meth:`~Trace.bits`, :ref:`Bitwise Unpacking <bitwise unpacking>`, ``'bits'``


Assignment Operations
---------------------

.. csv-table::
   :header: "Operator", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   ``+=``, :ref:`Addition <assigning addition>`, ``'iadd'``
   ``-=``, :ref:`Subtraction <assigning subtraction>`, ``'isub'``
   ``*=``, :ref:`Multiplication <assigning multiplication>`, ``'imul'``
   ``/=``, :ref:`Division <assigning division>`, ``idiv``
   ``//=``, :ref:`Floor Division <assigning floor division>`, ``'ifloordiv'``
   ``%=``, :ref:`Modulo <assigning modulo>`, ``'imod'``
   ``**=``, :ref:`Exponentiation <assigning exponentiation>`, ``'ipow'``
   ``&=``, :ref:`Bitwise AND <assigning bitwise AND>`, ``'iand'``
   ``|=``, :ref:`Bitwise OR <assigning bitwise OR>`, ``'ior'``
   ``^=``, :ref:`Bitwise XOR <assigning bitwise XOR>`, ``'ixor'``
   ``<<=``, :ref:`Bitwise Left Shift <assigning bitwise left shift>`, ``'ishl'``
   ``>>=``, :ref:`Bitwise Right Shift <assigning bitwise right shift>`, ``'ishr'``


Mathematical Functions
----------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   :meth:`~Trace.neg`, :ref:`Negation <negation>`, ``'neg'``
   :meth:`~Trace.abs`, :ref:`Absolute <absolute>`, ``'abs'``
   :meth:`~Trace.round`, :ref:`Rounding <rounding>`, ``'round'``
   :meth:`~Trace.trunc`, :ref:`Truncation <truncation>`, ``'trunc'``
   :meth:`~Trace.floor`, :ref:`Floor Rounding <floor>`, ``'floor'``
   :meth:`~Trace.ceil`, :ref:`Ceil Rounding <ceil>`, ``'ceil'``
   :meth:`~Trace.sign`, :ref:`Signum <signum>`, ``'sign'``
   :meth:`~Trace.zero`, :ref:`Zeros <zeros>`, ``'zero'``
   :meth:`~Trace.positive`, :ref:`Positives <positives>`, ``'positive'``
   :meth:`~Trace.negative`, :ref:`Negatives <negatives>`, ``'negative'``
   :meth:`~Trace.min`, :ref:`Min <min>`, ``'min'``
   :meth:`~Trace.max`, :ref:`Max <max>`, ``'max'``
   :meth:`~Trace.average`, :ref:`Average <average>`, ``'avg'``

Trigonometric Functions
-----------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   :meth:`~Trace.sin`, :ref:`Sine <sine>`, ``'sin'``
   :meth:`~Trace.cos`, :ref:`Cosine <cosine>`, ``'cos'``
   :meth:`~Trace.tan`, :ref:`Tangent <tangent>`, ``'tan'``
   :meth:`~Trace.asin`, :ref:`Arc Sine <arc sine>`, ``'asin'``
   :meth:`~Trace.acos`, :ref:`Arc Cosine <arc cosine>`, ``'acos'``
   :meth:`~Trace.atan`, :ref:`Arc Tangent <arc tangent>`, ``'atan'``
   :meth:`~Trace.sinh`, :ref:`Hyperbolic Sine <hyperbolic sine>`, ``'sinh'``
   :meth:`~Trace.cosh`, :ref:`Hyperbolic Cosine <hyperbolic cosine>`, ``'cosh'``
   :meth:`~Trace.tanh`, :ref:`Hyperbolic Tangent <hyperbolic tangent>`, ``'tanh'``
   :meth:`~Trace.asinh`, :ref:`Area Hyperbolic Sine <area hyperbolic sine>`, ``'asinh'``
   :meth:`~Trace.acosh`, :ref:`Area Hyperbolic Cosine <area hyperbolic cosine>`, ``'acosh'``
   :meth:`~Trace.atanh`, :ref:`Area Hyperbolic Tangent <area hyperbolic tangent>`, ``'atanh'``

Differentiating Functions
-------------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   :meth:`~Trace.delta`, :ref:`Delta <delta>`, ``'delta'``
   :meth:`~Trace.enter_positive`, :ref:`Enter Positives <enter_positives>`, ``'enter_positive'``
   :meth:`~Trace.left_positive`, :ref:`Left Positives <left_positives>`, ``'left_positive'``
   :meth:`~Trace.enter_negative`, :ref:`Enter Negatives <enter_negatives>`, ``'enter_negative'``
   :meth:`~Trace.left_negative`, :ref:`Left Negatives <left_negatives>`, ``'left_negative'``


Integrating Functions
---------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   :meth:`~Trace.accumulate`, :ref:`Accumulate <accumulate>`, ``'accumulate'``
   :meth:`~Trace.sums_positive`, :ref:`Sums Positive <sums positive>`, ``'sums_positive'``
   :meth:`~Trace.sums_negative`, :ref:`Sums Negative <sums negative>`, ``'sums_negative'``


Statistics
----------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 40
   :align: left

   :meth:`~Trace.sum`, :ref:`Sum <sum>`,
   :meth:`~Trace.count`, :ref:`Count <count>`,
   :meth:`~Trace.sort`, :ref:`Sort <sort>`, ``'sort'``
   :meth:`~Trace.winsorize`, :ref:`Winsorize <winsorize>`, ``'winsorize'``
   :meth:`~Trace.mean`, :ref:`Mean <mean>` :math:`\overline{x}`,
   :meth:`~Trace.weighted_mean`, :ref:`Weighted Mean <weighted mean>` :math:`\overline{x}_{w}`,
   :meth:`~Trace.winsor_mean`, :ref:`Winsor Mean <winsor mean>` :math:`\overline{x}_{w\alpha}`,
   :meth:`~Trace.median`, :ref:`Median <median>` :math:`\overline{x}_{med}`,
   :meth:`~Trace.mode`, :ref:`Mode <mode>` :math:`\overline{x}_{mod}`,
   :meth:`~Trace.min`, :ref:`Minimum <minimum>` :math:`x_{min}`,
   :meth:`~Trace.max`, :ref:`Maximum <maximum>` :math:`x_{max}`,
   :meth:`~Trace.range`, :ref:`Range <range>` :math:`x_{max} - x_{min}`,
   :meth:`~Trace.midrange`, :ref:`Mid-Range <midrange>` :math:`\frac{x_{max} + x_{min}}{2}`,
   :meth:`~Trace.aad`, :ref:`Average Absolute Deviation (AAD) <AAD>` :math:`D_{mean} = m_1`,
   :meth:`~Trace.mad`, :ref:`Median Absolute Deviation (MAD) <MAD>` :math:`D_{med}`,
   :meth:`~Trace.variance`, :ref:`Variance <variance>` :math:`\sigma^2 = m_2`,
   :meth:`~Trace.std`, :ref:`Standard Deviation <standard deviation>` :math:`\sigma`,
   :meth:`~Trace.coefficient`, :ref:`Coefficient of Variation <coefficient of variation>` :math:`c_v`,
   :meth:`~Trace.skew`, :ref:`Skew <skew>` :math:`m_3`,
   :meth:`~Trace.kurtosis`, :ref:`Kurtosis <kurtosis>` :math:`m_4`,
   :meth:`~Trace.zscore`, :ref:`Z-Score <zscore>` :math:`z`, ``'zscore'``
   :meth:`~Trace.quantiles`, :ref:`Quantiles <quantiles>` :math:`q_n`,

X-Axis Transformations
----------------------

.. csv-table::
   :header: "Method", "Name", "Label"
   :widths: 20, 80, 20
   :align: left

   :meth:`~Trace.move`, :ref:`Move <move>`, ``'move'``
   :meth:`~Trace.slice`, :ref:`Slice <slice>`, ``'slice'``
