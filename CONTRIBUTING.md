# Contributing to Python Cheat Sheet Library

Thank you for considering contributing to `python-cheatsheet-lib`! This document provides guidelines and instructions for contributing.

## 🎯 How Can I Contribute?

### Reporting Bugs

- Use the GitHub Issues tracker
- Check if the bug has already been reported
- Include a clear title and description
- Provide code samples demonstrating the issue
- Include your Python version and OS

### Suggesting Enhancements

- Use GitHub Issues with the "enhancement" label
- Provide a clear use case
- Explain why this enhancement would be useful
- Include code examples if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

## 🔧 Development Setup

### Prerequisites

- Python 3.13+
- `uv` package manager

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/python-cheatsheet-lib.git
cd python-cheatsheet-lib

# Create virtual environment
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev,docs,async]"

# Install pre-commit hooks
uv run pre-commit install
```

## ✅ Code Standards

### Style Guide

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use Ruff for linting
- Use type hints (mypy strict mode)
- Write docstrings for all public APIs

### Code Formatting

```bash
# Format code
uv run black src/ tests/

# Check linting
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=python_cheatsheet_lib --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_patterns/test_singleton.py
```

## 📝 Documentation

### Docstring Format

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description.

    Longer description explaining the function's purpose, behavior,
    and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative

    Examples:
        >>> example_function("test", 42)
        True
    """
    pass
```

### Adding Examples

Each module should include:

1. Clear, runnable examples
2. Docstrings explaining "Why?" and "When to use?"
3. Trade-offs and anti-patterns
4. Type hints
5. Unit tests

Example template:

```python
def pattern_example() -> None:
    """
    Demonstrate [Pattern Name].

    Why?
    - Reason 1
    - Reason 2

    Trade-offs:
    - Pro: Benefit
    - Con: Drawback

    Anti-pattern: What to avoid

    Examples:
        >>> pattern_example()
        Expected output
    """
    # Implementation
    pass
```

## 🧪 Testing Guidelines

### Test Structure

- Place tests in `tests/` directory
- Mirror the source structure
- Use descriptive test names
- Test edge cases and error conditions

```python
def test_singleton_identity():
    """Test that singleton returns same instance."""
    from python_cheatsheet_lib.oop.patterns.creational.singleton import Config
    assert Config() is Config()

def test_singleton_thread_safety():
    """Test singleton is thread-safe."""
    # Implementation
    pass
```

### Coverage Requirements

- Aim for 80%+ code coverage
- All new features must include tests
- Test both success and failure paths

## 🚀 Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions will handle PyPI release

## 📋 Checklist for Pull Requests

- [ ] Code follows style guidelines (Black, Ruff, mypy)
- [ ] Added tests for new functionality
- [ ] All tests pass locally
- [ ] Updated documentation
- [ ] Added docstrings with examples
- [ ] Updated CHANGELOG.md
- [ ] Commits are clear and descriptive
- [ ] PR description explains changes

## 🎨 Module Guidelines

### Adding New Patterns

1. Create file in appropriate directory
2. Implement pattern with Pythonic idioms
3. Include comprehensive docstrings
4. Add example function
5. Write unit tests
6. Update module `__init__.py`
7. Add to documentation

### Python 3.13+ Focus

- Use modern syntax (PEP 695, match statements)
- Leverage type hints fully
- Demonstrate new features
- Compare with older approaches when relevant

### Code Organization

```
module_name.py:
  - Imports
  - Type definitions
  - Classes/functions
  - Example function
  - if __name__ == "__main__": block for testing
```

## 🤝 Community

- Be respectful and inclusive
- Help others learn
- Provide constructive feedback
- Ask questions if unclear

## 📞 Getting Help

- Open an issue for questions
- Join GitHub Discussions
- Check existing documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉

