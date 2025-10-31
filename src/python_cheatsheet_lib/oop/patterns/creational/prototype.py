"""
Prototype Pattern - Clone objects instead of creating them from scratch.

Creates new objects by copying existing prototypes, useful when
object creation is expensive or complex.
"""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# Simple prototype with copy module
@dataclass
class Character:
    """
    Game character that can be cloned.

    Examples:
        >>> warrior = Character("Warrior", 100, 50, ["sword", "shield"])
        >>> mage = copy.copy(warrior)
        >>> mage.name = "Mage"
        >>> mage.inventory.append("staff")
        >>> "staff" in warrior.inventory  # Shallow copy shares list!
        True
    """

    name: str
    health: int
    mana: int
    inventory: list[str] = field(default_factory=list)


    def clone(self) -> Character:
        """
        Create a deep copy of this character.

        Returns:
            New Character instance with copied attributes

        Examples:
            >>> warrior = Character("Warrior", 100, 50, ["sword"])
            >>> mage = warrior.clone()
            >>> mage.name = "Mage"
            >>> mage.inventory.append("staff")
            >>> "staff" in warrior.inventory  # Deep copy, separate lists
            False
        """
        return copy.deepcopy(self)


# Prototype with custom copy logic
class Monster(ABC):
    """Abstract monster class with prototype pattern."""

    def __init__(self, health: int, damage: int) -> None:
        """Initialize monster."""
        self.health = health
        self.damage = damage
        self.position = (0, 0)

    @abstractmethod
    def attack(self) -> str:
        """Attack behavior."""
        pass

    def __copy__(self) -> Monster:
        """Shallow copy."""
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo: dict[int, object]) -> Monster:
        """
        Deep copy with memo to handle circular references.

        Args:
            memo: Dictionary tracking already copied objects

        Returns:
            Deep copy of monster
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for key, value in self.__dict__.items():
            setattr(result, key, copy.deepcopy(value, memo))

        return result

    def clone(self) -> Monster:
        """Create a deep copy."""
        return copy.deepcopy(self)


class Dragon(Monster):
    """Dragon monster."""

    def __init__(self, health: int, damage: int, fire_power: int) -> None:
        """Initialize dragon."""
        super().__init__(health, damage)
        self.fire_power = fire_power
        self.treasure: list[str] = []

    def attack(self) -> str:
        """Dragon breathes fire."""
        return f"Dragon breathes fire! Damage: {self.damage + self.fire_power}"


class Goblin(Monster):
    """Goblin monster."""

    def __init__(self, health: int, damage: int, sneakiness: int) -> None:
        """Initialize goblin."""
        super().__init__(health, damage)
        self.sneakiness = sneakiness
        self.stolen_items: list[str] = []

    def attack(self) -> str:
        """Goblin sneaks and attacks."""
        return f"Goblin sneaks! Damage: {self.damage}"


# Prototype registry
class MonsterRegistry:
    """
    Registry of prototype monsters.

    Why use a registry?
    - Centralized prototype management
    - Easy to add new prototypes
    - Named prototypes for clarity
    - Reduces redundant initialization

    Examples:
        >>> registry = MonsterRegistry()
        >>> dragon = registry.get("dragon")
        >>> dragon.position = (10, 20)
        >>> dragon2 = registry.get("dragon")
        >>> dragon2.position  # Fresh copy
        (0, 0)
    """

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._prototypes: dict[str, Monster] = {}

    def register(self, name: str, prototype: Monster) -> None:
        """
        Register a prototype.

        Args:
            name: Name for the prototype
            prototype: Monster instance to use as prototype
        """
        self._prototypes[name] = prototype

    def unregister(self, name: str) -> None:
        """Remove a prototype from registry."""
        del self._prototypes[name]

    def get(self, name: str) -> Monster:
        """
        Get a clone of the named prototype.

        Args:
            name: Name of prototype

        Returns:
            Cloned monster

        Raises:
            KeyError: If prototype not found
        """
        prototype = self._prototypes.get(name)
        if prototype is None:
            raise KeyError(f"Prototype '{name}' not found")
        return prototype.clone()


# Complex object with nested structures
@dataclass
class Weapon:
    """Weapon with stats."""

    name: str
    damage: int
    enchantments: list[str] = field(default_factory=list)


@dataclass
class Player:
    """
    Player with complex nested objects.

    Demonstrates cloning of complex hierarchies.
    """

    name: str
    level: int
    weapon: Weapon | None = None
    skills: dict[str, int] = field(default_factory=dict)
    party_members: list[Player] = field(default_factory=list)

    def clone(self) -> Player:
        """
        Create deep copy avoiding circular references.

        Returns:
            Cloned player
        """
        return copy.deepcopy(self)


def demonstrate_all() -> None:
    """Demonstrate Prototype pattern."""
    print("=== Prototype Pattern ===\n")

    # Basic cloning
    print("1. Basic Character Cloning:")
    warrior = Character("Warrior", 100, 50, ["sword", "shield"])
    mage = warrior.clone()
    mage.name = "Mage"
    mage.health = 70
    mage.mana = 100
    mage.inventory = ["staff", "robe"]
    print(f"   Original: {warrior.name}, HP: {warrior.health}, Items: {warrior.inventory}")
    print(f"   Clone: {mage.name}, HP: {mage.health}, Items: {mage.inventory}")
    print()

    # Monster cloning
    print("2. Monster Cloning:")
    dragon_proto = Dragon(health=500, damage=50, fire_power=30)
    dragon_proto.treasure = ["gold", "gems"]

    dragon1 = dragon_proto.clone()
    dragon1.position = (10, 20)
    dragon1.treasure.append("crown")

    dragon2 = dragon_proto.clone()
    dragon2.position = (30, 40)

    print(f"   Proto treasure: {dragon_proto.treasure}")
    print(f"   Dragon1 treasure: {dragon1.treasure}")
    print(f"   Dragon2 treasure: {dragon2.treasure}")
    print(f"   Dragon1 pos: {dragon1.position}, Dragon2 pos: {dragon2.position}")
    print()

    # Registry pattern
    print("3. Prototype Registry:")
    registry = MonsterRegistry()

    # Register prototypes
    registry.register("dragon", Dragon(500, 50, 30))
    registry.register("goblin", Goblin(50, 10, 5))

    # Create monsters from prototypes
    boss_dragon = registry.get("dragon")
    boss_dragon.health = 1000
    boss_dragon.damage = 100

    minion1 = registry.get("goblin")
    minion2 = registry.get("goblin")

    print(f"   Boss dragon: HP={boss_dragon.health}, DMG={boss_dragon.damage}")
    print(f"   Minion 1: HP={minion1.health}")
    print(f"   Minion 2: HP={minion2.health}")
    print(f"   Minions are separate: {minion1 is not minion2}")
    print()

    # Complex cloning
    print("4. Complex Object Cloning:")
    excalibur = Weapon("Excalibur", 100, ["holy", "sharp"])
    arthur = Player(
        name="Arthur",
        level=50,
        weapon=excalibur,
        skills={"swordsmanship": 95, "leadership": 90},
    )

    lancelot = arthur.clone()
    lancelot.name = "Lancelot"
    lancelot.weapon.name = "Arondight"  # type: ignore
    lancelot.skills["swordsmanship"] = 98

    print(f"   Arthur's weapon: {arthur.weapon.name if arthur.weapon else 'None'}")  # type: ignore
    print(f"   Lancelot's weapon: {lancelot.weapon.name if lancelot.weapon else 'None'}")  # type: ignore
    print(f"   Arthur's skill: {arthur.skills['swordsmanship']}")
    print(f"   Lancelot's skill: {lancelot.skills['swordsmanship']}")


def compare_copy_methods() -> None:
    """Compare shallow vs deep copy."""
    print("\n=== Shallow vs Deep Copy ===\n")

    original = Character("Original", 100, 50, ["item1", "item2"])

    # Shallow copy
    shallow = copy.copy(original)
    shallow.name = "Shallow"
    shallow.inventory.append("item3")

    # Deep copy
    deep = copy.deepcopy(original)
    deep.name = "Deep"
    deep.inventory.append("item4")

    print(f"Original: {original.name}, Items: {original.inventory}")
    print(f"Shallow:  {shallow.name}, Items: {shallow.inventory}")
    print(f"Deep:     {deep.name}, Items: {deep.inventory}")
    print(f"\nShallow copy shares inventory: {shallow.inventory is original.inventory}")
    print(f"Deep copy has separate inventory: {deep.inventory is not original.inventory}")


if __name__ == "__main__":
    demonstrate_all()
    compare_copy_methods()

