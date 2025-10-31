"""
Chain of Responsibility Pattern - Pass request along chain of handlers.

Each handler decides whether to process the request or pass it to the next handler.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# Handler interface
class Handler(ABC):
    """Base handler in the chain."""

    def __init__(self) -> None:
        """Initialize handler."""
        self._next_handler: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """
        Set the next handler in the chain.

        Args:
            handler: Next handler

        Returns:
            The handler (for chaining)
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str | None:
        """
        Handle the request or pass to next handler.

        Args:
            request: Request to handle

        Returns:
            Response or None if not handled
        """
        pass


# Concrete handlers
class AuthenticationHandler(Handler):
    """Check if user is authenticated."""

    def handle(self, request: dict[str, Any]) -> str | None:
        """Handle authentication check."""
        if not request.get("authenticated"):
            return "Error: User not authenticated"

        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class AuthorizationHandler(Handler):
    """Check if user has permission."""

    def handle(self, request: dict[str, Any]) -> str | None:
        """Handle authorization check."""
        if request.get("role") != "admin":
            return "Error: Insufficient permissions"

        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class ValidationHandler(Handler):
    """Validate request data."""

    def handle(self, request: dict[str, Any]) -> str | None:
        """Handle data validation."""
        if not request.get("data"):
            return "Error: Invalid data"

        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class ProcessingHandler(Handler):
    """Process the request."""

    def handle(self, request: dict[str, Any]) -> str | None:
        """Handle request processing."""
        data = request.get("data", "")
        return f"Successfully processed: {data}"


# Pythonic approach: Using functions
def auth_middleware(request: dict[str, Any], next_handler: Any = None) -> str:
    """Authentication middleware."""
    if not request.get("authenticated"):
        return "Error: Not authenticated"
    return next_handler(request) if next_handler else "OK"


def role_middleware(request: dict[str, Any], next_handler: Any = None) -> str:
    """Authorization middleware."""
    if request.get("role") != "admin":
        return "Error: Not admin"
    return next_handler(request) if next_handler else "OK"


def process_request(request: dict[str, Any]) -> str:
    """Final processor."""
    return f"Processed: {request.get('data')}"


# Logger chain example
class LogLevel:
    """Log levels."""

    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class Logger(ABC):
    """Abstract logger in chain."""

    def __init__(self, level: int) -> None:
        """Initialize with log level."""
        self.level = level
        self._next_logger: Logger | None = None

    def set_next(self, logger: Logger) -> Logger:
        """Set next logger in chain."""
        self._next_logger = logger
        return logger

    def log(self, level: int, message: str) -> None:
        """Log message if level is appropriate."""
        if level >= self.level:
            self.write(message)

        if self._next_logger:
            self._next_logger.log(level, message)

    @abstractmethod
    def write(self, message: str) -> None:
        """Write log message."""
        pass


class ConsoleLogger(Logger):
    """Log to console."""

    def write(self, message: str) -> None:
        """Write to console."""
        print(f"Console: {message}")


class FileLogger(Logger):
    """Log to file."""

    def write(self, message: str) -> None:
        """Write to file."""
        print(f"File: {message}")


class ErrorLogger(Logger):
    """Log errors."""

    def write(self, message: str) -> None:
        """Write error."""
        print(f"ERROR: {message}")


def demonstrate_all() -> None:
    """Demonstrate Chain of Responsibility pattern."""
    print("=== Chain of Responsibility Pattern ===\n")

    # Request processing chain
    print("1. Request Processing Chain:")

    # Build chain
    auth = AuthenticationHandler()
    authz = AuthorizationHandler()
    validation = ValidationHandler()
    processing = ProcessingHandler()

    auth.set_next(authz).set_next(validation).set_next(processing)

    # Test requests
    request1 = {"authenticated": True, "role": "admin", "data": "important data"}
    print(f"   Valid request: {auth.handle(request1)}")

    request2 = {"authenticated": False, "role": "admin", "data": "data"}
    print(f"   Not authenticated: {auth.handle(request2)}")

    request3 = {"authenticated": True, "role": "user", "data": "data"}
    print(f"   Not authorized: {auth.handle(request3)}")
    print()

    # Logger chain
    print("2. Logger Chain:")

    console = ConsoleLogger(LogLevel.DEBUG)
    file = FileLogger(LogLevel.WARNING)
    error = ErrorLogger(LogLevel.ERROR)

    console.set_next(file).set_next(error)

    console.log(LogLevel.DEBUG, "Debug message")
    console.log(LogLevel.WARNING, "Warning message")
    console.log(LogLevel.ERROR, "Error message")


if __name__ == "__main__":
    demonstrate_all()
