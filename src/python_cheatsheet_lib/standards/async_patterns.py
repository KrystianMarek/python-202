"""
Async/await patterns for concurrent programming.

Modern Python async patterns using asyncio.
"""

from __future__ import annotations

import asyncio


async def fetch_data(url: str, delay: float = 0.1) -> str:
    """
    Simulate async data fetching.

    Examples:
        >>> import asyncio
        >>> asyncio.run(fetch_data("https://example.com"))
        'Data from https://example.com'
    """
    await asyncio.sleep(delay)
    return f"Data from {url}"


async def demonstrate_gather() -> None:
    """Demonstrate asyncio.gather for concurrent execution."""
    print("Running concurrent tasks...")
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
    )
    for result in results:
        print(f"   {result}")


async def demonstrate_all() -> None:
    """Demonstrate async patterns."""
    print("=== Async Patterns ===\n")
    await demonstrate_gather()


if __name__ == "__main__":
    asyncio.run(demonstrate_all())

