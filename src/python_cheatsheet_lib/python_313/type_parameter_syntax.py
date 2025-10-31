"""
PEP 695: Type Parameter Syntax (Python 3.12+, enhanced in 3.13).

New simplified syntax for generic classes, functions, and type aliases.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

# Traditional approach (pre-PEP 695)
T = TypeVar("T")
U = TypeVar("U")


def old_style_identity(value: T) -> T:
    """Old-style generic function using TypeVar."""
    return value


# PEP 695: New simplified syntax
def identity[T](value: T) -> T:
    """
    New-style generic function with inline type parameter.

    Why?
    - More concise and readable
    - Type parameter scope is limited to the function
    - No need to define TypeVar separately
    - Better IDE support

    Args:
        value: Any value of type T

    Returns:
        The same value

    Examples:
        >>> identity(42)
        42
        >>> identity("hello")
        'hello'
    """
    return value


def first[T](items: list[T]) -> T | None:
    """
    Get first item from a list using new type parameter syntax.

    Args:
        items: List of items of type T

    Returns:
        First item or None if empty

    Examples:
        >>> first([1, 2, 3])
        1
        >>> first([]) is None
        True
    """
    return items[0] if items else None


def map_values[K, V, R](mapping: dict[K, V], func: callable[[V], R]) -> dict[K, R]:
    """
    Transform dictionary values using a function.

    Demonstrates multiple type parameters with new syntax.

    Args:
        mapping: Input dictionary
        func: Transformation function

    Returns:
        New dictionary with transformed values

    Examples:
        >>> map_values({"a": 1, "b": 2}, lambda x: x * 2)
        {'a': 2, 'b': 4}
    """
    return {k: func(v) for k, v in mapping.items()}


# Generic classes with new syntax
class Stack[T]:
    """
    Generic stack implementation using PEP 695 syntax.

    Why?
    - Type parameter is part of class definition
    - Clearer than TypeVar approach
    - Better scoping

    Examples:
        >>> stack = Stack[int]()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.pop()
        2
        >>> stack.pop()
        1
    """

    def __init__(self) -> None:
        """Initialize empty stack."""
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Add item to stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return top item."""
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T | None:
        """Return top item without removing it."""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        """Return number of items in stack."""
        return len(self._items)


class Pair[T, U]:
    """
    Generic pair with two different types.

    Examples:
        >>> pair = Pair(1, "one")
        >>> pair.first
        1
        >>> pair.second
        'one'
    """

    def __init__(self, first: T, second: U) -> None:
        """
        Initialize pair.

        Args:
            first: First value of type T
            second: Second value of type U
        """
        self.first = first
        self.second = second

    def swap(self) -> Pair[U, T]:
        """
        Return a new pair with swapped values.

        Returns:
            New Pair with first and second swapped
        """
        return Pair(self.second, self.first)


# Type aliases with new syntax
type Point2D = tuple[float, float]
type Point3D = tuple[float, float, float]
type Matrix[T] = list[list[T]]
type JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def distance_2d(p1: Point2D, p2: Point2D) -> float:
    """
    Calculate Euclidean distance between two 2D points.

    Args:
        p1: First point
        p2: Second point

    Returns:
        Distance between points

    Examples:
        >>> distance_2d((0.0, 0.0), (3.0, 4.0))
        5.0
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def create_matrix[T](rows: int, cols: int, default: T) -> Matrix[T]:
    """
    Create a matrix filled with default value.

    Args:
        rows: Number of rows
        cols: Number of columns
        default: Default value for cells

    Returns:
        Matrix filled with default values

    Examples:
        >>> create_matrix(2, 3, 0)
        [[0, 0, 0], [0, 0, 0]]
    """
    return [[default for _ in range(cols)] for _ in range(rows)]


# Bounded type parameters
class Comparable[T: (int, float, str)]:
    """
    Generic class with bounded type parameter.

    Type T must be int, float, or str.

    Examples:
        >>> comp = Comparable(42)
        >>> comp.value
        42
    """

    def __init__(self, value: T) -> None:
        """Initialize with comparable value."""
        self.value = value

    def is_greater_than(self, other: T) -> bool:
        """Check if this value is greater than other."""
        return self.value > other


# Protocol with type parameters
class Container[T](Protocol):
    """
    Protocol for container types.

    Any class implementing __len__ and __getitem__ satisfies this protocol.
    """

    def __len__(self) -> int:
        """Return number of items."""
        ...

    def __getitem__(self, index: int) -> T:
        """Get item at index."""
        ...


def get_first_three[T](container: Container[T]) -> list[T]:
    """
    Get first three items from any container.

    Args:
        container: Any object implementing Container protocol

    Returns:
        List of up to 3 items

    Examples:
        >>> get_first_three([1, 2, 3, 4, 5])
        [1, 2, 3]
        >>> get_first_three("hello")
        ['h', 'e', 'l']
    """
    return [container[i] for i in range(min(3, len(container)))]


def demonstrate_all() -> None:
    """Demonstrate all type parameter syntax features."""
    print("=== PEP 695 Type Parameter Syntax ===\n")

    # Generic functions
    print("1. Generic Functions:")
    print(f"   identity(42) = {identity(42)}")
    print(f"   identity('hello') = {identity('hello')}")
    print(f"   first([1, 2, 3]) = {first([1, 2, 3])}")
    print()

    # Multiple type parameters
    print("2. Multiple Type Parameters:")
    result = map_values({"a": 1, "b": 2, "c": 3}, lambda x: x * 2)
    print(f"   map_values({{'a': 1, 'b': 2, 'c': 3}}, x*2) = {result}")
    print()

    # Generic classes
    print("3. Generic Classes:")
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print("   Stack operations: pushed 1, 2, 3")
    print(f"   pop() = {stack.pop()}")
    print(f"   peek() = {stack.peek()}")
    print()

    # Pair class
    print("4. Pair Class:")
    pair = Pair(42, "answer")
    print(f"   Pair(42, 'answer').first = {pair.first}")
    print(f"   Pair(42, 'answer').second = {pair.second}")
    swapped = pair.swap()
    print(f"   After swap: ({swapped.first}, {swapped.second})")
    print()

    # Type aliases
    print("5. Type Aliases:")
    p1: Point2D = (0.0, 0.0)
    p2: Point2D = (3.0, 4.0)
    print(f"   distance_2d({p1}, {p2}) = {distance_2d(p1, p2)}")
    matrix = create_matrix(2, 3, 0)
    print(f"   create_matrix(2, 3, 0) = {matrix}")
    print()

    # Bounded type parameters
    print("6. Bounded Type Parameters:")
    comp = Comparable(10)
    print(f"   Comparable(10).is_greater_than(5) = {comp.is_greater_than(5)}")
    print()

    # Protocol with type parameters
    print("7. Protocol with Type Parameters:")
    print(f"   get_first_three([1, 2, 3, 4, 5]) = {get_first_three([1, 2, 3, 4, 5])}")
    print(f"   get_first_three('hello world') = {get_first_three('hello world')}")


if __name__ == "__main__":
    demonstrate_all()

