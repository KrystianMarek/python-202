"""
Composite Pattern - Compose objects into tree structures.

Treats individual objects and compositions uniformly using recursive composition.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable


# Component interface
class FileSystemNode(ABC):
    """Base class for file system nodes."""

    def __init__(self, name: str) -> None:
        """Initialize node with name."""
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes."""
        pass

    @abstractmethod
    def print_structure(self, indent: int = 0) -> str:
        """Print structure with indentation."""
        pass


# Leaf
class File(FileSystemNode):
    """File (leaf node)."""

    def __init__(self, name: str, size: int) -> None:
        """Initialize file."""
        super().__init__(name)
        self.size = size

    def get_size(self) -> int:
        """Get file size."""
        return self.size

    def print_structure(self, indent: int = 0) -> str:
        """Print file info."""
        return f"{'  ' * indent}- {self.name} ({self.size} bytes)"


# Composite
class Directory(FileSystemNode):
    """Directory (composite node)."""

    def __init__(self, name: str) -> None:
        """Initialize directory."""
        super().__init__(name)
        self.children: list[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> None:
        """Add child node."""
        self.children.append(node)

    def remove(self, node: FileSystemNode) -> None:
        """Remove child node."""
        self.children.remove(node)

    def get_size(self) -> int:
        """Get total size of directory (recursive)."""
        return sum(child.get_size() for child in self.children)

    def print_structure(self, indent: int = 0) -> str:
        """Print directory structure (recursive)."""
        result = f"{'  ' * indent}+ {self.name}/\n"
        for child in self.children:
            result += child.print_structure(indent + 1) + "\n"
        return result.rstrip()


# Alternative: Expression tree example
class Expression(ABC):
    """Base class for expressions."""

    @abstractmethod
    def evaluate(self) -> float:
        """Evaluate the expression."""
        pass

    @abstractmethod
    def to_string(self) -> str:
        """Convert to string representation."""
        pass


class Number(Expression):
    """Leaf: Number literal."""

    def __init__(self, value: float) -> None:
        """Initialize with value."""
        self.value = value

    def evaluate(self) -> float:
        """Return the number."""
        return self.value

    def to_string(self) -> str:
        """String representation."""
        return str(self.value)


class BinaryOperation(Expression):
    """Composite: Binary operation."""

    def __init__(self, left: Expression, right: Expression, operator: str) -> None:
        """Initialize binary operation."""
        self.left = left
        self.right = right
        self.operator = operator

    def evaluate(self) -> float:
        """Evaluate the operation."""
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        match self.operator:
            case "+":
                return left_val + right_val
            case "-":
                return left_val - right_val
            case "*":
                return left_val * right_val
            case "/":
                return left_val / right_val
            case _:
                raise ValueError(f"Unknown operator: {self.operator}")

    def to_string(self) -> str:
        """String representation."""
        return f"({self.left.to_string()} {self.operator} {self.right.to_string()})"


def demonstrate_all() -> None:
    """Demonstrate Composite pattern."""
    print("=== Composite Pattern ===\n")

    # File system example
    print("1. File System:")
    root = Directory("root")

    home = Directory("home")
    user = Directory("user")

    doc1 = File("readme.txt", 100)
    doc2 = File("notes.txt", 200)
    photo = File("photo.jpg", 5000)

    user.add(doc1)
    user.add(doc2)
    user.add(photo)

    home.add(user)
    root.add(home)

    etc = Directory("etc")
    config = File("config.ini", 50)
    etc.add(config)
    root.add(etc)

    print(root.print_structure())
    print(f"\nTotal size: {root.get_size()} bytes")
    print()

    # Expression tree example
    print("2. Expression Tree:")
    # Build: (10 + 5) * (20 - 15)
    expr = BinaryOperation(
        BinaryOperation(Number(10), Number(5), "+"),
        BinaryOperation(Number(20), Number(15), "-"),
        "*",
    )

    print(f"   Expression: {expr.to_string()}")
    print(f"   Result: {expr.evaluate()}")


if __name__ == "__main__":
    demonstrate_all()

