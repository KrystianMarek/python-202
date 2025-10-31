"""
Higher-order functions - functions that operate on other functions.

Includes map, filter, reduce, and custom higher-order functions.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def demonstrate_map() -> None:
    """Demonstrate map function."""
    print("1. Map:")
    numbers = [1, 2, 3, 4, 5]
    squared = [x**2 for x in numbers]
    print(f"   {numbers} -> {squared}")


def demonstrate_filter() -> None:
    """Demonstrate filter function."""
    print("\n2. Filter:")
    numbers = [1, 2, 3, 4, 5, 6]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"   Even numbers: {evens}")


def demonstrate_reduce() -> None:
    """Demonstrate reduce function."""
    print("\n3. Reduce:")
    numbers = [1, 2, 3, 4, 5]
    product = functools.reduce(lambda x, y: x * y, numbers)
    print(f"   Product: {product}")


def compose[T, R](*functions: Callable[[T], T]) -> Callable[[T], R]:
    """
    Compose functions from right to left.

    Examples:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = compose(double, add_one)
        >>> f(3)  # double(add_one(3)) = double(4) = 8
        8
    """

    def inner(arg: T) -> R:
        result = arg
        for f in reversed(functions):
            result = f(result)  # type: ignore
        return result  # type: ignore

    return inner


def demonstrate_all() -> None:
    """Demonstrate higher-order functions."""
    print("=== Higher-Order Functions ===\n")
    demonstrate_map()
    demonstrate_filter()
    demonstrate_reduce()

    print("\n4. Function Composition:")

    def add_one(x: int) -> int:
        return x + 1

    def double(x: int) -> int:
        return x * 2

    f = compose(double, add_one)
    result = f(3)
    print(f"   compose(double, add_one)(3) = {result}")


if __name__ == "__main__":
    demonstrate_all()

