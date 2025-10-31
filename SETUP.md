# Python Cheat Sheet Library - Setup Guide

A comprehensive Python cheat sheet library has been created with all the components specified in your plan.

## 📦 What's Included

### ✅ Core Modules

1. **Python 3.13 Features** (`src/python_cheatsheet_lib/python_313/`)
   - Improved error messages
   - Type parameter syntax (PEP 695)
   - Free-threaded interpreter concepts
   - JIT experiments

2. **All 23 Gang of Four Design Patterns** (`src/python_cheatsheet_lib/oop/patterns/`)
   - **Creational** (6): Singleton, Factory Method, Abstract Factory, Builder, Prototype, Object Pool
   - **Structural** (7): Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
   - **Behavioral** (10): Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor

3. **Metaprogramming** (`src/python_cheatsheet_lib/metaprogramming/`)
   - Descriptors (type-validated, lazy, cached properties)
   - Metaclasses (registry, singleton, __init_subclass__)

4. **Functional Programming** (`src/python_cheatsheet_lib/functional/`)
   - Higher-order functions (map, filter, reduce, compose)

5. **Python Idioms** (`src/python_cheatsheet_lib/idioms/`)
   - Duck typing with Protocols
   - EAFP vs LBYL

6. **Modern Standards** (`src/python_cheatsheet_lib/standards/`)
   - Async/await patterns

## 🚀 Quick Start

### Installation (Development Mode)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
cd /Users/kmarek/Development/python-202
uv venv --python 3.13

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Install package in editable mode with dev dependencies
uv pip install -e ".[dev,docs,async]"

# Install pre-commit hooks
uv run pre-commit install
```

### Running Examples

```bash
# Run quickstart example
python examples/quickstart.py

# Run specific pattern examples
python -m python_cheatsheet_lib.oop.patterns.creational.singleton
python -m python_cheatsheet_lib.python_313.type_parameter_syntax

# Or use the CLI
cheatsheet-run python_cheatsheet_lib.oop.patterns.creational.singleton.demonstrate_all
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=python_cheatsheet_lib --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_patterns/test_singleton.py
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

## 📚 Documentation

### Build Documentation

```bash
cd docs
uv run sphinx-build -b html . _build/html
open _build/html/index.html  # On macOS
```

## 🏗️ Project Structure

```
python-202/
├── src/python_cheatsheet_lib/     # Main package
│   ├── core/                       # Core utilities
│   ├── python_313/                 # Python 3.13 features
│   ├── oop/                        # OOP basics and patterns
│   │   ├── basics.py
│   │   └── patterns/
│   │       ├── creational/         # 6 patterns
│   │       ├── structural/         # 7 patterns
│   │       └── behavioral/         # 10 patterns
│   ├── metaprogramming/            # Advanced metaprogramming
│   │   ├── descriptors.py
│   │   └── metaclasses.py
│   ├── functional/                 # Functional programming
│   ├── idioms/                     # Python idioms
│   └── standards/                  # Modern standards
├── tests/                          # Test suite
├── docs/                           # Sphinx documentation
├── examples/                       # Example scripts
├── .github/workflows/              # CI/CD
├── pyproject.toml                  # Package configuration
├── README.md                       # Main documentation
└── CONTRIBUTING.md                 # Contribution guidelines
```

## 🎯 Usage Examples

### Example 1: Using Design Patterns

```python
from python_cheatsheet_lib.oop.patterns.creational.singleton import DatabaseConnection
from python_cheatsheet_lib.oop.patterns.structural.adapter import AudioPlayerAdapter, LegacyAudioPlayer

# Singleton pattern
db1 = DatabaseConnection("localhost")
db2 = DatabaseConnection("remote")
assert db1 is db2  # Same instance!

# Adapter pattern
legacy = LegacyAudioPlayer()
adapter = AudioPlayerAdapter(legacy)
adapter.play("song.mp3")
```

### Example 2: Python 3.13 Features

```python
from python_cheatsheet_lib.python_313.type_parameter_syntax import identity, Stack

# New type parameter syntax
result = identity(42)  # Type-safe generic function

# Generic class
stack = Stack[int]()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2
```

### Example 3: Metaprogramming

```python
from python_cheatsheet_lib.metaprogramming.descriptors import TypedProperty, LazyProperty

class Person:
    name = TypedProperty(str)
    age = TypedProperty(int)

    @LazyProperty
    def expensive_data(self):
        print("Computing...")
        return [1, 2, 3]

person = Person()
person.name = "Alice"
person.age = 30

# Lazy evaluation
data1 = person.expensive_data  # Prints "Computing..."
data2 = person.expensive_data  # Cached, no print
```

## 🔧 Development Workflow

### Adding New Patterns

1. Create new file in appropriate directory
2. Implement pattern with docstrings and examples
3. Add tests in `tests/test_patterns/`
4. Update module `__init__.py`
5. Run tests and linting

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-pattern

# Make changes
# ... edit files ...

# Format and lint
uv run black src/ tests/
uv run ruff check --fix src/ tests/

# Run tests
uv run pytest

# Commit
git add .
git commit -m "Add new pattern: Template Method"

# Push
git push origin feature/new-pattern
```

## 📊 CI/CD

GitHub Actions workflows are configured for:

- **CI** (`.github/workflows/ci.yml`):
  - Runs on push to main/develop
  - Tests on Ubuntu, macOS, Windows
  - Linting (ruff), formatting (black), type checking (mypy)
  - Test coverage reporting

- **Documentation** (`.github/workflows/docs.yml`):
  - Builds Sphinx documentation on push to main

## 🎓 Learning Resources

Each module includes:
- Comprehensive docstrings
- Working examples
- "Why?" sections explaining use cases
- Trade-offs and anti-patterns
- Type hints throughout

## 📝 Next Steps

1. **Add More Examples**: Extend each module with additional real-world examples
2. **Jupyter Notebooks**: Create interactive notebooks in `docs/notebooks/`
3. **Performance Benchmarks**: Add benchmark scripts in `examples/`
4. **Video Tutorials**: Link to video explanations
5. **PyPI Publication**: Publish to PyPI when ready

## 🤝 Contributing

See `CONTRIBUTING.md` for detailed contribution guidelines.

## 📄 License

MIT License - see `LICENSE` file for details.

---

**Built with ❤️ for the Python community**

For questions or issues, please open a GitHub issue.

