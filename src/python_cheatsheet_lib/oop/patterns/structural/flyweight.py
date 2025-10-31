"""
Flyweight Pattern - Share common state to support large numbers of objects.

Reduces memory usage by sharing intrinsic (common) state among many objects,
while keeping extrinsic (unique) state separate.
"""

from __future__ import annotations


# Flyweight: Shared character style
class CharacterStyle:
    """
    Flyweight object storing shared character formatting.

    Intrinsic state (shared): font, size, color
    """

    def __init__(self, font: str, size: int, color: str) -> None:
        """Initialize shared style."""
        self.font = font
        self.size = size
        self.color = color
        print(f"Creating style: {font}, {size}pt, {color}")

    def __repr__(self) -> str:
        """String representation."""
        return f"Style({self.font}, {self.size}pt, {self.color})"


# Flyweight Factory
class StyleFactory:
    """
    Factory that ensures flyweights are shared.

    Examples:
        >>> factory = StyleFactory()
        >>> style1 = factory.get_style("Arial", 12, "black")
        Creating style: Arial, 12pt, black
        >>> style2 = factory.get_style("Arial", 12, "black")
        >>> style1 is style2  # Same object!
        True
    """

    def __init__(self) -> None:
        """Initialize empty pool."""
        self._styles: dict[tuple[str, int, str], CharacterStyle] = {}

    def get_style(self, font: str, size: int, color: str) -> CharacterStyle:
        """
        Get or create a style flyweight.

        Args:
            font: Font name
            size: Font size
            color: Font color

        Returns:
            Shared CharacterStyle instance
        """
        key = (font, size, color)
        if key not in self._styles:
            self._styles[key] = CharacterStyle(font, size, color)
        return self._styles[key]

    def get_style_count(self) -> int:
        """Get number of unique styles."""
        return len(self._styles)


# Context: Uses flyweight
class Character:
    """
    Character in a document.

    Extrinsic state (unique): position
    Intrinsic state (shared): style (flyweight)
    """

    def __init__(self, char: str, style: CharacterStyle, position: int) -> None:
        """Initialize character."""
        self.char = char
        self.style = style  # Shared flyweight
        self.position = position  # Unique to this character

    def render(self) -> str:
        """Render character with style."""
        return f"'{self.char}' at {self.position} with {self.style}"


# Document using flyweights
class Document:
    """
    Document containing many characters.

    Demonstrates memory savings from flyweight pattern.

    Examples:
        >>> doc = Document()
        >>> doc.add_text("Hello", "Arial", 12, "black")
        Creating style: Arial, 12pt, black
        >>> doc.add_text("World", "Arial", 12, "black")
        >>> doc.get_character_count()
        10
        >>> doc.get_style_count()
        1
    """

    def __init__(self) -> None:
        """Initialize empty document."""
        self.characters: list[Character] = []
        self.style_factory = StyleFactory()

    def add_text(self, text: str, font: str, size: int, color: str) -> None:
        """
        Add text to document.

        Args:
            text: Text to add
            font: Font name
            size: Font size
            color: Font color
        """
        style = self.style_factory.get_style(font, size, color)
        for char in text:
            position = len(self.characters)
            self.characters.append(Character(char, style, position))

    def get_character_count(self) -> int:
        """Get total number of characters."""
        return len(self.characters)

    def get_style_count(self) -> int:
        """Get number of unique styles (flyweights)."""
        return self.style_factory.get_style_count()

    def render(self) -> str:
        """Render part of document."""
        return "\n".join(char.render() for char in self.characters[:5])


# Alternative example: Game particles
class ParticleType:
    """Flyweight for particle appearance."""

    def __init__(self, sprite: str, color: str, size: int) -> None:
        """Initialize particle type."""
        self.sprite = sprite
        self.color = color
        self.size = size

    def render(self, x: int, y: int, velocity_x: float, velocity_y: float) -> str:
        """Render particle at position with velocity."""
        return f"{self.sprite}({self.color},{self.size}) at ({x},{y}) v=({velocity_x:.1f},{velocity_y:.1f})"


