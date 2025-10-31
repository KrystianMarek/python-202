"""
Decorator Pattern - Add responsibilities to objects dynamically.

Note: This is the structural pattern, different from Python's @ decorator syntax,
though they share similar concepts.
"""

from __future__ import annotations

import functools
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar


# Structural Decorator Pattern (Classic GoF)
class Coffee(ABC):
    """Base coffee interface."""

    @abstractmethod
    def cost(self) -> float:
        """Get cost of coffee."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Get description."""
        pass


class SimpleCoffee(Coffee):
    """Basic coffee implementation."""

    def cost(self) -> float:
        """Base cost."""
        return 2.0

    def description(self) -> str:
        """Base description."""
        return "Simple coffee"


class CoffeeDecorator(Coffee):
    """Base decorator."""

    def __init__(self, coffee: Coffee) -> None:
        """Wrap a coffee object."""
        self._coffee = coffee

    def cost(self) -> float:
        """Delegate to wrapped coffee."""
        return self._coffee.cost()

    def description(self) -> str:
        """Delegate to wrapped coffee."""
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    """Add milk to coffee."""

    def cost(self) -> float:
        """Add milk cost."""
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        """Add milk to description."""
        return f"{self._coffee.description()}, milk"


class SugarDecorator(CoffeeDecorator):
    """Add sugar to coffee."""

    def cost(self) -> float:
        """Add sugar cost."""
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        """Add sugar to description."""
        return f"{self._coffee.description()}, sugar"


class WhipDecorator(CoffeeDecorator):
    """Add whipped cream to coffee."""

    def cost(self) -> float:
        """Add whip cost."""
        return self._coffee.cost() + 0.7

    def description(self) -> str:
        """Add whip to description."""
        return f"{self._coffee.description()}, whip"


# Pythonic Function Decorators
P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to time function execution.

    Examples:
        >>> @timer
        ... def slow_function():
        ...     time.sleep(0.1)
        ...     return 42
        >>> result = slow_function()  # doctest: +SKIP
        slow_function took 0.1000s
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            raise RuntimeError("Should not reach here")

        return wrapper

    return decorator


def cache_result(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Simple cache decorator.

    Examples:
        >>> @cache_result
        ... def expensive_computation(n: int) -> int:
        ...     print(f"Computing for {n}")
        ...     return n * n
        >>> expensive_computation(5)
        Computing for 5
        25
        >>> expensive_computation(5)  # Cached, no print
        25
    """
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create cache key from args
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    wrapper.cache = cache  # type: ignore
    return wrapper


# Class decorator
def singleton[T](cls: type[T]) -> type[T]:
    """
    Singleton class decorator.

    Examples:
        >>> @singleton
        ... class Database:
        ...     def __init__(self):
        ...         self.connection = "connected"
        >>> db1 = Database()
        >>> db2 = Database()
        >>> db1 is db2
        True
    """
    instances: dict[type, Any] = {}

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore


def demonstrate_all() -> None:
    """Demonstrate Decorator pattern."""
    print("=== Decorator Pattern ===\n")

    # Structural decorator (classic)
    print("1. Structural Decorator (Coffee):")
    coffee = SimpleCoffee()
    print(f"   {coffee.description()}: ${coffee.cost():.2f}")

    # Add milk
    coffee = MilkDecorator(coffee)
    print(f"   {coffee.description()}: ${coffee.cost():.2f}")

    # Add sugar and whip
    coffee = SugarDecorator(coffee)
    coffee = WhipDecorator(coffee)
    print(f"   {coffee.description()}: ${coffee.cost():.2f}")
    print()

    # Pythonic function decorators
    print("2. Function Decorators:")

    @timer
    def slow_computation() -> int:
        time.sleep(0.05)
        return sum(range(1000))

    result = slow_computation()
    print(f"   Result: {result}")
    print()

    # Cache decorator
    print("3. Cache Decorator:")

    @cache_result
    def fibonacci(n: int) -> int:
        print(f"   Computing fib({n})")
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(f"   fib(5) = {fibonacci(5)}")
    print(f"   fib(5) again = {fibonacci(5)}  # No recomputation")
    print()

    # Class decorator
    print("4. Class Decorator:")

    @singleton
    class Config:
        def __init__(self) -> None:
            self.setting = "default"

    config1 = Config()
    config2 = Config()
    print(f"   config1 is config2: {config1 is config2}")


if __name__ == "__main__":
    demonstrate_all()
