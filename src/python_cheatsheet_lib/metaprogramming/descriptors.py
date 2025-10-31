"""
Descriptors - Customize attribute access at the class level.

Descriptors are objects that define how attributes are accessed, set, or deleted.
"""

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


# Basic descriptor
class Verbose:
    """
    Descriptor that logs all access.

    Examples:
        >>> class MyClass:
        ...     x = Verbose("x")
        ...     def __init__(self):
        ...         self.x = 10
        >>> obj = MyClass()
        Getting x from <...>
        >>> obj.x
        10
    """

    def __init__(self, name: str) -> None:
        """Initialize descriptor."""
        self.name = name

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class."""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Get attribute value."""
        if obj is None:
            return self
        print(f"Getting {self.name} from {obj}")
        return obj.__dict__.get(self.name)

    def __set__(self, obj: Any, value: Any) -> None:
        """Set attribute value."""
        print(f"Setting {self.name} to {value}")
        obj.__dict__[self.name] = value

    def __delete__(self, obj: Any) -> None:
        """Delete attribute."""
        print(f"Deleting {self.name}")
        del obj.__dict__[self.name]


# Validated descriptor
class TypedProperty[T]:
    """
    Type-validated descriptor.

    Examples:
        >>> class Person:
        ...     name = TypedProperty(str)
        ...     age = TypedProperty(int)
        >>> p = Person()
        >>> p.name = "Alice"
        >>> p.age = 30
        >>> p.age = "thirty"  # doctest: +SKIP
        Traceback: TypeError
    """

    def __init__(self, expected_type: type[T]) -> None:
        """Initialize with expected type."""
        self.expected_type = expected_type
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store attribute name."""
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> T:
        """Get value."""
        if obj is None:
            return self  # type: ignore
        return getattr(obj, self.name, None)

    def __set__(self, obj: Any, value: T) -> None:
        """Set value with type checking."""
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, " f"got {type(value).__name__}"
            )
        setattr(obj, self.name, value)


# Lazy property descriptor
class LazyProperty:
    """
    Lazy evaluation descriptor.

    Computes value only once, on first access.

    Examples:
        >>> class DataLoader:
        ...     @LazyProperty
        ...     def data(self):
        ...         print("Loading data...")
        ...         return [1, 2, 3]
        >>> loader = DataLoader()
        >>> loader.data  # First access
        Loading data...
        [1, 2, 3]
        >>> loader.data  # Cached
        [1, 2, 3]
    """

    def __init__(self, func: Any) -> None:
        """Initialize with function."""
        self.func = func
        self.name = func.__name__

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Lazy evaluation."""
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value


# Cached property (similar to functools.cached_property)
class CachedProperty:
    """
    Cached property descriptor.

    Examples:
        >>> class ExpensiveComputation:
        ...     @CachedProperty
        ...     def result(self):
        ...         print("Computing...")
        ...         return 42
        >>> comp = ExpensiveComputation()
        >>> comp.result
        Computing...
        42
        >>> comp.result  # Cached
        42
    """

    def __init__(self, func: Any) -> None:
        """Initialize with function."""
        self.func = func
        self.attrname = None

    def __set_name__(self, owner: type, name: str) -> None:
        """Store attribute name."""
        self.attrname = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Get cached value or compute."""
        if obj is None:
            return self

        if self.attrname is None:
            raise TypeError("Cannot use CachedProperty instance without calling __set_name__")

        cache = obj.__dict__
        if self.attrname not in cache:
            cache[self.attrname] = self.func(obj)

        return cache[self.attrname]


# Range-validated descriptor
class RangeValidated:
    """
    Descriptor with range validation.

    Examples:
        >>> class Temperature:
        ...     celsius = RangeValidated(-273.15, 1000.0)
        >>> temp = Temperature()
        >>> temp.celsius = 25.0
        >>> temp.celsius
        25.0
    """

    def __init__(self, min_value: float, max_value: float) -> None:
        """Initialize with min/max values."""
        self.min_value = min_value
        self.max_value = max_value
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store attribute name."""
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> float:
        """Get value."""
        if obj is None:
            return self  # type: ignore
        return getattr(obj, self.name, 0.0)

    def __set__(self, obj: Any, value: float) -> None:
        """Set value with range validation."""
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Value must be between {self.min_value} and {self.max_value}")
        setattr(obj, self.name, value)


def demonstrate_all() -> None:
    """Demonstrate descriptors."""
    print("=== Descriptors ===\n")

    # Type-validated property
    print("1. Type-Validated Property:")

    class Person:
        name = TypedProperty(str)
        age = TypedProperty(int)

        def __init__(self, name: str, age: int) -> None:
            self.name = name
            self.age = age

    person = Person("Alice", 30)
    print(f"   Name: {person.name}, Age: {person.age}")

    try:
        person.age = "thirty"  # type: ignore
    except TypeError as e:
        print(f"   Error: {e}")
    print()

    # Lazy property
    print("2. Lazy Property:")

    class DataLoader:
        @LazyProperty
        def expensive_data(self) -> list[int]:
            print("   Loading expensive data...")
            return [1, 2, 3, 4, 5]

    loader = DataLoader()
    print("   First access:")
    data1 = loader.expensive_data
    print(f"   Data: {data1}")
    print("   Second access (cached):")
    data2 = loader.expensive_data
    print(f"   Data: {data2}")
    print()

    # Range-validated property
    print("3. Range-Validated Property:")

    class Temperature:
        celsius = RangeValidated(-273.15, 1000.0)

    temp = Temperature()
    temp.celsius = 25.0
    print(f"   Valid temperature: {temp.celsius}°C")

    try:
        temp.celsius = -300.0
    except ValueError as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    demonstrate_all()
