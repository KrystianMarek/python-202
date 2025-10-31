"""
Basic OOP concepts in Python: classes, inheritance, properties, and more.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar


# Basic class example
class Person:
    """
    Basic class with instance and class attributes.

    Examples:
        >>> person = Person("Alice", 30)
        >>> person.name
        'Alice'
        >>> person.greet()
        'Hello, I am Alice'
    """

    species: ClassVar[str] = "Homo sapiens"  # Class attribute

    def __init__(self, name: str, age: int) -> None:
        """Initialize a person."""
        self.name = name  # Instance attribute
        self.age = age

    def greet(self) -> str:
        """Return a greeting."""
        return f"Hello, I am {self.name}"

    @classmethod
    def create_anonymous(cls) -> Person:
        """Factory method to create anonymous person."""
        return cls("Anonymous", 0)

    @staticmethod
    def is_adult(age: int) -> bool:
        """Check if age represents an adult."""
        return age >= 18


# Properties and descriptors
class Temperature:
    """
    Demonstrate properties and data validation.

    Examples:
        >>> temp = Temperature(25.0)
        >>> temp.celsius
        25.0
        >>> temp.fahrenheit
        77.0
    """

    def __init__(self, celsius: float) -> None:
        """Initialize temperature in Celsius."""
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set temperature in Celsius with validation."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature in Fahrenheit."""
        self.celsius = (value - 32) * 5 / 9


# Inheritance
class Animal(ABC):
    """Abstract base class for animals."""

    def __init__(self, name: str) -> None:
        """Initialize animal with name."""
        self.name = name

    @abstractmethod
    def make_sound(self) -> str:
        """Return the sound the animal makes."""
        pass

    def describe(self) -> str:
        """Describe the animal."""
        return f"{self.name} says {self.make_sound()}"


class Dog(Animal):
    """Dog implementation."""

    def make_sound(self) -> str:
        """Dogs bark."""
        return "Woof!"


class Cat(Animal):
    """Cat implementation."""

    def make_sound(self) -> str:
        """Cats meow."""
        return "Meow!"


# Dataclasses (Python 3.7+)
@dataclass
class Point:
    """
    2D point using dataclass.

    Examples:
        >>> p = Point(3.0, 4.0)
        >>> p.distance_from_origin()
        5.0
    """

    x: float
    y: float

    def distance_from_origin(self) -> float:
        """Calculate distance from origin."""
        return (self.x**2 + self.y**2) ** 0.5


@dataclass
class Inventory:
    """
    Inventory with default factory.

    Examples:
        >>> inv = Inventory("Warehouse A")
        >>> inv.add_item("Widget", 10)
        >>> inv.items["Widget"]
        10
    """

    name: str
    items: dict[str, int] = field(default_factory=dict)

    def add_item(self, item: str, quantity: int) -> None:
        """Add items to inventory."""
        self.items[item] = self.items.get(item, 0) + quantity


# Slots for memory optimization
class PointWithSlots:
    """
    Point class using __slots__ for memory efficiency.

    __slots__ prevents dynamic attribute creation and reduces memory overhead.

    Examples:
        >>> p = PointWithSlots(1.0, 2.0)
        >>> p.x
        1.0
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        """Initialize point."""
        self.x = x
        self.y = y


# Multiple inheritance and MRO
class Flyable:
    """Mixin for flying ability."""

    def fly(self) -> str:
        """Return flying action."""
        return "Flying through the air!"


class Swimmable:
    """Mixin for swimming ability."""

    def swim(self) -> str:
        """Return swimming action."""
        return "Swimming in the water!"


class Duck(Animal, Flyable, Swimmable):
    """Duck can fly and swim."""

    def make_sound(self) -> str:
        """Ducks quack."""
        return "Quack!"


# Special methods (dunder methods)
class Vector:
    """
    2D vector with operator overloading.

    Examples:
        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(3, 4)
        >>> v3 = v1 + v2
        >>> v3.x, v3.y
        (4, 6)
    """

    def __init__(self, x: float, y: float) -> None:
        """Initialize vector."""
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        """Add two vectors."""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vector:
        """Multiply vector by scalar."""
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        """String representation."""
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y


def demonstrate_all() -> None:
    """Demonstrate all OOP basics."""
    print("=== OOP Basics ===\n")

    # Basic class
    print("1. Basic Class:")
    person = Person("Alice", 30)
    print(f"   {person.greet()}")
    print(f"   Is adult: {Person.is_adult(person.age)}\n")

    # Properties
    print("2. Properties:")
    temp = Temperature(25.0)
    print(f"   {temp.celsius}°C = {temp.fahrenheit}°F\n")

    # Inheritance
    print("3. Inheritance:")
    dog = Dog("Buddy")
    cat = Cat("Whiskers")
    print(f"   {dog.describe()}")
    print(f"   {cat.describe()}\n")

    # Dataclasses
    print("4. Dataclasses:")
    point = Point(3.0, 4.0)
    print(f"   Point: {point}")
    print(f"   Distance: {point.distance_from_origin()}\n")

    # Multiple inheritance
    print("5. Multiple Inheritance:")
    duck = Duck("Donald")
    print(f"   {duck.describe()}")
    print(f"   {duck.fly()}")
    print(f"   {duck.swim()}\n")

    # Operator overloading
    print("6. Operator Overloading:")
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    v3 = v1 + v2
    print(f"   {v1} + {v2} = {v3}")


if __name__ == "__main__":
    demonstrate_all()
