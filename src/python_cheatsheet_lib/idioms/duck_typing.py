"""
Duck Typing - "If it walks like a duck and quacks like a duck, it's a duck."

Use Protocol for structural subtyping instead of explicit inheritance.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> str:
        """Draw the object."""
        ...


class Circle:
    """Circle doesn't inherit from anything."""

    def draw(self) -> str:
        """Draw circle."""
        return "Drawing circle"


class Square:
    """Square doesn't inherit from anything."""

    def draw(self) -> str:
        """Draw square."""
        return "Drawing square"


def render(obj: Drawable) -> str:
    """
    Render any drawable object.

    Uses duck typing - doesn't care about inheritance.

    Examples:
        >>> circle = Circle()
        >>> render(circle)
        'Drawing circle'
    """
    return obj.draw()


def demonstrate_all() -> None:
    """Demonstrate duck typing."""
    print("=== Duck Typing ===\n")

    shapes = [Circle(), Square()]
    for shape in shapes:
        print(f"   {render(shape)}")


if __name__ == "__main__":
    demonstrate_all()

