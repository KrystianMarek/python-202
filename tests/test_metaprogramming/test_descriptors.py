"""Tests for descriptors."""

from python_cheatsheet_lib.metaprogramming.descriptors import LazyProperty, TypedProperty


def test_typed_property() -> None:
    """Test type-validated property."""

    class Person:
        name = TypedProperty(str)
        age = TypedProperty(int)

    person = Person()
    person.name = "Alice"
    person.age = 30

    assert person.name == "Alice"
    assert person.age == 30

    try:
        person.age = "thirty"  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError:
        pass


def test_lazy_property() -> None:
    """Test lazy property evaluation."""
    call_count = 0

    class DataLoader:
        @LazyProperty
        def data(self) -> list[int]:
            nonlocal call_count
            call_count += 1
            return [1, 2, 3]

    loader = DataLoader()
    assert call_count == 0

    data1 = loader.data
    assert call_count == 1
    assert data1 == [1, 2, 3]

    data2 = loader.data
    assert call_count == 1  # Cached, not called again
    assert data2 == [1, 2, 3]
