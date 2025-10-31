"""
EAFP vs LBYL - Two approaches to error handling.

EAFP: Easier to Ask for Forgiveness than Permission (try/except)
LBYL: Look Before You Leap (if/else checks)
"""

from __future__ import annotations


def lbyl_approach(data: dict[str, int], key: str) -> int:
    """
    Look Before You Leap - check before accessing.

    Examples:
        >>> lbyl_approach({"a": 1}, "a")
        1
        >>> lbyl_approach({"a": 1}, "b")
        0
    """
    if key in data:
        return data[key]
    else:
        return 0


def eafp_approach(data: dict[str, int], key: str) -> int:
    """
    Easier to Ask Forgiveness than Permission - try and handle errors.

    Examples:
        >>> eafp_approach({"a": 1}, "a")
        1
        >>> eafp_approach({"a": 1}, "b")
        0
    """
    try:
        return data[key]
    except KeyError:
        return 0


def demonstrate_all() -> None:
    """Demonstrate EAFP vs LBYL."""
    print("=== EAFP vs LBYL ===\n")

    data = {"x": 10, "y": 20}

    print("LBYL (Look Before You Leap):")
    print(f"   {lbyl_approach(data, 'x')}")
    print(f"   {lbyl_approach(data, 'z')}")

    print("\nEAFP (Easier to Ask Forgiveness):")
    print(f"   {eafp_approach(data, 'x')}")
    print(f"   {eafp_approach(data, 'z')}")


if __name__ == "__main__":
    demonstrate_all()
