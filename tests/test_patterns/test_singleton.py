"""Tests for Singleton pattern."""

import threading

from python_cheatsheet_lib.oop.patterns.creational.singleton import DatabaseConnection


def test_singleton_identity() -> None:
    """Test that singleton returns same instance."""
    db1 = DatabaseConnection("localhost")
    db2 = DatabaseConnection("remotehost")
    assert db1 is db2


def test_singleton_thread_safety() -> None:
    """Test singleton is thread-safe."""
    instances: list[DatabaseConnection] = []

    def get_instance() -> None:
        instances.append(DatabaseConnection("test"))

    threads = [threading.Thread(target=get_instance) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All instances should be the same object
    unique_ids = len({id(instance) for instance in instances})
    assert unique_ids == 1

