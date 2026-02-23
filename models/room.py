from abc import ABC, abstractmethod


class Room(ABC):
    def __init__(self, room_id, room_number, floor, price, status="available"):
        self.room_id = room_id
        self.room_number = room_number
        self.floor = floor
        self.price = price
        self.status = status
        self.capacity = 1
        self.is_occupied = status != "available"

    @abstractmethod
    def get_room_type(self):
        pass

    def to_dict(self):
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
        room_type = data.get("room_type", "SingleRoom")
        if room_type == "SingleRoom":
            return SingleRoom.from_dict(data)
        elif room_type == "DoubleRoom":
            return DoubleRoom.from_dict(data)
        elif room_type == "Suite":
            return Suite.from_dict(data)
        return None

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type()}) - ${self.price} - {self.status}"


class SingleRoom(Room):
    def __init__(self, room_id, room_number, floor, price, status="available"):
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 1

    def get_room_type(self):
        return "SingleRoom"

    @staticmethod
    def from_dict(data):
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
    def __init__(self, room_id, room_number, floor, price, status="available"):
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 2

    def get_room_type(self):
        return "DoubleRoom"

    @staticmethod
    def from_dict(data):
        room = DoubleRoom(
            data["room_id"],
            data["room_number"],
            data["room_number"],
            data["price"],
            data.get("status", "available")
        )
        room.is_occupied = data.get("is_occupied", False)
        return room


class Suite(Room):
    def __init__(self, room_id, room_number, floor, price, status="available"):
        super().__init__(room_id, room_number, floor, price, status)
        self.capacity = 4

    def get_room_type(self):
        return "Suite"

    @staticmethod
    def from_dict(data):
        room = Suite(
            data["room_id"],
            data["room_number"],
            data["floor"],
            data["price"],
            data.get("status", "available")
        )
        room.is_occupied = data.get("is_occupied", False)
        return room
