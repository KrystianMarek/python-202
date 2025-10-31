"""
Strategy Pattern - Define family of algorithms, make them interchangeable.

Encapsulates algorithms and makes them interchangeable at runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Protocol


# Strategy interface
class SortStrategy(ABC):
    """Strategy for sorting."""

    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        """Sort the data."""
        pass


# Concrete strategies
class BubbleSort(SortStrategy):
    """Bubble sort strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Implement bubble sort."""
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSort(SortStrategy):
    """Quick sort strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Implement quick sort."""
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class MergeSort(SortStrategy):
    """Merge sort strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Implement merge sort."""
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])

        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        """Merge two sorted lists."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


# Context
class Sorter:
    """
    Sorter that uses a strategy.

    Examples:
        >>> sorter = Sorter(QuickSort())
        >>> sorter.sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
        >>> sorter.set_strategy(BubbleSort())
        >>> sorter.sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
    """

    def __init__(self, strategy: SortStrategy) -> None:
        """Initialize with strategy."""
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change strategy at runtime."""
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        """Sort using current strategy."""
        return self._strategy.sort(data)


# Pythonic approach: Functions as strategies
def compression_zip(data: str) -> str:
    """ZIP compression."""
    return f"ZIP({data})"


def compression_rar(data: str) -> str:
    """RAR compression."""
    return f"RAR({data})"


def compression_gzip(data: str) -> str:
    """GZIP compression."""
    return f"GZIP({data})"


class Compressor:
    """
    Compressor using function strategies.

    Examples:
        >>> comp = Compressor(compression_zip)
        >>> comp.compress("data")
        'ZIP(data)'
        >>> comp.set_strategy(compression_gzip)
        >>> comp.compress("data")
        'GZIP(data)'
    """

    def __init__(self, strategy: Callable[[str], str]) -> None:
        """Initialize with compression function."""
        self._strategy = strategy

    def set_strategy(self, strategy: Callable[[str], str]) -> None:
        """Change compression strategy."""
        self._strategy = strategy

    def compress(self, data: str) -> str:
        """Compress using current strategy."""
        return self._strategy(data)


# Payment strategy example
class PaymentStrategy(Protocol):
    """Payment strategy protocol."""

    def pay(self, amount: float) -> str:
        """Process payment."""
        ...


class CreditCardPayment:
    """Credit card payment."""

    def __init__(self, card_number: str) -> None:
        """Initialize with card number."""
        self.card_number = card_number

    def pay(self, amount: float) -> str:
        """Pay with credit card."""
        return f"Paid ${amount:.2f} with card ending in {self.card_number[-4:]}"


class PayPalPayment:
    """PayPal payment."""

    def __init__(self, email: str) -> None:
        """Initialize with email."""
        self.email = email

    def pay(self, amount: float) -> str:
        """Pay with PayPal."""
        return f"Paid ${amount:.2f} via PayPal ({self.email})"


class CryptoPayment:
    """Cryptocurrency payment."""

    def __init__(self, wallet: str) -> None:
        """Initialize with wallet address."""
        self.wallet = wallet

    def pay(self, amount: float) -> str:
        """Pay with crypto."""
        return f"Paid ${amount:.2f} via crypto to {self.wallet[:10]}..."


class ShoppingCart:
    """Shopping cart with payment strategy."""

    def __init__(self) -> None:
        """Initialize cart."""
        self._items: list[tuple[str, float]] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, item: str, price: float) -> None:
        """Add item to cart."""
        self._items.append((item, price))

    def set_payment_method(self, strategy: PaymentStrategy) -> None:
        """Set payment method."""
        self._payment_strategy = strategy

    def checkout(self) -> str:
        """Process payment."""
        total = sum(price for _, price in self._items)
        if self._payment_strategy is None:
            return "No payment method selected"
        return self._payment_strategy.pay(total)


def demonstrate_all() -> None:
    """Demonstrate Strategy pattern."""
    print("=== Strategy Pattern ===\n")

    # Sorting strategies
    print("1. Sorting Strategies:")
    data = [64, 34, 25, 12, 22, 11, 90]

    sorter = Sorter(BubbleSort())
    print(f"   Bubble Sort: {sorter.sort(data)}")

    sorter.set_strategy(QuickSort())
    print(f"   Quick Sort:  {sorter.sort(data)}")

    sorter.set_strategy(MergeSort())
    print(f"   Merge Sort:  {sorter.sort(data)}")
    print()

    # Compression strategies
    print("2. Compression Strategies:")
    compressor = Compressor(compression_zip)
    print(f"   {compressor.compress('hello world')}")

    compressor.set_strategy(compression_gzip)
    print(f"   {compressor.compress('hello world')}")
    print()

    # Payment strategies
    print("3. Payment Strategies:")
    cart = ShoppingCart()
    cart.add_item("Book", 29.99)
    cart.add_item("Pen", 4.99)

    cart.set_payment_method(CreditCardPayment("1234567890123456"))
    print(f"   {cart.checkout()}")

    cart.set_payment_method(PayPalPayment("user@example.com"))
    print(f"   {cart.checkout()}")

    cart.set_payment_method(CryptoPayment("0x1234567890abcdef"))
    print(f"   {cart.checkout()}")


if __name__ == "__main__":
    demonstrate_all()

