"""
Interpreter Pattern - Define grammar representation and interpreter.

Implements interpreter for a language, defining how to evaluate sentences.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# Expression interface
class Expression(ABC):
    """Base expression class."""

    @abstractmethod
    def interpret(self, context: dict[str, int]) -> int:
        """Interpret the expression."""
        pass


# Terminal expressions
class Number(Expression):
    """Number literal expression."""

    def __init__(self, value: int) -> None:
        """Initialize with number value."""
        self.value = value

    def interpret(self, context: dict[str, int]) -> int:
        """Return the number."""
        return self.value


class Variable(Expression):
    """Variable expression."""

    def __init__(self, name: str) -> None:
        """Initialize with variable name."""
        self.name = name

    def interpret(self, context: dict[str, int]) -> int:
        """Look up variable in context."""
        return context.get(self.name, 0)


# Non-terminal expressions
class Add(Expression):
    """Addition expression."""

    def __init__(self, left: Expression, right: Expression) -> None:
        """Initialize with operands."""
        self.left = left
        self.right = right

    def interpret(self, context: dict[str, int]) -> int:
        """Evaluate addition."""
        return self.left.interpret(context) + self.right.interpret(context)


class Subtract(Expression):
    """Subtraction expression."""

    def __init__(self, left: Expression, right: Expression) -> None:
        """Initialize with operands."""
        self.left = left
        self.right = right

    def interpret(self, context: dict[str, int]) -> int:
        """Evaluate subtraction."""
        return self.left.interpret(context) - self.right.interpret(context)


class Multiply(Expression):
    """Multiplication expression."""

    def __init__(self, left: Expression, right: Expression) -> None:
        """Initialize with operands."""
        self.left = left
        self.right = right

    def interpret(self, context: dict[str, int]) -> int:
        """Evaluate multiplication."""
        return self.left.interpret(context) * self.right.interpret(context)


# Boolean expressions
class BooleanExpression(ABC):
    """Base boolean expression."""

    @abstractmethod
    def evaluate(self, context: dict[str, bool]) -> bool:
        """Evaluate boolean expression."""
        pass


class Constant(BooleanExpression):
    """Boolean constant."""

    def __init__(self, value: bool) -> None:
        """Initialize with value."""
        self.value = value

    def evaluate(self, context: dict[str, bool]) -> bool:
        """Return constant."""
        return self.value


class BooleanVariable(BooleanExpression):
    """Boolean variable."""

    def __init__(self, name: str) -> None:
        """Initialize with name."""
        self.name = name

    def evaluate(self, context: dict[str, bool]) -> bool:
        """Look up variable."""
        return context.get(self.name, False)


class And(BooleanExpression):
    """AND expression."""

    def __init__(self, left: BooleanExpression, right: BooleanExpression) -> None:
        """Initialize with operands."""
        self.left = left
        self.right = right

    def evaluate(self, context: dict[str, bool]) -> bool:
        """Evaluate AND."""
        return self.left.evaluate(context) and self.right.evaluate(context)


class Or(BooleanExpression):
    """OR expression."""

    def __init__(self, left: BooleanExpression, right: BooleanExpression) -> None:
        """Initialize with operands."""
        self.left = left
        self.right = right

    def evaluate(self, context: dict[str, bool]) -> bool:
        """Evaluate OR."""
        return self.left.evaluate(context) or self.right.evaluate(context)


class Not(BooleanExpression):
    """NOT expression."""

    def __init__(self, expr: BooleanExpression) -> None:
        """Initialize with expression."""
        self.expr = expr

    def evaluate(self, context: dict[str, bool]) -> bool:
        """Evaluate NOT."""
        return not self.expr.evaluate(context)


def demonstrate_all() -> None:
    """Demonstrate Interpreter pattern."""
    print("=== Interpreter Pattern ===\n")

    # Arithmetic expressions
    print("1. Arithmetic Expressions:")
    # Build: (x + 5) * (y - 3)
    expr = Multiply(
        Add(Variable("x"), Number(5)),
        Subtract(Variable("y"), Number(3)),
    )

    context = {"x": 10, "y": 8}
    result = expr.interpret(context)
    print(f"   (x + 5) * (y - 3) where x={context['x']}, y={context['y']}")
    print(f"   Result: {result}")
    print()

    # Boolean expressions
    print("2. Boolean Expressions:")
    # Build: (a AND b) OR (NOT c)
    bool_expr = Or(
        And(BooleanVariable("a"), BooleanVariable("b")),
        Not(BooleanVariable("c")),
    )

    bool_context = {"a": True, "b": False, "c": True}
    bool_result = bool_expr.evaluate(bool_context)
    print(f"   (a AND b) OR (NOT c)")
    print(f"   where a={bool_context['a']}, b={bool_context['b']}, c={bool_context['c']}")
    print(f"   Result: {bool_result}")


if __name__ == "__main__":
    demonstrate_all()

