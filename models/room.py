"""Room models for the Hotel Management System."""
from abc import ABC, abstractmethod


class Room(ABC):
    """Abstract base class for hotel rooms."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, room_id, room_number, floor, price, status="available"):
        """
        Initialize a room.

        Args:
            room_id: Unique identifier for the room
            room_number: Room number
            floor: Floor number
            price: Price per night
            status: Room status (available/unavailable)
        """
        self.room_id = room_id
        self.room_number = room_number
        self.floor = floor
        self.price = price
        self.status = status
        self.capacity = 1
        self.is_occupied = status != "available"

    @abstractmethod
    def get_room_type(self):
        """Get the type of room."""

    def to_dict(self):
        """Convert room to dictionary representation."""
        return {
            "room_id": self.room_id,
            "room_number": self.room_number,
            "floor": self.floor,
            "room_type": self.get_room_type(),
            "price": self.price,
            "status": self.status,
            "capacity": self.capacity,
            "is_occupied": self.is_occupied
        }

    @staticmethod
    def from_dict(data):
        """Create a room from dictionary data."""
        room_type = data.get("room_type", "SingleRoom")
        if room_type == "SingleRoom":
            return SingleRoom.from_dict(data)
        if room_type == "DoubleRoom":
            return DoubleRoom.from_dict(data)
        if room_type == "Suite":
            return Suite.from_dict(data)
        return None

    def __str__(self):
        """Return string representation of room."""
        return f"Room {self.room_number} ({self.get_room_type()}) - ${self.price} - {self.status}"


class SingleRoom(Room):
    """Single occupancy room (capacity: 1)."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, room_id, room_number, floor, price, status="available"):
        """
        Initialize a single room.

        Args:
            room_id: Unique identifier for the room
            room_number: Room number
            floor: Floor number
            price: Price per night
            status: Room status (available/unavailable)
        """
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 1

    def get_room_type(self):
        """Get room type."""
        return "SingleRoom"

    @staticmethod
    def from_dict(data):
        """Create a single room from dictionary data."""
        room = SingleRoom(
            data["room_id"],
            data["room_number"],
            data["floor"],
            data["price"],
            data.get("status", "available")
        )
        room.is_occupied = data.get("is_occupied", False)
        return room


class DoubleRoom(Room):
    """Double occupancy room (capacity: 2)."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, room_id, room_number, floor, price, status="available"):
        """
        Initialize a double room.

        Args:
            room_id: Unique identifier for the room
            room_number: Room number
            floor: Floor number
            price: Price per night
            status: Room status (available/unavailable)
        """
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 2

    def get_room_type(self):
        """Get room type."""
        return "DoubleRoom"

    @staticmethod
    def from_dict(data):
        """Create a double room from dictionary data."""
        room = DoubleRoom(
            data["room_id"],
            data["room_number"],
            data["floor"],
            data["price"],
            data.get("status", "available")
        )
        room.is_occupied = data.get("is_occupied", False)
        return room


class Suite(Room):
    """Suite room with luxury amenities (capacity: 4)."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, room_id, room_number, floor, price, status="available"):
        """
        Initialize a suite room.

        Args:
            room_id: Unique identifier for the room
            room_number: Room number
            floor: Floor number
            price: Price per night
            status: Room status (available/unavailable)
        """
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 4

    def get_room_type(self):
        """Get room type."""
        return "Suite"

    @staticmethod
    def from_dict(data):
        """Create a suite room from dictionary data."""
        room = Suite(
            data["room_id"],
            data["room_number"],
            data["floor"],
            data["price"],
            data.get("status", "available")
        )
        room.is_occupied = data.get("is_occupied", False)
        return room
