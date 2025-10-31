"""Tests for core utilities."""

from python_cheatsheet_lib.core.runner import example_context, run_example


def test_example_context() -> None:
    """Test example context manager."""
    with example_context("Test"):
        pass  # Should print start and end


def test_run_example() -> None:
    """Test run_example function."""

    def sample_func() -> int:
        return 42

    result = run_example(sample_func)
    assert result == 42

