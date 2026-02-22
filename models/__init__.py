from models.hotel import Hotel
from models.customer import Customer
from models.room import Room, SingleRoom, DoubleRoom, Suite
from models.reservation import (Reservation,
    StandardReservation,
    VIPReservation,
    CorporateReservation
)

__all__ = [
    'Hotel',
    'Customer',
    'Room', 'SingleRoom', 'DoubleRoom', 'Suite',
    'Reservation', 'StandardReservation', 'VIPReservation', 'CorporateReservation'
]
