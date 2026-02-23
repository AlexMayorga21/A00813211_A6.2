"""Data manager module for handling JSON data persistence."""
import json
import os
from models import (
    Hotel, SingleRoom, DoubleRoom, Suite,
    Customer,
    StandardReservation, VIPReservation, CorporateReservation
)


class DataManager:
    """Manages data persistence with error handling"""

    def __init__(self):
        self.hotels_file = "hotels.json"
        self.customers_file = "customers.json"
        self.reservations_file = "reservations.json"

    def _safe_load_json(self, filename):
        """Safely load JSON file"""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[ERROR] Corrupted JSON in {filename}. Starting fresh.")
            return []
        except (OSError, IOError):
            print(f"[ERROR] Cannot read {filename}.")
            return []

    def _safe_save_json(self, filename, data):
        """Safely save JSON file"""
        try:
            with open(filename, mode='w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, default=str)
        except (OSError, IOError) as e:
            print(f"[ERROR] Cannot save to {filename}: {e}")

    def load_hotels(self):
        """Load hotels from JSON file"""
        data = self._safe_load_json(self.hotels_file)
        hotels = []
        for hotel_data in data:
            try:
                hotel = Hotel(
                    hotel_data["hotel_id"],
                    hotel_data["name"],
                    hotel_data["address"],
                    hotel_data["description"]
                )
                for room_data in hotel_data.get("rooms", []):
                    room_type = room_data["type"]
                    if room_type == "single":
                        room = SingleRoom(
                            room_data["room_id"],
                            room_data["room_number"],
                            room_data["floor"],
                            room_data["price"]
                        )
                    elif room_type == "double":
                        room = DoubleRoom(
                            room_data["room_id"],
                            room_data["room_number"],
                            room_data["floor"],
                            room_data["price"]
                        )
                    else:
                        room = Suite(
                            room_data["room_id"],
                            room_data["room_number"],
                            room_data["floor"],
                            room_data["price"]
                        )
                    room.is_occupied = room_data.get("is_occupied", False)
                    hotel.rooms.append(room)
                hotels.append(hotel)
            except (KeyError, ValueError) as e:
                print(f"[WARNING] Skipping invalid hotel: {e}")
                continue
        return hotels

    def load_customers(self):
        """Load customers from JSON file"""
        data = self._safe_load_json(self.customers_file)
        customers = []
        for customer_data in data:
            try:
                # customer_id, first_name, last_name, email, phone
                customer = Customer(
                    customer_data["customer_id"],
                    customer_data["first_name"],
                    customer_data["last_name"],
                    customer_data["email"],
                    customer_data["phone"]
                )
                customers.append(customer)
            except (KeyError, ValueError) as e:
                print(f"[WARNING] Skipping invalid customer: {e}")
                continue
        return customers

    def load_reservations(self):
        """Load reservations from JSON file"""
        data = self._safe_load_json(self.reservations_file)
        reservations = []
        for res_data in data:
            try:
                res_type = res_data["type"]
                if res_type == "standard":
                    res_class = StandardReservation
                elif res_type == "vip":
                    res_class = VIPReservation
                else:
                    res_class = CorporateReservation
                reservation = res_class(
                    res_data["reservation_id"],
                    res_data["customer_id"],
                    res_data["hotel_id"],
                    res_data["room_id"],
                    res_data["check_in_date"],
                    res_data["check_out_date"],
                    res_data.get("number_of_guests", 1)
                )
                reservations.append(reservation)
            except (KeyError, ValueError) as e:
                print(f"[WARNING] Skipping invalid reservation: {e}")
                continue
        return reservations

    def save_hotels(self, hotels):
        """Save hotels to JSON file"""
        data = [hotel.to_dict() for hotel in hotels]
        self._safe_save_json(self.hotels_file, data)

    def save_customers(self, customers):
        """Save customers to JSON file"""
        data = [customer.to_dict() for customer in customers]
        self._safe_save_json(self.customers_file, data)

    def save_reservations(self, reservations):
        """Save reservations to JSON file"""
        data = [reservation.to_dict() for reservation in reservations]
        self._safe_save_json(self.reservations_file, data)
