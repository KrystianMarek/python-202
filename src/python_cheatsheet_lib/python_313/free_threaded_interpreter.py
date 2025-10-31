"""
Free-threaded Python (PEP 703) - Experimental no-GIL mode in Python 3.13.

This module demonstrates concepts related to Python 3.13's experimental
free-threaded mode, which removes the Global Interpreter Lock (GIL).

Note: Actual no-GIL Python requires building with --disable-gil flag.
"""

from __future__ import annotations

import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor


def check_gil_status() -> dict[str, bool | str]:
    """
    Check if Python is running in free-threaded (no-GIL) mode.

    Returns:
        Dictionary with GIL status information

    Examples:
        >>> status = check_gil_status()
        >>> "gil_enabled" in status
        True
    """
    # In Python 3.13+ with --disable-gil, sys._is_gil_enabled() returns False
    try:
        gil_enabled = sys._is_gil_enabled()  # type: ignore
    except AttributeError:
        gil_enabled = True  # Default Python has GIL enabled

    return {
        "gil_enabled": gil_enabled,
        "version": sys.version,
        "implementation": sys.implementation.name,
    }


def cpu_bound_task(n: int) -> int:
    """
    CPU-intensive task for benchmarking thread performance.

    Args:
        n: Number of iterations

    Returns:
        Sum of squares
    """
    total = 0
    for i in range(n):
        total += i * i
    return total


def benchmark_threads(
    task: Callable[[int], int],
    iterations: int,
    num_threads: int,
) -> tuple[float, list[int]]:
    """
    Benchmark a task using multiple threads.

    In free-threaded Python (no-GIL), CPU-bound tasks should benefit
    from true parallelism.

    Args:
        task: Function to benchmark
        iterations: Number of iterations per task
        num_threads: Number of threads to use

    Returns:
        Tuple of (elapsed_time, results)

    Examples:
        >>> elapsed, results = benchmark_threads(cpu_bound_task, 10000, 2)
        >>> len(results)
        2
    """
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(task, iterations) for _ in range(num_threads)]
        results = [f.result() for f in futures]

    elapsed_time = time.perf_counter() - start_time
    return elapsed_time, results


def compare_threading_modes() -> None:
    """
    Compare single-threaded vs multi-threaded performance.

    In traditional Python (with GIL), multi-threading doesn't help CPU-bound tasks.
    In free-threaded Python (no-GIL), multi-threading provides real parallelism.

    Why?
    - Demonstrates the impact of GIL on CPU-bound workloads
    - Shows potential speedup with free-threaded Python
    - Helps understand when threading is beneficial
    """
    iterations = 1_000_000
    print("=== Threading Performance Comparison ===\n")

    # Single-threaded baseline
    start = time.perf_counter()
    result_single = cpu_bound_task(iterations * 4)
    elapsed_single = time.perf_counter() - start

    print(f"Single-threaded: {elapsed_single:.4f} seconds")
    print(f"Result: {result_single}\n")

    # Multi-threaded (4 threads)
    elapsed_multi, results_multi = benchmark_threads(cpu_bound_task, iterations, 4)
    print(f"Multi-threaded (4 threads): {elapsed_multi:.4f} seconds")
    print(f"Results: {len(results_multi)} tasks completed\n")

    # Calculate speedup
    speedup = elapsed_single / elapsed_multi
    print(f"Speedup: {speedup:.2f}x")

    if speedup < 1.5:
        print("\nNote: Limited speedup indicates GIL is present.")
        print("For true parallelism, build Python with --disable-gil")
    else:
        print("\nNote: Good speedup may indicate free-threaded mode!")


def thread_safety_example() -> None:
    """
    Demonstrate thread safety considerations in free-threaded Python.

    In no-GIL mode, race conditions become more likely and important to handle.

    Why?
    - Emphasizes the need for proper synchronization
    - Shows thread-safe patterns
    - Demonstrates common pitfalls
    """
    print("=== Thread Safety Example ===\n")

    # Unsafe counter (race condition)
    class UnsafeCounter:
        def __init__(self) -> None:
            self.count = 0

        def increment(self) -> None:
            # Not thread-safe! Read-modify-write is not atomic
            self.count += 1

    # Safe counter with lock
    class SafeCounter:
        def __init__(self) -> None:
            self.count = 0
            self._lock = threading.Lock()

        def increment(self) -> None:
            with self._lock:
                self.count += 1

    def worker(counter: UnsafeCounter | SafeCounter, iterations: int) -> None:
        for _ in range(iterations):
            counter.increment()

    # Test unsafe counter
    unsafe = UnsafeCounter()
    threads = [threading.Thread(target=worker, args=(unsafe, 1000)) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Unsafe counter result: {unsafe.count}")
    print(f"Expected: {10 * 1000}")
    print(f"Lost updates: {10 * 1000 - unsafe.count}\n")

    # Test safe counter
    safe = SafeCounter()
    threads = [threading.Thread(target=worker, args=(safe, 1000)) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Safe counter result: {safe.count}")
    print(f"Expected: {10 * 1000}")
    print("No lost updates with proper locking!\n")


def io_bound_example() -> None:
    """
    Demonstrate that I/O-bound tasks benefit from threading regardless of GIL.

    Both regular and free-threaded Python handle I/O concurrency well.

    Why?
    - I/O operations release the GIL
    - Threading is beneficial for I/O even with GIL
    - Shows when threading is always useful
    """
    print("=== I/O-Bound Threading Example ===\n")

    def simulate_io_task(task_id: int, duration: float) -> str:
        """Simulate an I/O operation with sleep."""
        time.sleep(duration)
        return f"Task {task_id} completed"

    # Single-threaded I/O
    start = time.perf_counter()
    for i in range(4):
        simulate_io_task(i, 0.1)
    elapsed_single = time.perf_counter() - start

    print(f"Single-threaded I/O: {elapsed_single:.4f} seconds")

    # Multi-threaded I/O
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(simulate_io_task, i, 0.1) for i in range(4)]
        _results = [f.result() for f in futures]
    elapsed_multi = time.perf_counter() - start

    print(f"Multi-threaded I/O: {elapsed_multi:.4f} seconds")
    print(f"Speedup: {elapsed_single / elapsed_multi:.2f}x")
    print("\nI/O-bound tasks benefit from threading even with GIL!\n")


def demonstrate_all() -> None:
    """Run all free-threaded Python examples."""
    # Check GIL status
    status = check_gil_status()
    print("=== Python GIL Status ===")
    for key, value in status.items():
        print(f"{key}: {value}")
    print("\n" + "=" * 60 + "\n")

    # Compare threading modes for CPU-bound tasks
    compare_threading_modes()
    print("\n" + "=" * 60 + "\n")

    # Thread safety
    thread_safety_example()
    print("\n" + "=" * 60 + "\n")

    # I/O-bound example
    io_bound_example()


if __name__ == "__main__":
    demonstrate_all()

