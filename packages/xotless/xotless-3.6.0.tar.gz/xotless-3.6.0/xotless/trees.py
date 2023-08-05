#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# copyright (c) merchise autrement [~º/~] and contributors
# all rights reserved.
#
# this is free software; you can do what the licence file allows you to.
#
"""Implements trees for efficient searching.

"""
from __future__ import annotations

import operator
import typing as t
from dataclasses import dataclass, field
from itertools import takewhile

from xotl.tools.infinity import Infinity

from .ranges import Range, TOrd
from .tracing import get_module_sentry_spanner

T = t.TypeVar("T")


@dataclass(init=False, unsafe_hash=True)
class Cell(t.Generic[T, TOrd]):
    """A data-carrying open-right range."""

    # NB: Introducing any kind of Range here entails modifications to the
    # algorithms below.
    lowerbound: TOrd
    upperbound: TOrd
    data: T

    __slots__ = ("lowerbound", "upperbound", "data")

    def __init__(
        self,
        lower: t.Optional[TOrd],
        upper: t.Optional[TOrd],
        data: T,
    ) -> None:
        self.lowerbound = t.cast(TOrd, -Infinity if lower is None else lower)
        self.upperbound = t.cast(TOrd, Infinity if upper is None else upper)
        self.data = data

    @classmethod
    def from_bounds(
        cls,
        lower: t.Optional[TOrd],
        upper: t.Optional[TOrd],
        data: T,
    ) -> Cell[T, TOrd]:  # pragma: no cover
        """Return a cell from the boundaries of an open-right range."""
        return cls(lower, upper, data)

    @classmethod
    def from_range(cls, r: Range[TOrd], data: T) -> Cell[T, TOrd]:
        """Return a cell casting `r` to an open-right range.

        .. note:: We disregard the kind of range, cells are always open-right.

        """
        return cls(r.lowerbound, r.upperbound, data)

    def __contains__(self, which):  # pragma: no cover
        return self.lowerbound <= which < self.upperbound

    def __bool__(self) -> bool:  # pragma: no cover
        return self.lowerbound < self.upperbound


@dataclass(init=False, repr=False)
class IntervalTree:
    """A data-containing generic IntervalTree.

    Intended usage:

    - Create the tree by calling the classmethod `from_cells`:meth:.

      The `cells <Cell>`:class: which represent the boundaries of the interval
      related to an opaque data item.  The intervals are allowed over any type
      ``TOrd`` (i.e, for which `<=` is defined and total).

      The current implementation regards all intervals as open-right, closed-left
      (see `Cell.from_range`:meth:).

    - Use `get`:meth: or `__getitem__`:meth: (i.e ``tree[x]``) to get the
      intervals ``x`` belongs to.

    - Use ``x in tree`` to test if ``x`` belongs to at least one interval.

    - ``bool(tree)`` is True when the tree contains no cells.

    .. warning:: You SHOULDN'T mutate any of the internal attributes.  The API
       is just the class method `from_cells`:meth: and then getting the cells
       containing a point the with either `get`:meth: of `__getitem__`:meth:.

    .. seealso:: Section 10.1 of [deBerg2008]_.

    .. [deBerg2008] Mark de Berg, et al. *Computational Geometry. Algorithms
       and Applications. Third Edition*. Springer Verlag. 2008.

    """

    _impl: _ORIntervalTree = field(init=False)

    def __init__(self, cells: t.Sequence[Cell[T, TOrd]]) -> None:
        self._impl = _ORIntervalTree.from_cells(cells)

    @classmethod
    def from_cells(cls, cells: t.Sequence[Cell[T, TOrd]]) -> IntervalTree:
        """Build an IntervalTree from the given sequence of cells."""
        return cls(cells)

    def __bool__(self):
        return bool(self._impl)

    def __contains__(self, query: TOrd):
        return query in self._impl

    def get(self, which: TOrd) -> t.Tuple[Cell[T, TOrd], ...]:
        """Return the sequence of cells to which `query` belongs.

        If `query` is not in any of the cells, return the empty tuple.

        """
        return self._impl.get(which)

    def __getitem__(self, which: TOrd) -> t.Tuple[Cell[T, TOrd], ...]:
        """Return the sequence of cells to which `query` belongs.

        If `query` is not in any of the cells, raise KeyError.

        """
        return self._impl[which]

    @property
    def depth(self):
        "The depth of the IntervalTree."
        return self._impl.depth


