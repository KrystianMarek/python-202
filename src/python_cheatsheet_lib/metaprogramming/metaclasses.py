"""
Metaclasses - Classes that create classes.

Metaclasses allow you to customize class creation and behavior.
"""

from __future__ import annotations

from typing import Any


# Basic metaclass
class Meta(type):
    """
    Basic metaclass example.

    Examples:
        >>> class MyClass(metaclass=Meta):
        ...     pass
        Creating class MyClass
    """

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        """Create new class."""
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, namespace)


# Registry metaclass
class PluginRegistry(type):
    """
    Metaclass that auto-registers classes.

    Examples:
        >>> class Plugin(metaclass=PluginRegistry):
        ...     plugins = {}
        >>> class EmailPlugin(Plugin):
        ...     plugin_name = "email"
        >>> class SMSPlugin(Plugin):
        ...     plugin_name = "sms"
        >>> Plugin.plugins
        {'email': <class '...EmailPlugin'>, 'sms': <class '...SMSPlugin'>}
    """

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        """Create and register class."""
        new_class = super().__new__(cls, name, bases, namespace)

        # Auto-register subclasses
        if bases and hasattr(new_class, "plugins"):
            if hasattr(new_class, "plugin_name"):
                new_class.plugins[new_class.plugin_name] = new_class  # type: ignore

        return new_class


# Singleton metaclass
class SingletonMeta(type):
    """
    Metaclass for singleton pattern.

    Examples:
        >>> class Config(metaclass=SingletonMeta):
        ...     def __init__(self):
        ...         self.value = 42
        >>> c1 = Config()
        >>> c2 = Config()
        >>> c1 is c2
        True
    """

    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Control instance creation."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# __init_subclass__ hook (modern alternative to metaclasses)
class Validator:
    """
    Base class with __init_subclass__ hook.

    Examples:
        >>> class EmailValidator(Validator):
        ...     pattern = r"^[\\w.-]+@[\\w.-]+\\.\\w+$"
        >>> EmailValidator.pattern
        '^[\\\\w.-]+@[\\w.-]+\\\\.\\w+$'
    """

    validators: dict[str, type[Validator]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Auto-register validators."""
        super().__init_subclass__(**kwargs)
        validator_name = cls.__name__.replace("Validator", "").lower()
        cls.validators[validator_name] = cls


class EmailValidator(Validator):
    """Email validator."""

    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"


class URLValidator(Validator):
    """URL validator."""

    pattern = r"^https?://[\w.-]+\.\w+"


def demonstrate_all() -> None:
    """Demonstrate metaclasses."""
    print("=== Metaclasses ===\n")

    # Plugin registry
    print("1. Plugin Registry:")

    class Plugin(metaclass=PluginRegistry):
        plugins: dict[str, type] = {}

    class CSVExporter(Plugin):
        plugin_name = "csv"

        def export(self) -> str:
            return "Exporting to CSV"

    class JSONExporter(Plugin):
        plugin_name = "json"

        def export(self) -> str:
            return "Exporting to JSON"

    print(f"   Registered plugins: {list(Plugin.plugins.keys())}")
    csv_plugin = Plugin.plugins["csv"]()
    print(f"   {csv_plugin.export()}")
    print()

    # Singleton
    print("2. Singleton via Metaclass:")

    class Database(metaclass=SingletonMeta):
        def __init__(self) -> None:
            self.connection = "postgresql://localhost"

    db1 = Database()
    db2 = Database()
    print(f"   db1 is db2: {db1 is db2}")
    print()

    # __init_subclass__
    print("3. __init_subclass__ Hook:")
    print(f"   Registered validators: {list(Validator.validators.keys())}")


if __name__ == "__main__":
    demonstrate_all()

