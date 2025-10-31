#!/usr/bin/env python3
"""
Quickstart example for python-cheatsheet-lib.

Demonstrates basic usage of the library.
"""

from python_cheatsheet_lib.oop.patterns.creational.singleton import DatabaseConnection
from python_cheatsheet_lib.oop.patterns.structural.adapter import (
    AudioPlayerAdapter,
    LegacyAudioPlayer,
)
from python_cheatsheet_lib.python_313.type_parameter_syntax import identity


def main() -> None:
    """Run quickstart examples."""
    print("=== Python Cheat Sheet Library - Quickstart ===\n")

    # Python 3.13 features
    print("1. Python 3.13 Type Parameters:")
    result = identity(42)
    print(f"   identity(42) = {result}")
    print()

    # Design Patterns
    print("2. Singleton Pattern:")
    db1 = DatabaseConnection("localhost")
    db2 = DatabaseConnection("remotehost")
    print(f"   Same instance: {db1 is db2}")
    print()

    # Adapter Pattern
    print("3. Adapter Pattern:")
    legacy = LegacyAudioPlayer()
    adapter = AudioPlayerAdapter(legacy)
    print(f"   {adapter.play('song.mp3')}")


if __name__ == "__main__":
    main()

