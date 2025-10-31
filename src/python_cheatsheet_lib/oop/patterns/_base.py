"""Base classes, protocols, and utilities for design patterns."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Protocol, runtime_checkable


@runtime_checkable
class Runnable(Protocol):
    """Protocol for runnable objects."""

    def run(self) -> None:
        """Execute the runnable."""
        ...


@runtime_checkable
class AsyncRunnable(Protocol):
    """Protocol for async runnable objects."""

    async def run_async(self) -> None:
        """Execute the runnable asynchronously."""
        ...


@contextmanager
def example_context(name: str):
    """
    Context manager for running pattern examples.

    Args:
        name: Name of the pattern example

    Yields:
        None
    """
    separator = "=" * 15
    print(f"\n{separator} {name} {separator}")
    try:
        yield
    finally:
        print(f"{separator} END {separator}\n")

