"""
Proxy Pattern - Provide surrogate or placeholder for another object.

Controls access to the original object, allowing additional functionality
like lazy loading, access control, caching, or logging.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any


# Subject interface
class Image(ABC):
    """Image interface."""

    @abstractmethod
    def display(self) -> str:
        """Display the image."""
        pass


# Real subject
class RealImage(Image):
    """
    Real image that loads from disk (expensive operation).

    Examples:
        >>> img = RealImage("photo.jpg")
        Loading image from disk: photo.jpg
        >>> img.display()
        'Displaying: photo.jpg'
    """

    def __init__(self, filename: str) -> None:
        """Load image from disk."""
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Expensive operation to load image."""
        print(f"Loading image from disk: {self.filename}")
        time.sleep(0.1)  # Simulate slow load

    def display(self) -> str:
        """Display the image."""
        return f"Displaying: {self.filename}"


# Virtual Proxy (lazy loading)
class ImageProxy(Image):
    """
    Proxy that delays loading until needed.

    Examples:
        >>> proxy = ImageProxy("large_photo.jpg")
        >>> # No loading yet!
        >>> result = proxy.display()  # Now it loads
        Loading image from disk: large_photo.jpg
        >>> result
        'Displaying: large_photo.jpg'
        >>> proxy.display()  # Cached, no reload
        'Displaying: large_photo.jpg'
    """

    def __init__(self, filename: str) -> None:
        """Initialize proxy without loading image."""
        self.filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> str:
        """Display image, loading if necessary."""
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()


# Protection Proxy (access control)
class Document(ABC):
    """Document interface."""

    @abstractmethod
    def read(self) -> str:
        """Read document."""
        pass

    @abstractmethod
    def write(self, content: str) -> str:
        """Write to document."""
        pass


class RealDocument(Document):
    """Real document implementation."""

    def __init__(self, title: str) -> None:
        """Initialize document."""
        self.title = title
        self.content = f"Content of {title}"

    def read(self) -> str:
        """Read document."""
        return self.content

    def write(self, content: str) -> str:
        """Write to document."""
        self.content = content
        return f"Written to {self.title}"


class ProtectedDocument(Document):
    """
    Proxy with access control.

    Examples:
        >>> doc = RealDocument("secret.txt")
        >>> proxy = ProtectedDocument(doc, user_role="admin")
        >>> proxy.read()
        'Content of secret.txt'
        >>> proxy.write("New content")
        'Written to secret.txt'
        >>> guest_proxy = ProtectedDocument(doc, user_role="guest")
        >>> guest_proxy.write("Hacked!")
        'Access denied: guest cannot write'
    """

    def __init__(self, document: RealDocument, user_role: str) -> None:
        """Initialize with document and user role."""
        self._document = document
        self._user_role = user_role

    def read(self) -> str:
        """Anyone can read."""
        return self._document.read()

    def write(self, content: str) -> str:
        """Only admin can write."""
        if self._user_role == "admin":
            return self._document.write(content)
        else:
            return f"Access denied: {self._user_role} cannot write"


# Caching Proxy
class DatabaseQuery(ABC):
    """Database query interface."""

    @abstractmethod
    def execute(self, sql: str) -> list[dict[str, Any]]:
        """Execute query."""
        pass


class RealDatabase(DatabaseQuery):
    """Real database with slow queries."""

    def execute(self, sql: str) -> list[dict[str, Any]]:
        """Execute slow query."""
        print(f"Executing query: {sql}")
        time.sleep(0.1)  # Simulate slow query
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


class CachingDatabaseProxy(DatabaseQuery):
    """
    Proxy that caches query results.

    Examples:
        >>> db = RealDatabase()
        >>> proxy = CachingDatabaseProxy(db)
        >>> results1 = proxy.execute("SELECT * FROM users")
        Executing query: SELECT * FROM users
        >>> results2 = proxy.execute("SELECT * FROM users")
        Using cached result for: SELECT * FROM users
        >>> len(results1)
        2
    """

    def __init__(self, database: RealDatabase) -> None:
        """Initialize with real database."""
        self._database = database
        self._cache: dict[str, list[dict[str, Any]]] = {}

    def execute(self, sql: str) -> list[dict[str, Any]]:
        """Execute query with caching."""
        if sql in self._cache:
            print(f"Using cached result for: {sql}")
            return self._cache[sql]

        result = self._database.execute(sql)
        self._cache[sql] = result
        return result

    def clear_cache(self) -> None:
        """Clear the cache."""
        self._cache.clear()


# Logging Proxy
class Service(ABC):
    """Service interface."""

    @abstractmethod
    def operation(self, data: str) -> str:
        """Perform operation."""
        pass


class RealService(Service):
    """Real service implementation."""

    def operation(self, data: str) -> str:
        """Process data."""
        return f"Processed: {data}"


class LoggingProxy(Service):
    """
    Proxy that logs all operations.

    Examples:
        >>> service = RealService()
        >>> proxy = LoggingProxy(service)
        >>> result = proxy.operation("test data")
        [LOG] Calling operation with: test data
        [LOG] Result: Processed: test data
        >>> result
        'Processed: test data'
    """

    def __init__(self, service: Service) -> None:
        """Initialize with real service."""
        self._service = service

    def operation(self, data: str) -> str:
        """Log and delegate operation."""
        print(f"[LOG] Calling operation with: {data}")
        result = self._service.operation(data)
        print(f"[LOG] Result: {result}")
        return result


def demonstrate_all() -> None:
    """Demonstrate Proxy pattern."""
    print("=== Proxy Pattern ===\n")

    # Virtual proxy (lazy loading)
    print("1. Virtual Proxy (Lazy Loading):")
    print("   Creating proxy (no load yet)...")
    proxy = ImageProxy("vacation.jpg")
    print("   Displaying image (loads now)...")
    print(f"   {proxy.display()}")
    print("   Displaying again (cached)...")
    print(f"   {proxy.display()}")
    print()

    # Protection proxy
    print("2. Protection Proxy (Access Control):")
    doc = RealDocument("confidential.txt")

    admin_proxy = ProtectedDocument(doc, "admin")
    print(f"   Admin read: {admin_proxy.read()}")
    print(f"   Admin write: {admin_proxy.write('Updated content')}")

    guest_proxy = ProtectedDocument(doc, "guest")
    print(f"   Guest read: {guest_proxy.read()}")
    print(f"   Guest write: {guest_proxy.write('Hack attempt!')}")
    print()

    # Caching proxy
    print("3. Caching Proxy:")
    db = RealDatabase()
    cache_proxy = CachingDatabaseProxy(db)

    print("   First query:")
    result1 = cache_proxy.execute("SELECT * FROM users")

    print("   Second query (cached):")
    result2 = cache_proxy.execute("SELECT * FROM users")

    print(f"   Results equal: {result1 == result2}")
    print()

    # Logging proxy
    print("4. Logging Proxy:")
    service = RealService()
    log_proxy = LoggingProxy(service)

    result = log_proxy.operation("important data")
    print(f"   Final result: {result}")


if __name__ == "__main__":
    demonstrate_all()

