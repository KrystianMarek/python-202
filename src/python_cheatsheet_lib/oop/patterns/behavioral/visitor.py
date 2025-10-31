"""
Visitor Pattern - Separate algorithm from object structure.

Allows adding new operations to existing object structures without modifying them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# Element interface
class Shape(ABC):
    """Shape that can be visited."""

    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept a visitor."""
        pass


# Concrete elements
class Circle(Shape):
    """Circle shape."""

    def __init__(self, radius: float) -> None:
        """Initialize circle."""
        self.radius = radius

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor."""
        return visitor.visit_circle(self)


class Rectangle(Shape):
    """Rectangle shape."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle."""
        self.width = width
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor."""
        return visitor.visit_rectangle(self)


class Triangle(Shape):
    """Triangle shape."""

    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle."""
        self.base = base
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor."""
        return visitor.visit_triangle(self)


# Visitor interface
class ShapeVisitor(ABC):
    """Visitor for shapes."""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        """Visit circle."""
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Visit rectangle."""
        pass

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> str:
        """Visit triangle."""
        pass


# Concrete visitors
class AreaCalculator(ShapeVisitor):
    """Calculate area of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle area."""
        area = 3.14159 * circle.radius**2
        return f"Circle area: {area:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle area."""
        area = rectangle.width * rectangle.height
        return f"Rectangle area: {area:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle area."""
        area = 0.5 * triangle.base * triangle.height
        return f"Triangle area: {area:.2f}"


class PerimeterCalculator(ShapeVisitor):
    """Calculate perimeter of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle perimeter."""
        perimeter = 2 * 3.14159 * circle.radius
        return f"Circle perimeter: {perimeter:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle perimeter."""
        perimeter = 2 * (rectangle.width + rectangle.height)
        return f"Rectangle perimeter: {perimeter:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle perimeter (assuming equilateral)."""
        perimeter = 3 * triangle.base
        return f"Triangle perimeter: {perimeter:.2f}"


class SVGExporter(ShapeVisitor):
    """Export shapes to SVG."""

    def visit_circle(self, circle: Circle) -> str:
        """Export circle as SVG."""
        return f'<circle r="{circle.radius}"/>'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle as SVG."""
        return f'<rect width="{rectangle.width}" height="{rectangle.height}"/>'

    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle as SVG."""
        return f'<polygon points="0,{triangle.height} {triangle.base / 2},0 {triangle.base},{triangle.height}"/>'


# Pythonic alternative using match-case
def calculate_area_functional(shape: Shape) -> float:
    """Calculate area using pattern matching."""
    match shape:
        case Circle(radius=r):
            return 3.14159 * r**2
        case Rectangle(width=w, height=h):
            return w * h
        case Triangle(base=b, height=h):
            return 0.5 * b * h
        case _:
            return 0.0


def demonstrate_all() -> None:
    """Demonstrate Visitor pattern."""
    print("=== Visitor Pattern ===\n")

    # Create shapes
    shapes: list[Shape] = [
        Circle(5.0),
        Rectangle(4.0, 6.0),
        Triangle(3.0, 4.0),
    ]

    # Area calculator visitor
    print("1. Area Calculator:")
    area_calc = AreaCalculator()
    for shape in shapes:
        print(f"   {shape.accept(area_calc)}")
    print()

    # Perimeter calculator visitor
    print("2. Perimeter Calculator:")
    perimeter_calc = PerimeterCalculator()
    for shape in shapes:
        print(f"   {shape.accept(perimeter_calc)}")
    print()

    # SVG exporter visitor
    print("3. SVG Exporter:")
    svg_exporter = SVGExporter()
    for shape in shapes:
        print(f"   {shape.accept(svg_exporter)}")
    print()

    # Functional approach
    print("4. Functional Approach (match-case):")
    for shape in shapes:
        area = calculate_area_functional(shape)
        print(f"   {type(shape).__name__} area: {area:.2f}")


if __name__ == "__main__":
    demonstrate_all()