@dataclass
class _IntervalTreeImplementation(t.Generic[T, TOrd]):
    pass


@dataclass
class _ORIntervalTree(_IntervalTreeImplementation[T, TOrd]):
    "Implementation of IntervalTree with open-right cells."

    center: t.Optional[TOrd]
    cells: t.Sequence[Cell[T, TOrd]]  # Ordered by lowerbound
    cells_by_upper: t.Sequence[
        Cell[T, TOrd]
    ]  # Ordered in reverse by upperbound.
    left: t.Optional[_ORIntervalTree]
    right: t.Optional[_ORIntervalTree]

    __slots__ = ("center", "cells", "cells_by_upper", "left", "right")

    @classmethod
    def from_cells(cls, cells: t.Sequence[Cell[T, TOrd]]) -> _ORIntervalTree:
        return cls._from_sorted_cells(
            sorted(tuple(cell for cell in cells if cell), key=_getlower)
        )

    def __bool__(self) -> bool:
        return bool(self.cells)

    def __contains__(self, which: TOrd):
        return bool(self.get(which))

    @classmethod
    def _from_sorted_cells(
        cls,
        cells: t.Sequence[Cell[T, TOrd]],
    ) -> _ORIntervalTree[T, TOrd]:
        with sentry_span("IntervalTree._from_sorted_cells"):
            left_cells = []
            middle_cells = []
            right_cells = []
            if cells:
                middle = len(cells) // 2
                middle_cell = cells[middle]
                center: t.Optional[TOrd] = middle_cell.lowerbound
                for cell in cells:
                    if cell.upperbound <= center:
                        left_cells.append(cell)
                    elif center < cell.lowerbound:
                        right_cells.append(cell)
                    else:
                        assert center in cell
                        middle_cells.append(cell)
            else:
                center = None
            result = cls(
                center=center,
                cells=tuple(middle_cells),
                cells_by_upper=tuple(
                    sorted(middle_cells, key=_getupper, reverse=True)
                ),
                left=cls._from_sorted_cells(left_cells) if left_cells else None,
                right=cls._from_sorted_cells(right_cells)
                if right_cells
                else None,
            )
            return result

    def __getitem__(self, which: TOrd) -> t.Tuple[Cell[T, TOrd], ...]:
        """Return all cells that contains the given item."""
        result = self.get(which)
        if not result:
            raise KeyError(which)
        return result

    def get(self, query: TOrd) -> t.Tuple[Cell[T, TOrd], ...]:
        with sentry_span("IntervalTree.get"):
            return tuple(self.iter_get(query))

    def iter_get(self, query: TOrd) -> t.Iterator[Cell[T, TOrd]]:
        if not self:
            return
        if query <= self.center:
            # Since self.cells is ordered by lowerbound, only *the first*
            # cells for which the lowerbound is less or equal to the query
            # contain the queried value.  Looking any further won't find any
            # match.
            #
            # See page 222 of [deBerg2008].
            yield from takewhile(lambda c: c.lowerbound <= query, self.cells)
        else:
            # The same as before but with `cells_by_upper`.
            yield from takewhile(
                lambda c: query < c.upperbound, self.cells_by_upper
            )
        if query < self.center and self.left:
            yield from self.left.get(query)
        elif query > self.center and self.right:
            yield from self.right.get(query)

    @property
    def depth(self):
        "The depth of the IntervalTree."
        return 1 + max(
            left.depth if (left := self.left) is not None else 0,
            right.depth if (right := self.right) is not None else 0,
        )


_getlower = operator.attrgetter("lowerbound")
_getupper = operator.attrgetter("upperbound")

sentry_span = get_module_sentry_spanner(__name__)
