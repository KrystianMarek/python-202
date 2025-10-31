"""
Experimental JIT Compiler in Python 3.13.

Python 3.13 includes an experimental just-in-time (JIT) compiler
that can provide performance improvements for certain workloads.

Note: The JIT is experimental and disabled by default in Python 3.13.
Enable with PYTHON_JIT=1 environment variable.
"""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable


def check_jit_status() -> dict[str, str | bool]:
    """
    Check if JIT is enabled in the current Python runtime.

    Returns:
        Dictionary with JIT status information

    Examples:
        >>> status = check_jit_status()
        >>> "jit_enabled" in status
        True
    """
    # Check environment variable
    jit_env = os.environ.get("PYTHON_JIT", "0")

    # In actual Python 3.13, there would be sys flags for JIT
    # This is a placeholder for demonstration
    return {
        "jit_env_var": jit_env,
        "jit_enabled": jit_env == "1",
        "version": sys.version,
        "platform": sys.platform,
    }


def fibonacci_recursive(n: int) -> int:
    """
    Recursive Fibonacci (inefficient, good for JIT testing).

    Args:
        n: Fibonacci number to calculate

    Returns:
        The nth Fibonacci number

    Examples:
        >>> fibonacci_recursive(10)
        55
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    Iterative Fibonacci (efficient).

    Args:
        n: Fibonacci number to calculate

    Returns:
        The nth Fibonacci number

    Examples:
        >>> fibonacci_iterative(10)
        55
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def benchmark_function(func: Callable[[int], int], n: int, iterations: int = 1) -> float:
    """
    Benchmark a function's execution time.

    Args:
        func: Function to benchmark
        n: Argument to pass to function
        iterations: Number of times to run the function

    Returns:
        Average execution time in seconds

    Examples:
        >>> elapsed = benchmark_function(fibonacci_iterative, 20, 100)
        >>> elapsed > 0
        True
    """
    start_time = time.perf_counter()
    for _ in range(iterations):
        _result = func(n)
    end_time = time.perf_counter()
    return (end_time - start_time) / iterations


def hot_loop_example() -> int:
    """
    Example of a hot loop that could benefit from JIT.

    Hot loops are frequently executed code paths that JIT can optimize.

    Returns:
        Computed result
    """
    total = 0
    for i in range(1_000_000):
        total += i * i - i // 2
    return total


def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """
    Naive matrix multiplication (CPU-intensive, JIT candidate).

    Args:
        a: First matrix
        b: Second matrix

    Returns:
        Product matrix

    Examples:
        >>> a = [[1.0, 2.0], [3.0, 4.0]]
        >>> b = [[5.0, 6.0], [7.0, 8.0]]
        >>> result = matrix_multiply(a, b)
        >>> len(result)
        2
    """
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    if cols_a != rows_b:
        raise ValueError("Incompatible matrix dimensions")

    result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]

    return result


def compare_jit_performance() -> None:
    """
    Compare performance with and without JIT (conceptual).

    In practice, you would run the same code with PYTHON_JIT=0 and PYTHON_JIT=1.

    Why?
    - Understand JIT impact on different workloads
    - Identify code patterns that benefit from JIT
    - Learn when JIT provides value
    """
    print("=== JIT Performance Comparison ===\n")

    status = check_jit_status()
    print(f"JIT Status: {status['jit_enabled']}\n")

    # Benchmark hot loop
    print("1. Hot Loop Benchmark:")
    elapsed = benchmark_function(lambda _: hot_loop_example(), 0, iterations=10)
    print(f"   Average time: {elapsed:.6f} seconds\n")

    # Benchmark recursive function
    print("2. Recursive Fibonacci (n=30):")
    elapsed = benchmark_function(fibonacci_recursive, 30, iterations=1)
    print(f"   Time: {elapsed:.6f} seconds\n")

    # Benchmark iterative function
    print("3. Iterative Fibonacci (n=30):")
    elapsed = benchmark_function(fibonacci_iterative, 30, iterations=1000)
    print(f"   Average time: {elapsed:.6f} seconds\n")

    # Benchmark matrix multiplication
    print("4. Matrix Multiplication (50x50):")
    size = 50
    matrix_a = [[float(i + j) for j in range(size)] for i in range(size)]
    matrix_b = [[float(i * j) for j in range(size)] for i in range(size)]

    start = time.perf_counter()
    _result = matrix_multiply(matrix_a, matrix_b)
    elapsed = time.perf_counter() - start
    print(f"   Time: {elapsed:.6f} seconds\n")

    if not status["jit_enabled"]:
        print("Note: JIT is not enabled. Set PYTHON_JIT=1 to enable it.")
        print("      Expect 10-30% performance improvement for hot loops.")


def jit_friendly_patterns() -> None:
    """
    Demonstrate code patterns that work well with JIT.

    JIT-friendly code:
    - Type-stable functions (consistent types)
    - Hot loops without excessive branching
    - Numerical computations
    - Functions called many times

    JIT-unfriendly:
    - Highly dynamic code
    - Heavy use of eval/exec
    - Frequent type changes
    - Meta-programming
    """
    print("=== JIT-Friendly vs JIT-Unfriendly Patterns ===\n")

    print("JIT-Friendly Patterns:")
    print("✓ Type-stable numeric loops")
    print("✓ Repeated function calls")
    print("✓ Array/list processing")
    print("✓ Mathematical computations\n")

    print("JIT-Unfriendly Patterns:")
    print("✗ Polymorphic function arguments")
    print("✗ Heavy use of dynamic features")
    print("✗ Infrequently called code")
    print("✗ String manipulation heavy code\n")

    # JIT-friendly example
    def jit_friendly(data: list[float]) -> float:
        """Type-stable numerical computation."""
        total = 0.0
        for value in data:
            total += value * value
        return total

    # JIT-unfriendly example
    def jit_unfriendly(data: list) -> float:
        """Polymorphic with type uncertainty."""
        total = 0.0
        for value in data:
            if isinstance(value, (int, float)):
                total += float(value)
            elif isinstance(value, str):
                total += float(len(value))
        return total

    # Benchmark
    test_data = [float(i) for i in range(10000)]

    elapsed_friendly = benchmark_function(lambda _: jit_friendly(test_data), 0, 100)
    print(f"JIT-friendly function: {elapsed_friendly:.6f} seconds")

    elapsed_unfriendly = benchmark_function(lambda _: jit_unfriendly(test_data), 0, 100)
    print(f"JIT-unfriendly function: {elapsed_unfriendly:.6f} seconds\n")


def demonstrate_all() -> None:
    """Run all JIT-related examples."""
    status = check_jit_status()
    print("=== Python JIT Status ===")
    for key, value in status.items():
        print(f"{key}: {value}")
    print("\n" + "=" * 60 + "\n")

    compare_jit_performance()
    print("\n" + "=" * 60 + "\n")

    jit_friendly_patterns()

    print("\n" + "=" * 60)
    print("\nTo enable JIT, run:")
    print("  PYTHON_JIT=1 python -m python_cheatsheet_lib.python_313.jit_experiments")


if __name__ == "__main__":
    demonstrate_all()
