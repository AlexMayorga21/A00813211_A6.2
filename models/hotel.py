from models.room import Room


class Hotel:
    def __init__(self, hotel_id, name, address, description):
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.description = description
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def remove_room(self, room_id):
        self.rooms = [room for room in self.rooms if room.room_id != room_id]

    def get_room(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None

    def get_available_rooms(self):
        return [room for room in self.rooms if not room.is_occupied]

    def to_dict(self):
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "address": self.address,
            "description": self.description,
            "rooms": [room.to_dict() for room in self.rooms]
        }

    @staticmethod
    def from_dict(data):
        hotel = Hotel(
            data["hotel_id"],
            data["name"],
            data["address"],
            data["description"]
        )

        for room_data in data.get("rooms", []):
            room = Room.from_dict(room_data)
            if room:
                hotel.add_room(room)

        return hotel

    def __str__(self):
        return f"{self.hotel_id}: {self.name} ({self.address}) - {len(self.rooms)} rooms"
