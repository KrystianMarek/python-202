"""
Abstract Factory Pattern - Create families of related objects.

Provides an interface for creating families of related or dependent objects
without specifying their concrete classes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol


# Product protocols
class Button(Protocol):
    """Button interface."""

    def render(self) -> str:
        """Render the button."""
        ...

    def click(self) -> str:
        """Handle click event."""
        ...


class Checkbox(Protocol):
    """Checkbox interface."""

    def render(self) -> str:
        """Render the checkbox."""
        ...

    def check(self) -> str:
        """Handle check event."""
        ...


# Windows products
class WindowsButton:
    """Windows-style button."""

    def render(self) -> str:
        """Render Windows button."""
        return "[Windows Button]"

    def click(self) -> str:
        """Windows click sound."""
        return "Windows: Click!"


class WindowsCheckbox:
    """Windows-style checkbox."""

    def render(self) -> str:
        """Render Windows checkbox."""
        return "[X] Windows Checkbox"

    def check(self) -> str:
        """Windows check sound."""
        return "Windows: Checked!"


# macOS products
class MacOSButton:
    """macOS-style button."""

    def render(self) -> str:
        """Render macOS button."""
        return "( macOS Button )"

    def click(self) -> str:
        """macOS click sound."""
        return "macOS: Click!"


class MacOSCheckbox:
    """macOS-style checkbox."""

    def render(self) -> str:
        """Render macOS checkbox."""
        return "☑ macOS Checkbox"

    def check(self) -> str:
        """macOS check sound."""
        return "macOS: Checked!"


# Linux products
class LinuxButton:
    """Linux-style button."""

    def render(self) -> str:
        """Render Linux button."""
        return "< Linux Button >"

    def click(self) -> str:
        """Linux click sound."""
        return "Linux: Click!"


class LinuxCheckbox:
    """Linux-style checkbox."""

    def render(self) -> str:
        """Render Linux checkbox."""
        return "[✓] Linux Checkbox"

    def check(self) -> str:
        """Linux check sound."""
        return "Linux: Checked!"


# Abstract Factory
class GUIFactory(ABC):
    """
    Abstract factory for creating GUI components.

    Why use Abstract Factory?
    - Create families of related objects
    - Ensure consistency across products
    - Easy to add new product families
    - Decouples client code from concrete classes
    """

    @abstractmethod
    def create_button(self) -> Button:
        """Create a button."""
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox."""
        pass


# Concrete Factories
class WindowsFactory(GUIFactory):
    """Factory for Windows GUI components."""

    def create_button(self) -> Button:
        """Create Windows button."""
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        """Create Windows checkbox."""
        return WindowsCheckbox()


class MacOSFactory(GUIFactory):
    """Factory for macOS GUI components."""

    def create_button(self) -> Button:
        """Create macOS button."""
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        """Create macOS checkbox."""
        return MacOSCheckbox()


class LinuxFactory(GUIFactory):
    """Factory for Linux GUI components."""

    def create_button(self) -> Button:
        """Create Linux button."""
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        """Create Linux checkbox."""
        return LinuxCheckbox()


# Client code
class Application:
    """
    Application that uses GUI factory.

    Demonstrates how client code works with abstract factory.

    Examples:
        >>> factory = WindowsFactory()
        >>> app = Application(factory)
        >>> app.render()
        'UI: [Windows Button] [X] Windows Checkbox'
    """

    def __init__(self, factory: GUIFactory) -> None:
        """
        Initialize application with a factory.

        Args:
            factory: GUI factory to use
        """
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render(self) -> str:
        """Render the UI."""
        return f"UI: {self.button.render()} {self.checkbox.render()}"

    def interact(self) -> str:
        """Simulate user interaction."""
        click_result = self.button.click()
        check_result = self.checkbox.check()
        return f"{click_result} | {check_result}"


