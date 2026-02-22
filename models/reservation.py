from abc import ABC, abstractmethod
from datetime import datetime

class Reservation(ABC):
    def __init__(self, reservation_id, customer_id, room_id, hotel_id,
                 check_in_date, check_out_date, number_of_guests, status="pending"):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.check_in_date = check_in_date if isinstance(check_in_date, datetime) else datetime.fromisoformat(check_in_date)
        self.check_out_date = check_out_date if isinstance(check_out_date, datetime) else datetime.fromisoformat(check_out_date)
        self.number_of_guests = number_of_guests
        self.status = status

    @abstractmethod
    def calculate_total_cost(self, room_price):
        """Each reservation type calculates cost differently"""
        pass

    @abstractmethod
    def get_cancellation_policy(self):
        """Each reservation type has different cancellation rules"""
        pass

    def get_nights(self):
        delta = self.check_out_date - self.check_in_date
        return delta.days

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "reservation_type": self.__class__.__name__,
            "customer_id": self.customer_id,
            "room_id": self.room_id,
            "hotel_id": self.hotel_id,
            "check_in_date": self.check_in_date.isoformat(),
            "check_out_date": self.check_out_date.isoformat(),
            "number_of_guests": self.number_of_guests,
            "status": self.status
        }

    def __str__(self):
        return f"Reservation {self.reservation_id} - {self.status} - {self.get_nights()} nights"


class StandardReservation(Reservation):
    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights()

    def get_cancellation_policy(self):
        return "Free cancellation up to 24 hours before check-in"


class VIPReservation(Reservation):
    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights() * 0.85  # 15% discount

    def get_cancellation_policy(self):
        return "Free cancellation up to 2 hours before check-in"


class CorporateReservation(Reservation):
    def calculate_total_cost(self, room_price):
        return room_price * self.get_nights() * 0.90  # 10% discount

    def get_cancellation_policy(self):
        return "Free cancellation up to 48 hours before check-in"
