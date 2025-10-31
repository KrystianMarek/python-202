"""
Object Pool Pattern - Reuse expensive objects instead of recreating them.

Maintains a pool of reusable objects, reducing overhead of creation/destruction.
Particularly useful for database connections, thread pools, etc.
"""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from queue import Empty, Queue
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass
class PooledObject[T]:
    """Wrapper for pooled objects with metadata."""

    obj: T
    created_at: float
    last_used: float
    use_count: int = 0


class ObjectPool[T]:
    """
    Generic object pool implementation.

    Why use Object Pool?
    - Expensive object creation (e.g., database connections)
    - Limited resources (e.g., thread pool)
    - Performance optimization
    - Resource management

    Trade-offs:
    - Memory overhead (unused objects)
    - Complexity in lifecycle management
    - Potential for stale objects

    Examples:
        >>> pool = ObjectPool(lambda: "connection", max_size=2)
        >>> conn1 = pool.acquire()
        >>> conn1
        'connection'
        >>> pool.release(conn1)
    """

    def __init__(
        self,
        factory: callable[[], T],
        max_size: int = 10,
        timeout: float | None = None,
    ) -> None:
        """
        Initialize object pool.

        Args:
            factory: Function to create new objects
            max_size: Maximum pool size
            timeout: Timeout for acquiring objects (None = no timeout)
        """
        self._factory = factory
        self._max_size = max_size
        self._timeout = timeout
        self._pool: Queue[PooledObject[T]] = Queue(maxsize=max_size)
        self._lock = threading.Lock()
        self._created_count = 0

    def acquire(self) -> T:
        """
        Acquire an object from the pool.

        Returns:
            Object from pool or newly created

        Raises:
            TimeoutError: If timeout expires waiting for object
        """
        try:
            # Try to get from pool
            pooled = self._pool.get(timeout=self._timeout)
            pooled.last_used = time.time()
            pooled.use_count += 1
            return pooled.obj

        except Empty:
            # Pool is empty, create new object if under limit
            with self._lock:
                if self._created_count < self._max_size:
                    obj = self._factory()
                    self._created_count += 1
                    return obj
                raise TimeoutError("Pool exhausted and max size reached") from None

    def release(self, obj: T) -> None:
        """
        Return object to pool.

        Args:
            obj: Object to return to pool
        """
        pooled = PooledObject(
            obj=obj,
            created_at=time.time(),
            last_used=time.time(),
            use_count=0,
        )

        try:
            self._pool.put_nowait(pooled)
        except Exception:
            # Pool is full, object will be garbage collected
            pass

    @contextmanager
    def get_object(self):
        """
        Context manager for automatic acquire/release.

        Yields:
            Object from pool

        Examples:
            >>> pool = ObjectPool(lambda: "connection", max_size=2)
            >>> with pool.get_object() as conn:
            ...     print(f"Using {conn}")
            Using connection
        """
        obj = self.acquire()
        try:
            yield obj
        finally:
            self.release(obj)

    def size(self) -> int:
        """Get current pool size."""
        return self._pool.qsize()

    def clear(self) -> None:
        """Clear all objects from pool."""
        while not self._pool.empty():
            try:
                self._pool.get_nowait()
            except Empty:
                break


# Concrete example: Database connection pool
class DatabaseConnection:
    """Simulated database connection."""

    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self) -> None:
        """Create expensive database connection."""
        with DatabaseConnection._lock:
            DatabaseConnection._id_counter += 1
            self.id = DatabaseConnection._id_counter

        print(f"Creating expensive DB connection {self.id}...")
        time.sleep(0.1)  # Simulate connection overhead
        self.connected = True

    def execute(self, query: str) -> str:
        """Execute query."""
        if not self.connected:
            raise RuntimeError("Connection not established")
        return f"Connection {self.id}: Executed '{query}'"

    def close(self) -> None:
        """Close connection."""
        self.connected = False
        print(f"Closing connection {self.id}")


class ConnectionPool:
    """
    Specialized database connection pool.

    Examples:
        >>> pool = ConnectionPool(max_size=3)
        >>> with pool.get_connection() as conn:
        ...     result = conn.execute("SELECT * FROM users")
        ...     print(result)
        Creating expensive DB connection ...
        Connection ...: Executed 'SELECT * FROM users'
    """

    def __init__(self, max_size: int = 5) -> None:
        """
        Initialize connection pool.

        Args:
            max_size: Maximum number of connections
        """
        self._pool: ObjectPool[DatabaseConnection] = ObjectPool(
            factory=DatabaseConnection,
            max_size=max_size,
            timeout=5.0,
        )

    @contextmanager
    def get_connection(self):
        """
        Get a database connection.

        Yields:
            DatabaseConnection instance
        """
        with self._pool.get_object() as conn:
            yield conn


