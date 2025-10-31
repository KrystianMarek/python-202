"""Tests for Factory Method pattern."""

from python_cheatsheet_lib.oop.patterns.creational.factory_method import (
    create_logger,
    Serializer,
)


def test_factory_function() -> None:
    """Test factory function creates correct logger types."""
    console_logger = create_logger("console")
    assert hasattr(console_logger, "log")

    file_logger = create_logger("file", filename="test.log")
    assert hasattr(file_logger, "log")


def test_registry_pattern() -> None:
    """Test registry pattern auto-registers subclasses."""
    assert "json" in Serializer._registry
    assert "xml" in Serializer._registry
    assert "yaml" in Serializer._registry

    serializer = Serializer.create("json")
    result = serializer.serialize({"key": "value"})
    assert "JSON" in result

