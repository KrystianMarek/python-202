"""
Command Pattern - Encapsulate request as an object.

Allows parameterization of clients with different requests, queuing,
logging, and undo/redo operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# Command interface
class Command(ABC):
    """Base command interface."""

    @abstractmethod
    def execute(self) -> Any:
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self) -> Any:
        """Undo the command."""
        pass


# Receiver
class TextEditor:
    """Text editor (receiver)."""

    def __init__(self) -> None:
        """Initialize with empty text."""
        self.text = ""

    def insert(self, text: str, position: int | None = None) -> None:
        """Insert text at position."""
        if position is None:
            position = len(self.text)
        self.text = self.text[:position] + text + self.text[position:]

    def delete(self, position: int, length: int) -> str:
        """Delete text and return deleted portion."""
        deleted = self.text[position : position + length]
        self.text = self.text[:position] + self.text[position + length :]
        return deleted

    def get_text(self) -> str:
        """Get current text."""
        return self.text


# Concrete commands
class InsertCommand(Command):
    """Command to insert text."""

    def __init__(self, editor: TextEditor, text: str, position: int | None = None):
        """Initialize command."""
        self.editor = editor
        self.text = text
        self.position = position if position is not None else len(editor.text)

    def execute(self) -> None:
        """Execute insert."""
        self.editor.insert(self.text, self.position)

    def undo(self) -> None:
        """Undo insert by deleting."""
        self.editor.delete(self.position, len(self.text))


class DeleteCommand(Command):
    """Command to delete text."""

    def __init__(self, editor: TextEditor, position: int, length: int):
        """Initialize command."""
        self.editor = editor
        self.position = position
        self.length = length
        self.deleted_text = ""

    def execute(self) -> None:
        """Execute delete."""
        self.deleted_text = self.editor.delete(self.position, self.length)

    def undo(self) -> None:
        """Undo delete by inserting back."""
        self.editor.insert(self.deleted_text, self.position)


# Invoker
class CommandHistory:
    """
    Manages command execution and undo/redo.

    Examples:
        >>> editor = TextEditor()
        >>> history = CommandHistory()
        >>> cmd = InsertCommand(editor, "Hello")
        >>> history.execute(cmd)
        >>> editor.get_text()
        'Hello'
        >>> history.undo()
        >>> editor.get_text()
        ''
    """

    def __init__(self) -> None:
        """Initialize empty history."""
        self._history: list[Command] = []
        self._current = -1

    def execute(self, command: Command) -> None:
        """Execute command and add to history."""
        # Remove any commands after current position
        self._history = self._history[: self._current + 1]

        command.execute()
        self._history.append(command)
        self._current += 1

    def undo(self) -> bool:
        """Undo last command."""
        if self._current < 0:
            return False

        self._history[self._current].undo()
        self._current -= 1
        return True

    def redo(self) -> bool:
        """Redo previously undone command."""
        if self._current >= len(self._history) - 1:
            return False

        self._current += 1
        self._history[self._current].execute()
        return True


# Alternative: Functional approach with lambdas
@dataclass
class FunctionalCommand:
    """Command using functions instead of classes."""

    execute_fn: Any
    undo_fn: Any

    def execute(self) -> Any:
        """Execute the command."""
        return self.execute_fn()

    def undo(self) -> Any:
        """Undo the command."""
        return self.undo_fn()


# Macro command (composite)
class MacroCommand(Command):
    """Execute multiple commands as one."""

    def __init__(self, commands: list[Command]) -> None:
        """Initialize with list of commands."""
        self.commands = commands

    def execute(self) -> None:
        """Execute all commands."""
        for command in self.commands:
            command.execute()

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self.commands):
            command.undo()


def demonstrate_all() -> None:
    """Demonstrate Command pattern."""
    print("=== Command Pattern ===\n")

    # Text editor with undo/redo
    print("1. Text Editor with Undo/Redo:")
    editor = TextEditor()
    history = CommandHistory()

    # Execute commands
    history.execute(InsertCommand(editor, "Hello"))
    print(f"   After 'Hello': '{editor.get_text()}'")

    history.execute(InsertCommand(editor, " World"))
    print(f"   After ' World': '{editor.get_text()}'")

    history.execute(InsertCommand(editor, "!", None))
    print(f"   After '!': '{editor.get_text()}'")

    # Undo
    history.undo()
    print(f"   After undo: '{editor.get_text()}'")

    history.undo()
    print(f"   After undo: '{editor.get_text()}'")

    # Redo
    history.redo()
    print(f"   After redo: '{editor.get_text()}'")
    print()

    # Macro command
    print("2. Macro Command:")
    editor2 = TextEditor()
    macro = MacroCommand(
        [
            InsertCommand(editor2, "First "),
            InsertCommand(editor2, "Second "),
            InsertCommand(editor2, "Third"),
        ]
    )

    macro.execute()
    print(f"   After macro: '{editor2.get_text()}'")

    macro.undo()
    print(f"   After macro undo: '{editor2.get_text()}'")


if __name__ == "__main__":
    demonstrate_all()
