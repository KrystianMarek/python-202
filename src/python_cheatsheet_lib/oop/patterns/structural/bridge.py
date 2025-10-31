"""
Bridge Pattern - Decouple abstraction from implementation.

Separates interface from implementation so both can vary independently.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# Implementation hierarchy
class Renderer(ABC):
    """Abstract renderer (implementation)."""

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        """Render a circle."""
        pass

    @abstractmethod
    def render_rectangle(self, width: float, height: float) -> str:
        """Render a rectangle."""
        pass


class SVGRenderer(Renderer):
    """SVG renderer implementation."""

    def render_circle(self, radius: float) -> str:
        """Render circle as SVG."""
        return f'<circle r="{radius}"/>'

    def render_rectangle(self, width: float, height: float) -> str:
        """Render rectangle as SVG."""
        return f'<rect width="{width}" height="{height}"/>'


class CanvasRenderer(Renderer):
    """Canvas renderer implementation."""

    def render_circle(self, radius: float) -> str:
        """Render circle on canvas."""
        return f"canvas.arc(0, 0, {radius}, 0, 2*Math.PI)"

    def render_rectangle(self, width: float, height: float) -> str:
        """Render rectangle on canvas."""
        return f"canvas.rect(0, 0, {width}, {height})"


class ASCIIRenderer(Renderer):
    """ASCII renderer implementation."""

    def render_circle(self, radius: float) -> str:
        """Render circle as ASCII."""
        return f"  ***\n *   *  (radius={radius})\n  ***"

    def render_rectangle(self, width: float, height: float) -> str:
        """Render rectangle as ASCII."""
        return f"+{'-' * int(width)}+\n|{' ' * int(width)}| (h={height})\n+{'-' * int(width)}+"


# Abstraction hierarchy
class Shape(ABC):
    """Abstract shape (abstraction)."""

    def __init__(self, renderer: Renderer) -> None:
        """Initialize shape with renderer."""
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        """Draw the shape."""
        pass


class Circle(Shape):
    """Circle shape."""

    def __init__(self, renderer: Renderer, radius: float) -> None:
        """Initialize circle."""
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        """Draw circle using renderer."""
        return self.renderer.render_circle(self.radius)


class Rectangle(Shape):
    """Rectangle shape."""

    def __init__(self, renderer: Renderer, width: float, height: float) -> None:
        """Initialize rectangle."""
        super().__init__(renderer)
        self.width = width
        self.height = height

    def draw(self) -> str:
        """Draw rectangle using renderer."""
        return self.renderer.render_rectangle(self.width, self.height)


def demonstrate_all() -> None:
    """Demonstrate Bridge pattern."""
    print("=== Bridge Pattern ===\n")

    # Same shape with different renderers
    print("1. Circle with different renderers:")
    circle = Circle(SVGRenderer(), 10)
    print(f"   SVG: {circle.draw()}")

    circle.renderer = CanvasRenderer()
    print(f"   Canvas: {circle.draw()}")

    circle.renderer = ASCIIRenderer()
    print(f"   ASCII:\n{circle.draw()}")
    print()

    print("2. Rectangle with different renderers:")
    rect = Rectangle(SVGRenderer(), 20, 10)
    print(f"   SVG: {rect.draw()}")

    rect.renderer = ASCIIRenderer()
    print(f"   ASCII:\n{rect.draw()}")


if __name__ == "__main__":
    demonstrate_all()