# Thread pool example
class Worker:
    """Worker that can execute tasks."""

    def __init__(self, worker_id: int) -> None:
        """Initialize worker."""
        self.worker_id = worker_id
        print(f"Created worker {worker_id}")

    def execute(self, task: callable[[], Any]) -> Any:
        """Execute a task."""
        print(f"Worker {self.worker_id} executing task")
        return task()


class WorkerPool:
    """
    Pool of worker threads.

    Examples:
        >>> pool = WorkerPool(num_workers=3)
        >>> def task():
        ...     return 42
        >>> result = pool.execute_task(task)
        >>> result
        42
    """

    def __init__(self, num_workers: int = 4) -> None:
        """
        Initialize worker pool.

        Args:
            num_workers: Number of workers to create
        """
        self._pool: ObjectPool[Worker] = ObjectPool(
            factory=lambda: Worker(self._worker_count()),
            max_size=num_workers,
        )
        self._counter = 0
        self._lock = threading.Lock()

    def _worker_count(self) -> int:
        """Get next worker ID."""
        with self._lock:
            self._counter += 1
            return self._counter

    def execute_task(self, task: callable[[], Any]) -> Any:
        """
        Execute task using a worker from pool.

        Args:
            task: Callable to execute

        Returns:
            Result of task execution
        """
        with self._pool.get_object() as worker:
            return worker.execute(task)


def demonstrate_all() -> None:
    """Demonstrate Object Pool pattern."""
    print("=== Object Pool Pattern ===\n")

    # Database connection pool
    print("1. Database Connection Pool:")
    pool = ConnectionPool(max_size=2)

    # First connection creates a new one
    with pool.get_connection() as conn1:
        print(f"   {conn1.execute('SELECT * FROM users')}")

    # Second connection reuses the first
    with pool.get_connection() as conn2:
        print(f"   {conn2.execute('SELECT * FROM orders')}")

    # Multiple concurrent connections
    with pool.get_connection() as conn3:
        with pool.get_connection() as conn4:
            print(f"   {conn3.execute('SELECT 1')}")
            print(f"   {conn4.execute('SELECT 2')}")
    print()

    # Worker pool
    print("2. Worker Pool:")
    worker_pool = WorkerPool(num_workers=2)

    def compute_task() -> int:
        time.sleep(0.01)
        return 42

    results = []
    for i in range(4):
        result = worker_pool.execute_task(compute_task)
        results.append(result)
        print(f"   Task {i + 1} result: {result}")
    print()

    # Generic pool
    print("3. Generic Object Pool:")
    expensive_objects: list[str] = []

    def create_expensive_object() -> str:
        obj = f"Object-{len(expensive_objects) + 1}"
        expensive_objects.append(obj)
        print(f"   Creating {obj}")
        return obj

    generic_pool: ObjectPool[str] = ObjectPool(
        factory=create_expensive_object,
        max_size=3,
    )

    # Acquire and release
    obj1 = generic_pool.acquire()
    obj2 = generic_pool.acquire()
    print(f"   Acquired: {obj1}, {obj2}")

    generic_pool.release(obj1)
    obj3 = generic_pool.acquire()  # Reuses obj1
    print(f"   Acquired again: {obj3}")
    print(f"   Total created: {len(expensive_objects)}")


def benchmark_pool() -> None:
    """Benchmark pool vs. creating new objects."""
    print("\n=== Pool Performance Comparison ===\n")

    # Without pool
    start = time.perf_counter()
    for _ in range(10):
        conn = DatabaseConnection()
        conn.execute("SELECT 1")
        conn.close()
    without_pool = time.perf_counter() - start

    # With pool
    pool = ConnectionPool(max_size=2)
    start = time.perf_counter()
    for _ in range(10):
        with pool.get_connection() as conn:
            conn.execute("SELECT 1")
    with_pool = time.perf_counter() - start

    print(f"Without pool: {without_pool:.4f}s")
    print(f"With pool:    {with_pool:.4f}s")
    print(f"Speedup:      {without_pool / with_pool:.2f}x")


if __name__ == "__main__":
    demonstrate_all()
    benchmark_pool()

