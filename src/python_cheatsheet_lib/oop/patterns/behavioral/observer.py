"""
Observer Pattern - Define one-to-many dependency between objects.

When one object changes state, all dependents are notified automatically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# Subject
class Subject(ABC):
    """Subject that observers can subscribe to."""

    def __init__(self) -> None:
        """Initialize with empty observers."""
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        self._observers.remove(observer)

    def notify(self, event: str, data: Any = None) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(event, data)


# Observer
class Observer(ABC):
    """Observer interface."""

    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        """Receive update from subject."""
        pass


# Concrete subject
class StockMarket(Subject):
    """
    Stock market that observers watch.

    Examples:
        >>> market = StockMarket()
        >>> investor = EmailNotifier("investor@example.com")
        >>> market.attach(investor)
        >>> market.set_price("AAPL", 150.0)
        Email to investor@example.com: Stock price changed: AAPL = $150.00
    """

    def __init__(self) -> None:
        """Initialize stock market."""
        super().__init__()
        self._prices: dict[str, float] = {}

    def set_price(self, symbol: str, price: float) -> None:
        """Set stock price and notify observers."""
        self._prices[symbol] = price
        self.notify("price_changed", {"symbol": symbol, "price": price})

    def get_price(self, symbol: str) -> float | None:
        """Get current price."""
        return self._prices.get(symbol)


# Concrete observers
class EmailNotifier(Observer):
    """Send email notifications."""

    def __init__(self, email: str) -> None:
        """Initialize with email."""
        self.email = email

    def update(self, event: str, data: Any) -> None:
        """Handle update."""
        if event == "price_changed":
            symbol = data["symbol"]
            price = data["price"]
            print(f"Email to {self.email}: Stock price changed: {symbol} = ${price:.2f}")


class SMSNotifier(Observer):
    """Send SMS notifications."""

    def __init__(self, phone: str) -> None:
        """Initialize with phone."""
        self.phone = phone

    def update(self, event: str, data: Any) -> None:
        """Handle update."""
        if event == "price_changed":
            symbol = data["symbol"]
            price = data["price"]
            print(f"SMS to {self.phone}: {symbol} -> ${price:.2f}")


class Logger(Observer):
    """Log all events."""

    def update(self, event: str, data: Any) -> None:
        """Log event."""
        print(f"LOG: Event '{event}' with data {data}")


# Pythonic approach with callbacks
class EventEmitter:
    """
    Simple event emitter using callbacks.

    Examples:
        >>> emitter = EventEmitter()
        >>> emitter.on("data", lambda x: print(f"Data: {x}"))
        >>> emitter.emit("data", 42)
        Data: 42
    """

    def __init__(self) -> None:
        """Initialize event emitter."""
        self._listeners: dict[str, list[Any]] = {}

    def on(self, event: str, callback: Any) -> None:
        """Register event listener."""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Any) -> None:
        """Remove event listener."""
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Emit event to all listeners."""
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)


def demonstrate_all() -> None:
    """Demonstrate Observer pattern."""
    print("=== Observer Pattern ===\n")

    # Stock market example
    print("1. Stock Market:")
    market = StockMarket()

    email_obs = EmailNotifier("trader@example.com")
    sms_obs = SMSNotifier("+1234567890")
    logger = Logger()

    market.attach(email_obs)
    market.attach(sms_obs)
    market.attach(logger)

    market.set_price("AAPL", 150.0)
    print()
    market.set_price("GOOGL", 2800.0)
    print()

    # Remove observer
    market.detach(sms_obs)
    print("After removing SMS observer:")
    market.set_price("AAPL", 155.0)
    print()

    # Event emitter
    print("2. Event Emitter:")
    emitter = EventEmitter()

    def on_connect(addr: str) -> None:
        print(f"   Connected to {addr}")

    def on_data(data: str) -> None:
        print(f"   Received: {data}")

    emitter.on("connect", on_connect)
    emitter.on("data", on_data)

    emitter.emit("connect", "192.168.1.1")
    emitter.emit("data", "Hello, World!")


if __name__ == "__main__":
    demonstrate_all()

