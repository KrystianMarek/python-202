"""Generic utilities for executing and running examples."""

from __future__ import annotations

import sys
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any


@contextmanager
def example_context(name: str):
    """
    Context manager for running examples with formatted output.

    Args:
        name: The name of the example being run

    Examples:
        >>> with example_context("Singleton Pattern"):
        ...     print("Example code here")
        ...
        ========== Singleton Pattern ==========
        Example code here
        ========== END ==========
    """
    separator = "=" * 10
    print(f"\n{separator} {name} {separator}")
    try:
        yield
    finally:
        print(f"{separator} END {separator}\n")


def run_example(func: Callable[[], Any], name: str | None = None) -> Any:
    """
    Execute an example function with formatted output.

    Args:
        func: The example function to run
        name: Optional name for the example (defaults to function name)

    Returns:
        The return value of the example function

    Examples:
        >>> def my_example():
        ...     print("Hello, World!")
        ...
        >>> run_example(my_example)
        ========== my_example ==========
        Hello, World!
        ========== END ==========
    """
    example_name = name or func.__name__
    with example_context(example_name):
        return func()


def main() -> None:
    """
    Entry point for the cheatsheet-run CLI command.

    Usage:
        cheatsheet-run module.function
    """
    if len(sys.argv) < 2:
        print("Usage: cheatsheet-run <module.function>")
        print(
            "Example: cheatsheet-run python_cheatsheet_lib.oop.patterns.creational.singleton_example"
        )
        sys.exit(1)

    module_path = sys.argv[1]
    try:
        # Split module and function
        parts = module_path.rsplit(".", 1)
        if len(parts) != 2:
            raise ValueError("Must specify both module and function")

        module_name, func_name = parts

        # Import module
        import importlib

        module = importlib.import_module(module_name)

        # Get function
        func = getattr(module, func_name)

        # Run example
        run_example(func)
    except Exception as e:
        print(f"Error running example: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
