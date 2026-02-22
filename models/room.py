from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, room_id, room_number, floor, price, status="available"):
        self.room_id = room_id
        self.room_number = room_number
        self.floor = floor
        self.price = price
        self.status = status

    @abstractmethod
    def get_capacity(self):
        pass

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
            "status": self.status
        }
    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type()}) - ${self.price} - {self.status}"


class SingleRoom(Room):
    def get_capacity(self):
        return 1

    def get_room_type(self):
        return "Single"


class DoubleRoom(Room):
    def get_capacity(self):
        return 2

    def get_room_type(self):
        return "Double"


class Suite(Room):
    def get_capacity(self):
        return 4

    def get_room_type(self):
        return "Suite"
