"""Reservation models for the Hotel Management System."""
from abc import ABC, abstractmethod
from datetime import datetime


class Reservation(ABC):
    """Abstract base class for hotel reservations."""

    # pylint: disable=too-many-arguments,too-many-instance-attributes,too-many-positional-arguments
    def __init__(self, reservation_id, customer_id, hotel_id, room_id,
                 check_in, check_out, number_of_guests, status="pending"):
        """
        Initialize a reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer making the reservation
            hotel_id: ID of the hotel
            room_id: ID of the reserved room
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
            number_of_guests: Number of guests
            status: Reservation status (pending/confirmed/cancelled)
        """
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
        """Calculate total cost based on reservation type."""

    @abstractmethod
    def get_cancellation_policy(self):
        """Get cancellation policy for this reservation type."""

    def get_nights(self):
        """Calculate the number of nights in the reservation."""
        check_in_dt = datetime.fromisoformat(self.check_in)
        check_out_dt = datetime.fromisoformat(self.check_out)
        delta = check_out_dt - check_in_dt
        return delta.days

    def to_dict(self):
        """Convert reservation to dictionary representation."""
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
        """Create a reservation from dictionary data."""
        res_type = data.get("reservation_type", "Standard")
        if res_type == "VIP":
            return VIPReservation.from_dict(data)
        if res_type == "Corporate":
            return CorporateReservation.from_dict(data)
        return StandardReservation.from_dict(data)

    def __str__(self):
        """Return string representation of reservation."""
        return (
            f"Reservation {self.reservation_id} for Customer "
            f"{self.customer_id} - {self.status} - {self.get_nights()} nights"
        )


class StandardReservation(Reservation):
    """Standard reservation with flexible cancellation policy."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        """
        Initialize a standard reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer making the reservation
            hotel_id: ID of the hotel
            room_id: ID of the reserved room
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
            number_of_guests: Number of guests
            status: Reservation status (pending/confirmed/cancelled)
        """
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
        """Calculate total cost for standard reservation."""
        return room_price * self.get_nights()

    def get_cancellation_policy(self):
        """Get cancellation policy for standard reservation."""
        return "Free cancellation up to 24 hours before check-in"

    @staticmethod
    def from_dict(data):
        """Create a standard reservation from dictionary data."""
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
    """VIP reservation with preferential rates and cancellation terms."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        """
        Initialize a VIP reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer making the reservation
            hotel_id: ID of the hotel
            room_id: ID of the reserved room
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
            number_of_guests: Number of guests
            status: Reservation status (pending/confirmed/cancelled)
        """
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
        """Calculate total cost for VIP reservation (15% discount)."""
        return room_price * self.get_nights() * 0.85

    def get_cancellation_policy(self):
        """Get cancellation policy for VIP reservation."""
        return "Free cancellation up to 2 hours before check-in"

    @staticmethod
    def from_dict(data):
        """Create a VIP reservation from dictionary data."""
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
    """Corporate reservation with corporate rates and policies."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        """
        Initialize a corporate reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer making the reservation
            hotel_id: ID of the hotel
            room_id: ID of the reserved room
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
            number_of_guests: Number of guests
            status: Reservation status (pending/confirmed/cancelled)
        """
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
        """Calculate total cost for corporate reservation (10% discount)."""
        return room_price * self.get_nights() * 0.90

    def get_cancellation_policy(self):
        """Get cancellation policy for corporate reservation."""
        return "Free cancellation up to 48 hours before check-in"

    @staticmethod
    def from_dict(data):
        """Create a corporate reservation from dictionary data."""
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
