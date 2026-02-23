from abc import ABC, abstractmethod
from datetime import datetime


class Reservation(ABC):
    def __init__(self, reservation_id, customer_id, hotel_id, room_id,
                 check_in, check_out, number_of_guests, status="pending"):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.number_of_guests = number_of_guests
        self.status = status
        self.reservation_type = "Standard"

    @abstractmethod
    def calculate_total_cost(self, room_price):
        """Each reservation type calculates cost differently"""
        pass

    @abstractmethod
    def get_cancellation_policy(self):
        """Each reservation type has different cancellation rules"""
        pass

    def get_nights(self):
        check_in_dt = datetime.fromisoformat(self.check_in)
        check_out_dt = datetime.fromisoformat(self.check_out)
        delta = check_out_dt - check_in_dt
        return delta.days

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "reservation_type": self.reservation_type,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_id": self.room_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "number_of_guests": self.number_of_guests,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        res_type = data.get("reservation_type", "Standard")
        if res_type == "VIP":
            return VIPReservation.from_dict(data)
        elif res_type == "Corporate":
            return CorporateReservation.from_dict(data)
        return StandardReservation.from_dict(data)

    def __str__(self):
        return (
            f"Reservation {self.reservation_id} for Customer "
            f"{self.customer_id} - {self.status} - {self.get_nights()} nights"
        )


class StandardReservation(Reservation):
    def __init__(
        self,
        reservation_id,
        customer_id,
        hotel_id,
        room_id,
        check_in,
        check_out,
        number_of_guests,
        status="pending"
    ):
        super().__init__(
            reservation_id,
            customer_id,
            hotel_id,
            room_id,
            check_in,
            check_out,
            number_of_guests,
            status
        )
        self.reservation_type = "Standard"

    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights()

    def get_cancellation_policy(self):
        return "Free cancellation up to 24 hours before check-in"

    @staticmethod
    def from_dict(data):
        return StandardReservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["room_id"],
            data["check_in"],
            data["check_out"],
            data["number_of_guests"],
            data.get("status", "pending")
        )


class VIPReservation(Reservation):
    def __init__(
        self,
        reservation_id,
        customer_id,
        hotel_id,
        room_id,
        check_in,
        check_out,
        number_of_guests,
        status="pending"
    ):
        super().__init__(
            reservation_id,
            customer_id,
            hotel_id,
            room_id,
            check_in,
            check_out,
            number_of_guests,
            status
        )
        self.reservation_type = "VIP"

    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights() * 0.85  # 15% discount

    def get_cancellation_policy(self):
        return "Free cancellation up to 2 hours before check-in"

    @staticmethod
    def from_dict(data):
        return VIPReservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["room_id"],
            data["check_in"],
            data["check_out"],
            data["number_of_guests"],
            data.get("status", "pending")
        )


class CorporateReservation(Reservation):
    def __init__(
        self,
        reservation_id,
        customer_id,
        hotel_id,
        room_id,
        check_in,
        check_out,
        number_of_guests,
        status="pending"
    ):
        super().__init__(
            reservation_id,
            customer_id,
            hotel_id,
            room_id,
            check_in,
            check_out,
            number_of_guests,
            status
        )
        self.reservation_type = "Corporate"

    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights() * 0.90  # 10% discount

    def get_cancellation_policy(self):
        return "Free cancellation up to 48 hours before check-in"

    @staticmethod
    def from_dict(data):
        return CorporateReservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["room_id"],
            data["check_in"],
            data["check_out"],
            data["number_of_guests"],
            data.get("status", "pending")
        )
