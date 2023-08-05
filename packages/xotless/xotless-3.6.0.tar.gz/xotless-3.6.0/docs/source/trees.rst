==============================================================
 :mod:`xotless.trees` -- An implementation of an IntervalTree
==============================================================

.. automodule:: xotless.trees

.. autoclass:: IntervalTree(...)

   .. automethod:: from_cells(cells: Sequence[Cell[T, TOrd]]) -> IntervalTree[T, TOrd]
   .. automethod:: get(query: TOrd) -> Tuple[Cell[T, TOrd], ...]

.. autoclass:: Cell

   .. automethod:: from_bounds(lower: Optional[TOrd], upper: Optional[TOrd], data: T) -> Cell[T, TOrd]
   .. automethod:: from_range(r: xotless.ranges.Range[TOrd]], data: T) -> Cell[T, TOrd]
