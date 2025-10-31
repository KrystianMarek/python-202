"""
Singleton Pattern - Ensure a class has only one instance.

Pythonic approaches:
1. Module-level instance (most Pythonic)
2. Metaclass
3. Decorator
4. Borg pattern (shared state)
"""

from __future__ import annotations

import threading
from typing import Any


# Approach 1: Metaclass Singleton (thread-safe)
class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass.

    Why use a metaclass?
    - Controls class creation
    - Thread-safe with lock
    - Works with inheritance

    Trade-offs:
    - More complex than module-level
    - Harder to test (mocking issues)
    """

    _instances: dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Control instance creation.

        Thread-safe lazy initialization.
        """
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """
    Database connection using Singleton pattern.

    Examples:
        >>> db1 = DatabaseConnection("localhost")
        >>> db2 = DatabaseConnection("remotehost")  # Ignored, returns same instance
        >>> db1 is db2
        True
        >>> db1.host
        'localhost'
    """

    def __init__(self, host: str) -> None:
        """Initialize connection (only called once)."""
        # Note: __init__ is called every time __call__ is invoked
        # Only set attributes if not already set
        if not hasattr(self, "host"):
            self.host = host
            self.connected = True
            print(f"Connecting to database at {host}")

    def query(self, sql: str) -> str:
        """Execute a query."""
        return f"Executing query on {self.host}: {sql}"


# Approach 2: Decorator Singleton
def singleton[T](cls: type[T]) -> type[T]:
    """
    Singleton decorator.

    Why use a decorator?
    - Simple and explicit
    - Easy to apply to existing classes
    - Clear intent

    Args:
        cls: Class to make singleton

    Returns:
        Singleton class
    """
    instances: dict[type, Any] = {}
    lock = threading.Lock()

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore


@singleton
class ConfigManager:
    """
    Configuration manager using decorator pattern.

    Examples:
        >>> config1 = ConfigManager()
        >>> config1.set("key", "value")
        >>> config2 = ConfigManager()
        >>> config2.get("key")
        'value'
    """

    def __init__(self) -> None:
        """Initialize config manager."""
        self._config: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)


# Approach 3: Borg Pattern (Monostate)
class Borg:
    """
    Borg pattern - shared state instead of shared instance.

    Why Borg?
    - Multiple instances, shared state
    - More Pythonic than strict Singleton
    - Easier to subclass

    Anti-pattern for:
    - When you actually need unique instances
    - When state should be isolated
    """

    _shared_state: dict[str, Any] = {}

    def __init__(self) -> None:
        """Initialize with shared state."""
        self.__dict__ = self._shared_state


class AppSettings(Borg):
    """
    Application settings using Borg pattern.

    Examples:
        >>> settings1 = AppSettings()
        >>> settings1.theme = "dark"
        >>> settings2 = AppSettings()
        >>> settings2.theme
        'dark'
        >>> settings1 is settings2  # Different instances
        False
        >>> settings1.theme == settings2.theme  # Same state
        True
    """

    def __init__(self) -> None:
        """Initialize settings."""
        super().__init__()
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.theme = "light"
            self.language = "en"


# Approach 4: Module-level Singleton (most Pythonic)
class _Logger:
    """Private logger class."""

    def __init__(self) -> None:
        """Initialize logger."""
        self.logs: list[str] = []

    def log(self, message: str) -> None:
        """Add log message."""
        self.logs.append(message)
        print(f"LOG: {message}")

    def get_logs(self) -> list[str]:
        """Get all logs."""
        return self.logs.copy()


# Single module-level instance
logger = _Logger()


def get_logger() -> _Logger:
    """
    Get the logger instance.

    This is the most Pythonic way to implement Singleton:
    - Simple and explicit
    - No metaclass magic
    - Module is naturally a singleton

    Returns:
        The global logger instance

    Examples:
        >>> log1 = get_logger()
        >>> log2 = get_logger()
        >>> log1 is log2
        True
    """
    return logger


# Comparison and best practices
def demonstrate_all() -> None:
    """Demonstrate all Singleton approaches."""
    print("=== Singleton Pattern ===\n")

    # Metaclass approach
    print("1. Metaclass Singleton:")
    db1 = DatabaseConnection("localhost")
    db2 = DatabaseConnection("remotehost")
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   db1.host: {db1.host}\n")

    # Decorator approach
    print("2. Decorator Singleton:")
    config1 = ConfigManager()
    config1.set("api_key", "secret123")
    config2 = ConfigManager()
    print(f"   config2.get('api_key'): {config2.get('api_key')}\n")

    # Borg pattern
    print("3. Borg Pattern:")
    settings1 = AppSettings()
    settings1.theme = "dark"
    settings2 = AppSettings()
    print(f"   settings1 is settings2: {settings1 is settings2}")
    print(f"   Same state: {settings1.theme == settings2.theme}\n")

    # Module-level (most Pythonic)
    print("4. Module-level Singleton:")
    log1 = get_logger()
    log1.log("First message")
    log2 = get_logger()
    log2.log("Second message")
    print(f"   log1 is log2: {log1 is log2}")
    print(f"   Total logs: {len(log1.get_logs())}\n")


def test_thread_safety() -> None:
    """Test thread safety of Singleton implementation."""
    print("=== Testing Thread Safety ===\n")

    instances: list[DatabaseConnection] = []

    def create_instance() -> None:
        instance = DatabaseConnection("test")
        instances.append(instance)

    threads = [threading.Thread(target=create_instance) for _ in range(10)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # All instances should be the same object
    unique_ids = len({id(instance) for instance in instances})
    print(f"Created {len(instances)} references")
    print(f"Unique instances: {unique_ids}")
    print(f"Thread-safe: {unique_ids == 1}\n")


if __name__ == "__main__":
    demonstrate_all()
    test_thread_safety()
