"""
Memento Pattern - Capture and restore object's internal state.

Provides ability to restore object to its previous state (undo).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# Memento
@dataclass(frozen=True)
class EditorMemento:
    """
    Memento storing editor state.

    Immutable snapshot of editor state.
    """

    content: str
    cursor_position: int


# Originator
class TextEditor:
    """
    Text editor that creates mementos.

    Examples:
        >>> editor = TextEditor()
        >>> editor.type("Hello")
        >>> memento = editor.save()
        >>> editor.type(" World")
        >>> editor.get_content()
        'Hello World'
        >>> editor.restore(memento)
        >>> editor.get_content()
        'Hello'
    """

    def __init__(self) -> None:
        """Initialize empty editor."""
        self._content = ""
        self._cursor_position = 0

    def type(self, text: str) -> None:
        """Type text at cursor position."""
        self._content = (
            self._content[: self._cursor_position]
            + text
            + self._content[self._cursor_position :]
        )
        self._cursor_position += len(text)

    def delete(self, count: int) -> None:
        """Delete characters before cursor."""
        start = max(0, self._cursor_position - count)
        self._content = self._content[:start] + self._content[self._cursor_position :]
        self._cursor_position = start

    def move_cursor(self, position: int) -> None:
        """Move cursor to position."""
        self._cursor_position = max(0, min(position, len(self._content)))

    def get_content(self) -> str:
        """Get current content."""
        return self._content

    def save(self) -> EditorMemento:
        """Create memento of current state."""
        return EditorMemento(self._content, self._cursor_position)

    def restore(self, memento: EditorMemento) -> None:
        """Restore state from memento."""
        self._content = memento.content
        self._cursor_position = memento.cursor_position


# Caretaker
class History:
    """
    Manages memento history for undo/redo.

    Examples:
        >>> editor = TextEditor()
        >>> history = History(editor)
        >>> editor.type("First")
        >>> history.save()
        >>> editor.type(" Second")
        >>> history.save()
        >>> history.undo()
        >>> editor.get_content()
        'First'
        >>> history.redo()
        >>> editor.get_content()
        'First Second'
    """

    def __init__(self, originator: TextEditor) -> None:
        """Initialize with originator."""
        self._originator = originator
        self._mementos: list[EditorMemento] = []
        self._current = -1

    def save(self) -> None:
        """Save current state."""
        # Remove any states after current position
        self._mementos = self._mementos[: self._current + 1]

        memento = self._originator.save()
        self._mementos.append(memento)
        self._current += 1

    def undo(self) -> bool:
        """Undo to previous state."""
        if self._current > 0:
            self._current -= 1
            self._originator.restore(self._mementos[self._current])
            return True
        return False

    def redo(self) -> bool:
        """Redo to next state."""
        if self._current < len(self._mementos) - 1:
            self._current += 1
            self._originator.restore(self._mementos[self._current])
            return True
        return False


# Game state example
@dataclass(frozen=True)
class GameMemento:
    """Game state memento."""

    level: int
    score: int
    health: int
    position: tuple[int, int]


class Game:
    """
    Game with save/load functionality.

    Examples:
        >>> game = Game()
        >>> save1 = game.save()
        >>> game.level_up()
        >>> game.add_score(100)
        >>> game.level
        2
        >>> game.restore(save1)
        >>> game.level
        1
    """

    def __init__(self) -> None:
        """Initialize new game."""
        self.level = 1
        self.score = 0
        self.health = 100
        self.position = (0, 0)

    def level_up(self) -> None:
        """Advance to next level."""
        self.level += 1

    def add_score(self, points: int) -> None:
        """Add points to score."""
        self.score += points

    def take_damage(self, damage: int) -> None:
        """Reduce health."""
        self.health = max(0, self.health - damage)

    def move(self, x: int, y: int) -> None:
        """Move to position."""
        self.position = (x, y)

    def save(self) -> GameMemento:
        """Save game state."""
        return GameMemento(self.level, self.score, self.health, self.position)

    def restore(self, memento: GameMemento) -> None:
        """Restore game state."""
        self.level = memento.level
        self.score = memento.score
        self.health = memento.health
        self.position = memento.position


def demonstrate_all() -> None:
    """Demonstrate Memento pattern."""
    print("=== Memento Pattern ===\n")

    # Text editor with history
    print("1. Text Editor with Undo/Redo:")
    editor = TextEditor()
    history = History(editor)

    editor.type("Hello")
    history.save()
    print(f"   After 'Hello': {editor.get_content()}")

    editor.type(" World")
    history.save()
    print(f"   After ' World': {editor.get_content()}")

    editor.type("!!!")
    history.save()
    print(f"   After '!!!': {editor.get_content()}")

    history.undo()
    print(f"   After undo: {editor.get_content()}")

    history.undo()
    print(f"   After undo: {editor.get_content()}")

    history.redo()
    print(f"   After redo: {editor.get_content()}")
    print()

    # Game save states
    print("2. Game Save States:")
    game = Game()

    # Save at level 1
    save1 = game.save()
    print(f"   Level {game.level}, Score {game.score}")

    # Progress
    game.level_up()
    game.add_score(500)
    game.move(10, 20)
    save2 = game.save()
    print(f"   Level {game.level}, Score {game.score}, Pos {game.position}")

    # More progress
    game.level_up()
    game.add_score(1000)
    game.take_damage(50)
    print(f"   Level {game.level}, Score {game.score}, Health {game.health}")

    # Load previous save
    game.restore(save2)
    print(f"   Restored: Level {game.level}, Score {game.score}, Health {game.health}")


if __name__ == "__main__":
    demonstrate_all()

