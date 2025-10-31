"""
Mediator Pattern - Define object that encapsulates how objects interact.

Reduces coupling by keeping objects from referring to each other explicitly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# Mediator interface
class ChatMediator(ABC):
    """Chat room mediator interface."""

    @abstractmethod
    def send_message(self, message: str, sender: User) -> None:
        """Send message through mediator."""
        pass

    @abstractmethod
    def add_user(self, user: User) -> None:
        """Add user to chat."""
        pass


# Concrete mediator
class ChatRoom(ChatMediator):
    """
    Chat room that mediates user communication.

    Examples:
        >>> room = ChatRoom()
        >>> alice = User("Alice", room)
        >>> bob = User("Bob", room)
        >>> room.add_user(alice)
        >>> room.add_user(bob)
        >>> alice.send("Hello Bob!")
        Alice: Hello Bob!
        Bob received: Hello Bob!
    """

    def __init__(self) -> None:
        """Initialize empty chat room."""
        self.users: list[User] = []

    def add_user(self, user: User) -> None:
        """Add user to room."""
        self.users.append(user)

    def send_message(self, message: str, sender: User) -> None:
        """Send message to all users except sender."""
        print(f"{sender.name}: {message}")
        for user in self.users:
            if user != sender:
                user.receive(message)


# Colleague
class User:
    """User that communicates through mediator."""

    def __init__(self, name: str, mediator: ChatMediator) -> None:
        """Initialize user with mediator."""
        self.name = name
        self.mediator = mediator

    def send(self, message: str) -> None:
        """Send message via mediator."""
        self.mediator.send_message(message, self)

    def receive(self, message: str) -> None:
        """Receive message."""
        print(f"{self.name} received: {message}")


# Air traffic control example
class ATCMediator(ABC):
    """Air traffic control mediator."""

    @abstractmethod
    def request_landing(self, aircraft: Aircraft) -> str:
        """Request landing permission."""
        pass

    @abstractmethod
    def request_takeoff(self, aircraft: Aircraft) -> str:
        """Request takeoff permission."""
        pass


class AirTrafficControl(ATCMediator):
    """
    Air traffic control tower.

    Examples:
        >>> atc = AirTrafficControl()
        >>> plane1 = Aircraft("Flight101", atc)
        >>> plane2 = Aircraft("Flight202", atc)
        >>> atc.request_landing(plane1)
        'Flight101: Landing approved'
        >>> atc.request_landing(plane2)
        'Flight202: Denied - runway occupied'
    """

    def __init__(self) -> None:
        """Initialize ATC."""
        self.runway_free = True

    def request_landing(self, aircraft: Aircraft) -> str:
        """Handle landing request."""
        if self.runway_free:
            self.runway_free = False
            return f"{aircraft.name}: Landing approved"
        else:
            return f"{aircraft.name}: Denied - runway occupied"

    def request_takeoff(self, aircraft: Aircraft) -> str:
        """Handle takeoff request."""
        if self.runway_free:
            return f"{aircraft.name}: Takeoff approved"
        else:
            self.runway_free = True
            return f"{aircraft.name}: Takeoff approved - runway now free"


class Aircraft:
    """Aircraft communicating through ATC."""

    def __init__(self, name: str, atc: ATCMediator) -> None:
        """Initialize aircraft."""
        self.name = name
        self.atc = atc

    def land(self) -> str:
        """Request landing."""
        return self.atc.request_landing(self)

    def takeoff(self) -> str:
        """Request takeoff."""
        return self.atc.request_takeoff(self)


def demonstrate_all() -> None:
    """Demonstrate Mediator pattern."""
    print("=== Mediator Pattern ===\n")

    # Chat room
    print("1. Chat Room:")
    room = ChatRoom()

    alice = User("Alice", room)
    bob = User("Bob", room)
    charlie = User("Charlie", room)

    room.add_user(alice)
    room.add_user(bob)
    room.add_user(charlie)

    alice.send("Hello everyone!")
    print()
    bob.send("Hi Alice!")
    print()

    # Air traffic control
    print("2. Air Traffic Control:")
    atc = AirTrafficControl()

    flight1 = Aircraft("AA101", atc)
    flight2 = Aircraft("UA202", atc)

    print(f"   {flight1.land()}")
    print(f"   {flight2.land()}")
    print(f"   {flight1.takeoff()}")
    print(f"   {flight2.land()}")


if __name__ == "__main__":
    demonstrate_all()

