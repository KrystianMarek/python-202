"""
Factory Method Pattern - Define an interface for creating objects.

Pythonic approaches:
1. Using @classmethod
2. Using Protocol for duck typing
3. Using __init_subclass__ hooks
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# Protocol-based approach (most Pythonic)
@runtime_checkable
class Logger(Protocol):
    """Protocol for logger objects."""

    def log(self, message: str) -> None:
        """Log a message."""
        ...

    def close(self) -> None:
        """Close the logger."""
        ...


class FileLogger:
    """
    Log to a file.

    Examples:
        >>> logger = FileLogger("app.log")
        >>> logger.log("Test message")
        FileLogger(app.log): Test message
        >>> logger.close()
        Closing file: app.log
    """

    def __init__(self, filename: str) -> None:
        """Initialize file logger."""
        self.filename = filename
        print(f"Opening file: {filename}")

    def log(self, message: str) -> None:
        """Write to file."""
        print(f"FileLogger({self.filename}): {message}")

    def close(self) -> None:
        """Close file."""
        print(f"Closing file: {self.filename}")


class ConsoleLogger:
    """
    Log to console.

    Examples:
        >>> logger = ConsoleLogger()
        >>> logger.log("Test message")
        ConsoleLogger: Test message
    """

    def __init__(self) -> None:
        """Initialize console logger."""
        print("Console logger ready")

    def log(self, message: str) -> None:
        """Write to console."""
        print(f"ConsoleLogger: {message}")

    def close(self) -> None:
        """Console logger doesn't need closing."""
        pass


class DatabaseLogger:
    """Log to database."""

    def __init__(self, connection_string: str) -> None:
        """Initialize database logger."""
        self.connection_string = connection_string
        print(f"Connected to database: {connection_string}")

    def log(self, message: str) -> None:
        """Write to database."""
        print(f"DatabaseLogger({self.connection_string}): {message}")

    def close(self) -> None:
        """Close database connection."""
        print(f"Closing database connection: {self.connection_string}")


# Factory function (simple approach)
def create_logger(logger_type: str, **kwargs: str) -> Logger:
    """
    Factory function for creating loggers.

    Why use a factory function?
    - Simple and Pythonic
    - Easy to extend
    - No class hierarchy needed

    Args:
        logger_type: Type of logger ("file", "console", "database")
        **kwargs: Arguments for logger initialization

    Returns:
        Logger instance

    Raises:
        ValueError: If logger type is unknown

    Examples:
        >>> logger = create_logger("console")
        Console logger ready
        >>> logger.log("Hello")
        ConsoleLogger: Hello
    """
    match logger_type.lower():
        case "file":
            return FileLogger(kwargs.get("filename", "default.log"))
        case "console":
            return ConsoleLogger()
        case "database":
            return DatabaseLogger(kwargs.get("connection_string", "localhost"))
        case _:
            raise ValueError(f"Unknown logger type: {logger_type}")


# Class-based approach with ABC
class Document(ABC):
    """Abstract document class."""

    def __init__(self, title: str) -> None:
        """Initialize document."""
        self.title = title

    @abstractmethod
    def render(self) -> str:
        """Render the document."""
        pass


class PDFDocument(Document):
    """PDF document implementation."""

    def render(self) -> str:
        """Render as PDF."""
        return f"PDF Document: {self.title}"


class WordDocument(Document):
    """Word document implementation."""

    def render(self) -> str:
        """Render as Word."""
        return f"Word Document: {self.title}"


class HTMLDocument(Document):
    """HTML document implementation."""

    def render(self) -> str:
        """Render as HTML."""
        return f"<html><title>{self.title}</title></html>"


class DocumentCreator(ABC):
    """
    Abstract creator with factory method.

    Why use abstract creator?
    - Enforces factory method in subclasses
    - Good for framework design
    - Allows customization in subclasses
    """

    @abstractmethod
    def create_document(self, title: str) -> Document:
        """Factory method to create document."""
        pass

    def process_document(self, title: str) -> str:
        """Template method using factory method."""
        doc = self.create_document(title)
        return doc.render()


class PDFCreator(DocumentCreator):
    """Creator for PDF documents."""

    def create_document(self, title: str) -> Document:
        """Create PDF document."""
        return PDFDocument(title)


class WordCreator(DocumentCreator):
    """Creator for Word documents."""

    def create_document(self, title: str) -> Document:
        """Create Word document."""
        return WordDocument(title)


class HTMLCreator(DocumentCreator):
    """Creator for HTML documents."""

    def create_document(self, title: str) -> Document:
        """Create HTML document."""
        return HTMLDocument(title)


# Registry pattern with @classmethod
class Serializer:
    """Base serializer with registry pattern."""

    _registry: dict[str, type[Serializer]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Auto-register subclasses."""
        super().__init_subclass__(**kwargs)
        # Extract format name from class name (e.g., JSONSerializer -> json)
        format_name = cls.__name__.replace("Serializer", "").lower()
        cls._registry[format_name] = cls

    @classmethod
    def create(cls, format_type: str) -> Serializer:
        """
        Factory method using registry.

        Args:
            format_type: Format type (json, xml, yaml)

        Returns:
            Serializer instance

        Examples:
            >>> serializer = Serializer.create("json")
            >>> serializer.serialize({"key": "value"})
            'JSON: {"key": "value"}'
        """
        serializer_class = cls._registry.get(format_type.lower())
        if not serializer_class:
            raise ValueError(f"Unknown format: {format_type}")
        return serializer_class()

    @abstractmethod
    def serialize(self, data: object) -> str:
        """Serialize data."""
        pass


class JSONSerializer(Serializer):
    """JSON serializer."""

    def serialize(self, data: object) -> str:
        """Serialize to JSON."""
        return f"JSON: {data}"


class XMLSerializer(Serializer):
    """XML serializer."""

    def serialize(self, data: object) -> str:
        """Serialize to XML."""
        return f"XML: {data}"


class YAMLSerializer(Serializer):
    """YAML serializer."""

    def serialize(self, data: object) -> str:
        """Serialize to YAML."""
        return f"YAML: {data}"


def demonstrate_all() -> None:
    """Demonstrate all factory method approaches."""
    print("=== Factory Method Pattern ===\n")

    # Simple factory function
    print("1. Factory Function:")
    logger1 = create_logger("console")
    logger1.log("Message from console")
    logger2 = create_logger("file", filename="app.log")
    logger2.log("Message to file")
    print()

    # Abstract creator pattern
    print("2. Abstract Creator:")
    pdf_creator = PDFCreator()
    word_creator = WordCreator()
    print(f"   {pdf_creator.process_document('Report')}")
    print(f"   {word_creator.process_document('Letter')}")
    print()

    # Registry pattern
    print("3. Registry Pattern:")
    json_serializer = Serializer.create("json")
    xml_serializer = Serializer.create("xml")
    print(f"   {json_serializer.serialize({'name': 'Alice'})}")
    print(f"   {xml_serializer.serialize({'name': 'Bob'})}")
    print()

    # Show registry
    print("4. Available serializers:")
    for format_type in Serializer._registry.keys():
        print(f"   - {format_type}")


if __name__ == "__main__":
    demonstrate_all()

