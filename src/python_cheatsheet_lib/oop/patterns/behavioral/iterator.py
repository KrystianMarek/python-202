"""
Iterator Pattern - Access elements sequentially without exposing representation.

Provides a way to traverse a collection without exposing its internal structure.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TypeVar

T = TypeVar("T")


# Custom iterator
class Range:
    """
    Custom range iterator.

    Examples:
        >>> r = Range(0, 5)
        >>> list(r)
        [0, 1, 2, 3, 4]
    """

    def __init__(self, start: int, end: int, step: int = 1) -> None:
        """Initialize range."""
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self) -> Iterator[int]:
        """Return iterator."""
        current = self.start
        while current < self.end:
            yield current
            current += self.step


# Tree traversal iterator
class TreeNode[T]:
    """Tree node for demonstration."""

    def __init__(self, value: T) -> None:
        """Initialize node."""
        self.value = value
        self.children: list[TreeNode[T]] = []

    def add_child(self, child: TreeNode[T]) -> None:
        """Add child node."""
        self.children.append(child)

    def __iter__(self) -> Iterator[T]:
        """Depth-first traversal."""
        yield self.value
        for child in self.children:
            yield from child


# Reverse iterator
class ReversibleCollection[T]:
    """
    Collection with forward and reverse iteration.

    Examples:
        >>> col = ReversibleCollection([1, 2, 3])
        >>> list(col)
        [1, 2, 3]
        >>> list(col.reverse())
        [3, 2, 1]
    """

    def __init__(self, items: list[T]) -> None:
        """Initialize with items."""
        self._items = items

    def __iter__(self) -> Iterator[T]:
        """Forward iteration."""
        return iter(self._items)

    def reverse(self) -> Iterator[T]:
        """Reverse iteration."""
        return reversed(self._items)


def demonstrate_all() -> None:
    """Demonstrate Iterator pattern."""
    print("=== Iterator Pattern ===\n")

    print("1. Custom Range:")
    for i in Range(0, 10, 2):
        print(f"   {i}", end=" ")
    print("\n")

    print("2. Tree Traversal:")
    root = TreeNode("root")
    child1 = TreeNode("child1")
    child2 = TreeNode("child2")
    grandchild = TreeNode("grandchild")

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    for node in root:
        print(f"   {node}")
    print()

    print("3. Reversible Collection:")
    col = ReversibleCollection([1, 2, 3, 4, 5])
    print(f"   Forward: {list(col)}")
    print(f"   Reverse: {list(col.reverse())}")


if __name__ == "__main__":
    demonstrate_all()