class Particle:
    """Particle with unique state."""

    def __init__(
        self,
        x: int,
        y: int,
        velocity_x: float,
        velocity_y: float,
        particle_type: ParticleType,
    ) -> None:
        """Initialize particle."""
        # Extrinsic state (unique)
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        # Intrinsic state (shared)
        self.type = particle_type

    def render(self) -> str:
        """Render this particle."""
        return self.type.render(self.x, self.y, self.velocity_x, self.velocity_y)


class ParticleSystem:
    """
    Particle system using flyweight pattern.

    Examples:
        >>> system = ParticleSystem()
        >>> system.add_particle_type("smoke", "*", "gray", 2)
        >>> system.spawn_particle("smoke", 100, 200, 1.5, -2.0)
        >>> system.spawn_particle("smoke", 105, 205, 1.2, -1.8)
        >>> len(system.particles)
        2
        >>> len(system.particle_types)  # Only 1 type shared
        1
    """

    def __init__(self) -> None:
        """Initialize particle system."""
        self.particles: list[Particle] = []
        self.particle_types: dict[str, ParticleType] = {}

    def add_particle_type(
        self,
        name: str,
        sprite: str,
        color: str,
        size: int,
    ) -> None:
        """Register a particle type."""
        self.particle_types[name] = ParticleType(sprite, color, size)

    def spawn_particle(
        self,
        type_name: str,
        x: int,
        y: int,
        velocity_x: float,
        velocity_y: float,
    ) -> None:
        """Spawn a particle of given type."""
        particle_type = self.particle_types[type_name]
        particle = Particle(x, y, velocity_x, velocity_y, particle_type)
        self.particles.append(particle)

    def render(self, limit: int = 5) -> list[str]:
        """Render particles."""
        return [p.render() for p in self.particles[:limit]]


def demonstrate_all() -> None:
    """Demonstrate Flyweight pattern."""
    print("=== Flyweight Pattern ===\n")

    # Text document example
    print("1. Text Document:")
    doc = Document()

    # Add text with same style (reuses flyweight)
    doc.add_text("Hello ", "Arial", 12, "black")
    doc.add_text("World", "Arial", 12, "black")

    # Add text with different style (creates new flyweight)
    doc.add_text("!", "Arial", 24, "red")

    print(f"   Characters: {doc.get_character_count()}")
    print(f"   Unique styles: {doc.get_style_count()}")
    print("\n   First few characters:")
    print(doc.render())
    print()

    # Particle system example
    print("2. Particle System:")
    system = ParticleSystem()

    # Register particle types (flyweights)
    system.add_particle_type("smoke", "*", "gray", 2)
    system.add_particle_type("fire", "+", "red", 3)
    system.add_particle_type("spark", ".", "yellow", 1)

    # Spawn many particles (share types)
    system.spawn_particle("smoke", 100, 100, 1.0, -2.0)
    system.spawn_particle("smoke", 102, 98, 0.8, -1.9)
    system.spawn_particle("fire", 100, 95, 0.5, -3.0)
    system.spawn_particle("spark", 101, 99, 2.0, -1.0)
    system.spawn_particle("smoke", 99, 101, 1.2, -2.1)

    print(f"   Particles: {len(system.particles)}")
    print(f"   Particle types: {len(system.particle_types)}")
    print("\n   Rendered particles:")
    for rendered in system.render():
        print(f"     {rendered}")


def memory_comparison() -> None:
    """Compare memory usage with and without flyweight."""
    print("\n=== Memory Comparison ===\n")

    import sys

    # Without flyweight (each character stores full style)
    class CharacterWithoutFlyweight:
        def __init__(self, char: str, font: str, size: int, color: str):
            self.char = char
            self.font = font  # Duplicated!
            self.size = size  # Duplicated!
            self.color = color  # Duplicated!

    # With flyweight
    style_factory = StyleFactory()
    style = style_factory.get_style("Arial", 12, "black")

    char_without = CharacterWithoutFlyweight("A", "Arial", 12, "black")
    char_with = Character("A", style, 0)

    print(f"Without flyweight: ~{sys.getsizeof(char_without)} bytes per character")
    print(f"With flyweight: ~{sys.getsizeof(char_with)} bytes per character")
    print("   (Style object is shared among all characters)")


if __name__ == "__main__":
    demonstrate_all()
    memory_comparison()