# Factory selector
def get_factory(platform: str) -> GUIFactory:
    """
    Get appropriate factory for platform.

    Args:
        platform: Platform name ("windows", "macos", "linux")

    Returns:
        Appropriate GUI factory

    Raises:
        ValueError: If platform is unknown

    Examples:
        >>> factory = get_factory("windows")
        >>> isinstance(factory, WindowsFactory)
        True
    """
    factories: dict[str, type[GUIFactory]] = {
        "windows": WindowsFactory,
        "macos": MacOSFactory,
        "linux": LinuxFactory,
    }

    factory_class = factories.get(platform.lower())
    if not factory_class:
        raise ValueError(f"Unknown platform: {platform}")

    return factory_class()


# Alternative: Database connection example
class Database(Protocol):
    """Database interface."""

    def connect(self) -> str:
        """Connect to database."""
        ...

    def query(self, sql: str) -> str:
        """Execute query."""
        ...


class Cache(Protocol):
    """Cache interface."""

    def get(self, key: str) -> str | None:
        """Get value from cache."""
        ...

    def set(self, key: str, value: str) -> None:
        """Set value in cache."""
        ...


# MySQL family
class MySQLDatabase:
    """MySQL database."""

    def connect(self) -> str:
        """Connect to MySQL."""
        return "Connected to MySQL"

    def query(self, sql: str) -> str:
        """Execute MySQL query."""
        return f"MySQL query: {sql}"


class RedisCache:
    """Redis cache."""

    def __init__(self) -> None:
        """Initialize Redis cache."""
        self._data: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        """Get from Redis."""
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        """Set in Redis."""
        self._data[key] = value


# PostgreSQL family
class PostgreSQLDatabase:
    """PostgreSQL database."""

    def connect(self) -> str:
        """Connect to PostgreSQL."""
        return "Connected to PostgreSQL"

    def query(self, sql: str) -> str:
        """Execute PostgreSQL query."""
        return f"PostgreSQL query: {sql}"


class MemcachedCache:
    """Memcached cache."""

    def __init__(self) -> None:
        """Initialize Memcached."""
        self._data: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        """Get from Memcached."""
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        """Set in Memcached."""
        self._data[key] = value


class DatabaseFactory(ABC):
    """Abstract factory for database and cache."""

    @abstractmethod
    def create_database(self) -> Database:
        """Create database connection."""
        pass

    @abstractmethod
    def create_cache(self) -> Cache:
        """Create cache connection."""
        pass


class MySQLStackFactory(DatabaseFactory):
    """Factory for MySQL + Redis stack."""

    def create_database(self) -> Database:
        """Create MySQL database."""
        return MySQLDatabase()

    def create_cache(self) -> Cache:
        """Create Redis cache."""
        return RedisCache()


class PostgreSQLStackFactory(DatabaseFactory):
    """Factory for PostgreSQL + Memcached stack."""

    def create_database(self) -> Database:
        """Create PostgreSQL database."""
        return PostgreSQLDatabase()

    def create_cache(self) -> Cache:
        """Create Memcached cache."""
        return MemcachedCache()


def demonstrate_all() -> None:
    """Demonstrate Abstract Factory pattern."""
    print("=== Abstract Factory Pattern ===\n")

    # GUI example
    print("1. GUI Factory:")
    for platform in ["windows", "macos", "linux"]:
        factory = get_factory(platform)
        app = Application(factory)
        print(f"   {platform.capitalize()}: {app.render()}")
        print(f"   Interaction: {app.interact()}")
    print()

    # Database stack example
    print("2. Database Stack Factory:")
    mysql_factory = MySQLStackFactory()
    db = mysql_factory.create_database()
    cache = mysql_factory.create_cache()
    print(f"   {db.connect()}")
    print(f"   {db.query('SELECT * FROM users')}")
    cache.set("user:1", "Alice")
    print(f"   Cache get: {cache.get('user:1')}")
    print()

    pg_factory = PostgreSQLStackFactory()
    db2 = pg_factory.create_database()
    print(f"   {db2.connect()}")


if __name__ == "__main__":
    demonstrate_all()

