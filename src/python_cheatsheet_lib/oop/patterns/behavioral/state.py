"""
State Pattern - Alter behavior when internal state changes.

Object appears to change its class when its internal state changes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# State interface
class State(ABC):
    """Base state class."""

    @abstractmethod
    def insert_coin(self, machine: VendingMachine) -> str:
        """Handle coin insertion."""
        pass

    @abstractmethod
    def select_item(self, machine: VendingMachine) -> str:
        """Handle item selection."""
        pass

    @abstractmethod
    def dispense(self, machine: VendingMachine) -> str:
        """Handle dispensing."""
        pass


# Concrete states
class NoCoinState(State):
    """State when no coin is inserted."""

    def insert_coin(self, machine: VendingMachine) -> str:
        """Transition to has coin state."""
        machine.set_state(machine.has_coin_state)
        return "Coin inserted"

    def select_item(self, machine: VendingMachine) -> str:
        """Cannot select without coin."""
        return "Insert coin first"

    def dispense(self, machine: VendingMachine) -> str:
        """Cannot dispense without coin."""
        return "Insert coin first"


class HasCoinState(State):
    """State when coin is inserted."""

    def insert_coin(self, machine: VendingMachine) -> str:
        """Already has coin."""
        return "Coin already inserted"

    def select_item(self, machine: VendingMachine) -> str:
        """Select item and move to dispensing."""
        machine.set_state(machine.dispensing_state)
        return "Item selected"

    def dispense(self, machine: VendingMachine) -> str:
        """Must select item first."""
        return "Select item first"


class DispensingState(State):
    """State when dispensing item."""

    def insert_coin(self, machine: VendingMachine) -> str:
        """Cannot insert while dispensing."""
        return "Please wait, dispensing item"

    def select_item(self, machine: VendingMachine) -> str:
        """Cannot select while dispensing."""
        return "Already dispensing"

    def dispense(self, machine: VendingMachine) -> str:
        """Dispense and return to no coin state."""
        machine.set_state(machine.no_coin_state)
        return "Item dispensed"


# Context
class VendingMachine:
    """
    Vending machine that changes behavior based on state.

    Examples:
        >>> machine = VendingMachine()
        >>> machine.insert_coin()
        'Coin inserted'
        >>> machine.select_item()
        'Item selected'
        >>> machine.dispense()
        'Item dispensed'
    """

    def __init__(self) -> None:
        """Initialize vending machine."""
        # Create states
        self.no_coin_state = NoCoinState()
        self.has_coin_state = HasCoinState()
        self.dispensing_state = DispensingState()

        # Start in no coin state
        self._state = self.no_coin_state

    def set_state(self, state: State) -> None:
        """Set current state."""
        self._state = state

    def insert_coin(self) -> str:
        """Insert coin."""
        return self._state.insert_coin(self)

    def select_item(self) -> str:
        """Select item."""
        return self._state.select_item(self)

    def dispense(self) -> str:
        """Dispense item."""
        return self._state.dispense(self)


# Alternative: Using match-case (Python 3.10+)
class TCPConnection:
    """
    TCP connection using match-case for states.

    Examples:
        >>> conn = TCPConnection()
        >>> conn.open()
        'Connection established'
        >>> conn.send("data")
        'Sent: data'
        >>> conn.close()
        'Connection closed'
    """

    def __init__(self) -> None:
        """Initialize in closed state."""
        self.state = "closed"

    def open(self) -> str:
        """Open connection."""
        match self.state:
            case "closed":
                self.state = "established"
                return "Connection established"
            case "established":
                return "Already connected"
            case _:
                return "Invalid state"

    def send(self, data: str) -> str:
        """Send data."""
        match self.state:
            case "established":
                return f"Sent: {data}"
            case "closed":
                return "Connection not open"
            case _:
                return "Invalid state"

    def close(self) -> str:
        """Close connection."""
        match self.state:
            case "established":
                self.state = "closed"
                return "Connection closed"
            case "closed":
                return "Already closed"
            case _:
                return "Invalid state"


def demonstrate_all() -> None:
    """Demonstrate State pattern."""
    print("=== State Pattern ===\n")

    # Vending machine
    print("1. Vending Machine:")
    machine = VendingMachine()

    print(f"   {machine.select_item()}")  # No coin
    print(f"   {machine.insert_coin()}")  # Insert coin
    print(f"   {machine.insert_coin()}")  # Try again
    print(f"   {machine.select_item()}")  # Select
    print(f"   {machine.dispense()}")  # Dispense
    print()

    # TCP connection
    print("2. TCP Connection:")
    conn = TCPConnection()

    print(f"   {conn.send('data')}")  # Not open
    print(f"   {conn.open()}")  # Open
    print(f"   {conn.send('Hello')}")  # Send
    print(f"   {conn.close()}")  # Close
    print(f"   {conn.send('data')}")  # Closed again


if __name__ == "__main__":
    demonstrate_all()
