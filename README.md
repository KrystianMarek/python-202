# Python Cheat Sheet Library

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An interactive, example-driven cheat sheet for advanced Python concepts, emphasizing Python 3.13+ features, OOP and functional paradigms, Gang of Four (GoF) design patterns, metaprogramming, and modern tooling.

## 🎯 Features

- **Python 3.13+ Native**: Showcases latest features including PEP 695 type parameters, improved error messages, free-threaded interpreter, and experimental JIT
- **Complete GoF Patterns**: All 23 Gang of Four design patterns implemented with Pythonic idioms
- **Advanced Metaprogramming**: Descriptors, metaclasses, dynamic code generation, AST manipulation
- **OOP & Functional Paradigms**: Side-by-side comparisons and integration patterns
- **Python Idioms**: Duck typing, EAFP/LBYL, context managers, protocols
- **Modern Tooling**: Examples using `uv`, async patterns, type hints
- **Runnable Examples**: Import and execute modular examples in your environment
- **Comprehensive Documentation**: Sphinx docs with Jupyter notebooks

## 📦 Installation

### From PyPI (when published)

```bash
pip install python-cheatsheet-lib
```

### Development Installation with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/python-cheatsheet-lib/python-cheatsheet-lib.git
cd python-cheatsheet-lib

# Create virtual environment and install dependencies
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev,docs,async]"
```

## 🚀 Quick Start

```python
# Import and run examples
from python_cheatsheet_lib.oop.patterns.creational import singleton
from python_cheatsheet_lib.python_313 import improved_error_messages
from python_cheatsheet_lib.metaprogramming.descriptors import validated_property

# Run singleton pattern example
singleton.singleton_example()

# Explore Python 3.13 features
improved_error_messages.demonstrate_error_improvements()

# Use validated properties
validated_property.validated_property_example()
```

## 📚 Content Organization

### Python 3.13 Features
- Improved REPL and error messages
- Free-threaded interpreter (no-GIL mode)
- Experimental JIT compiler
- PEP 695 type parameter syntax
- Enhanced pattern matching

### Design Patterns (All 23 GoF)

#### Creational Patterns
- Abstract Factory
- Builder
- Factory Method
- Prototype
- Singleton
- Object Pool

#### Structural Patterns
- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

#### Behavioral Patterns
- Chain of Responsibility
- Command
- Interpreter
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

### Metaprogramming
- **Introspection**: Type inspection, callable inspection, frame hacking
- **Descriptors**: Basic descriptors, validated properties, bound method proxies
- **Metaclasses**: Registry metaclass, singleton metaclass, `__init_subclass__` hooks
- **Dynamic Code**: AST manipulation, code generation, import hooking
- **Advanced Decorators**: ParamSpec, async decorators, class decorators
- **Protocols**: Runtime checks, structural subtyping, protocol composition

### Functional Programming
- Higher-order functions
- Immutability patterns
- Advanced comprehensions
- Functional composition

### Python Idioms
- Duck typing and protocols
- EAFP vs LBYL
- Context managers
- Monkey patching

### Modern Standards
- `uv` workflows
- Async/await patterns
- Type hints and type checking

## 🔧 Development

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_patterns/test_singleton.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

### Building Documentation

```bash
cd docs
uv run sphinx-build -b html . _build/html
```

### Building Package

```bash
# Build wheel and sdist
uv run hatch build

# Install locally
uv pip install dist/*.whl
```

## 📖 Documentation

Full documentation is available at [ReadTheDocs](https://python-cheatsheet-lib.readthedocs.io) (when published).

Local docs can be built and viewed:
```bash
cd docs
uv run sphinx-build -b html . _build/html
open _build/html/index.html  # On macOS
```

## 🎓 Examples

Each module includes runnable examples:

```python
# Design Pattern Example
from python_cheatsheet_lib.oop.patterns.structural.adapter import adapter_example
adapter_example()

# Metaprogramming Example
from python_cheatsheet_lib.metaprogramming.metaclasses.registry_metaclass import (
    registry_example
)
registry_example()

# Python 3.13 Features
from python_cheatsheet_lib.python_313.type_parameter_syntax import (
    type_parameter_example
)
type_parameter_example()
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest`)
6. Format code (`uv run black src/ tests/`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Python core developers for Python 3.13+ features
- Gang of Four for design patterns
- The Python community for best practices and idioms
- Astral team for `uv` and `ruff`

## 🗺️ Roadmap

- **v0.1.0**: Core structure, basic patterns
- **v0.2.0**: All 23 GoF patterns
- **v0.3.0**: Complete metaprogramming module
- **v0.4.0**: Python 3.13 features, async patterns
- **v0.5.0**: Comprehensive documentation
- **v1.0.0**: PyPI release, 100% test coverage

## 📞 Support

- Issues: [GitHub Issues](https://github.com/python-cheatsheet-lib/python-cheatsheet-lib/issues)
- Discussions: [GitHub Discussions](https://github.com/python-cheatsheet-lib/python-cheatsheet-lib/discussions)

## Pattern Cheat Sheet

| Pattern | Category | Pythonic Feature | Use Case |
|---------|----------|------------------|----------|
| Singleton | Creational | Metaclass | Config management |
| Factory Method | Creational | `@classmethod` | Polymorphic creation |
| Builder | Creational | Fluent API + `@dataclass` | Complex object construction |
| Adapter | Structural | `Protocol` | Legacy API integration |
| Decorator | Structural | `@decorator` + `functools.wraps` | Cross-cutting concerns |
| Proxy | Structural | `__getattr__` | Lazy loading, access control |
| Observer | Behavioral | `async def` + Events | Pub/Sub systems |
| Strategy | Behavioral | First-class functions | Algorithm selection |
| Command | Behavioral | Callable objects | Undo/redo systems |
| State | Behavioral | `match` statements | State machines |

---

Made with ❤️ for the Python community

