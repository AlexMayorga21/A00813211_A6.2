"""
Unit tests for the Hotel Management System.

This module contains comprehensive unit tests for all components of the hotel
management system including customers, rooms, hotels, reservations, and the
main system itself.
"""
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from main import HotelManagementSystem
from models import Hotel, Customer, SingleRoom, DoubleRoom, Suite
from models import StandardReservation, VIPReservation, CorporateReservation


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer model."""

    def setUp(self):
        """Initialize test customer."""
        self.customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")

    def test_customer_initialization(self):
        """Test that customer is initialized with correct attributes."""
        self.assertEqual(self.customer.customer_id, "C1")
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john@email.com")
        self.assertEqual(self.customer.phone, "1234567890")

    def test_customer_str_representation(self):
        """Test string representation of customer."""
        expected = "C1: John Doe (john@email.com, 1234567890)"
        self.assertEqual(str(self.customer), expected)

    def test_customer_to_dict(self):
        """Test customer conversion to dictionary."""
        customer_dict = self.customer.to_dict()
        self.assertEqual(customer_dict["customer_id"], "C1")
        self.assertEqual(customer_dict["first_name"], "John")
        self.assertEqual(customer_dict["last_name"], "Doe")

    def test_customer_from_dict(self):
        """Test customer creation from dictionary."""
        data = {
            "customer_id": "C2",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@email.com",
            "phone": "9876543210"
        }
        customer = Customer.from_dict(data)
        self.assertEqual(customer.customer_id, "C2")
        self.assertEqual(customer.first_name, "Jane")


class TestRooms(unittest.TestCase):
    """Test cases for room models (SingleRoom, DoubleRoom, Suite)."""

    def test_single_room_initialization(self):
        """Test that single room is initialized with correct capacity."""
        room = SingleRoom("R1", "101", 1, 100.0)
        self.assertEqual(room.room_id, "R1")
        self.assertEqual(room.room_number, "101")
        self.assertEqual(room.capacity, 1)
        self.assertEqual(room.price, 100.0)
        self.assertFalse(room.is_occupied)

    def test_double_room_initialization(self):
        """Test that double room is initialized with correct capacity."""
        room = DoubleRoom("R2", "102", 1, 150.0)
        self.assertEqual(room.room_id, "R2")
        self.assertEqual(room.capacity, 2)
        self.assertEqual(room.price, 150.0)

    def test_suite_initialization(self):
        """Test that suite is initialized with correct capacity."""
        room = Suite("R3", "103", 2, 250.0)
        self.assertEqual(room.room_id, "R3")
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.price, 250.0)

    def test_room_to_dict(self):
        """Test room conversion to dictionary."""
        room = SingleRoom("R1", "101", 1, 100.0)
        room_dict = room.to_dict()
        self.assertEqual(room_dict["room_id"], "R1")
        self.assertEqual(room_dict["is_occupied"], False)

    def test_room_from_dict(self):
        """Test room creation from dictionary."""
        data = {
            "room_id": "R1",
            "room_number": "101",
            "capacity": 1,
            "price": 100.0,
            "is_occupied": False,
            "room_type": "SingleRoom",
            "floor": 1
        }
        room = SingleRoom.from_dict(data)
        self.assertEqual(room.room_id, "R1")
        self.assertEqual(room.room_number, "101")

    def test_room_occupied_status(self):
        """Test room occupied status can be changed."""
        room = SingleRoom("R1", "101", 1, 100.0)
        self.assertFalse(room.is_occupied)
        room.is_occupied = True
        self.assertTrue(room.is_occupied)


class TestHotel(unittest.TestCase):
    """Test cases for the Hotel model."""

    def setUp(self):
        """Initialize test hotel."""
        self.hotel = Hotel("H1", "Grand Hotel", "123 Main St", "Luxury hotel")

    def test_hotel_initialization(self):
        """Test hotel initialization with correct attributes."""
        self.assertEqual(self.hotel.hotel_id, "H1")
        self.assertEqual(self.hotel.name, "Grand Hotel")
        self.assertEqual(self.hotel.address, "123 Main St")
        self.assertEqual(self.hotel.description, "Luxury hotel")
        self.assertEqual(len(self.hotel.rooms), 0)

    def test_add_room(self):
        """Test adding a single room to hotel."""
        room = SingleRoom("R1", "101", 1, 100.0)
        self.hotel.add_room(room)
        self.assertEqual(len(self.hotel.rooms), 1)
        self.assertEqual(self.hotel.rooms[0].room_id, "R1")

    def test_add_multiple_rooms(self):
        """Test adding multiple rooms to hotel."""
        room1 = SingleRoom("R1", "101", 1, 100.0)
        room2 = DoubleRoom("R2", "102", 1, 150.0)
        self.hotel.add_room(room1)
        self.hotel.add_room(room2)
        self.assertEqual(len(self.hotel.rooms), 2)

    def test_get_available_rooms_all_available(self):
        """Test retrieving available rooms when all are available."""
        room1 = SingleRoom("R1", "101", 1, 100.0)
        room2 = DoubleRoom("R2", "102", 1, 150.0)
        self.hotel.add_room(room1)
        self.hotel.add_room(room2)
        available = self.hotel.get_available_rooms()
        self.assertEqual(len(available), 2)

    def test_get_available_rooms_some_occupied(self):
        """Test retrieving available rooms when some are occupied."""
        room1 = SingleRoom("R1", "101", 1, 100.0)
        room2 = DoubleRoom("R2", "102", 1, 150.0)
        self.hotel.add_room(room1)
        self.hotel.add_room(room2)
        room1.is_occupied = True
        available = self.hotel.get_available_rooms()
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0].room_id, "R2")

    def test_get_available_rooms_none_available(self):
        """Test retrieving available rooms when none are available."""
        room1 = SingleRoom("R1", "101", 1, 100.0)
        self.hotel.add_room(room1)
        room1.is_occupied = True
        available = self.hotel.get_available_rooms()
        self.assertEqual(len(available), 0)

    def test_hotel_to_dict(self):
        """Test hotel conversion to dictionary."""
        room = SingleRoom("R1", "101", 1, 100.0)
        self.hotel.add_room(room)
        hotel_dict = self.hotel.to_dict()
        self.assertEqual(hotel_dict["hotel_id"], "H1")
        self.assertEqual(len(hotel_dict["rooms"]), 1)

    def test_hotel_from_dict(self):
        """Test hotel creation from dictionary."""
        data = {
            "hotel_id": "H1",
            "name": "Grand Hotel",
            "address": "123 Main St",
            "description": "Luxury hotel",
            "rooms": []
        }
        hotel = Hotel.from_dict(data)
        self.assertEqual(hotel.hotel_id, "H1")
        self.assertEqual(hotel.name, "Grand Hotel")

    def test_hotel_str_representation(self):
        """Test string representation of hotel."""
        expected = "H1: Grand Hotel (123 Main St) - 0 rooms"
        self.assertEqual(str(self.hotel), expected)


class TestReservations(unittest.TestCase):
    """Test cases for reservation models."""

    def test_standard_reservation_initialization(self):
        """Test standard reservation initialization."""
        res = StandardReservation("RES001", "C1", "H1", "R1", "2024-01-10", "2024-01-15", 2)
        self.assertEqual(res.reservation_id, "RES001")
        self.assertEqual(res.customer_id, "C1")
        self.assertEqual(res.hotel_id, "H1")
        self.assertEqual(res.room_id, "R1")
        self.assertEqual(res.check_in, "2024-01-10")
        self.assertEqual(res.check_out, "2024-01-15")
        self.assertEqual(res.number_of_guests, 2)
        self.assertEqual(res.reservation_type, "Standard")

    def test_vip_reservation_initialization(self):
        """Test VIP reservation initialization."""
        res = VIPReservation("RES002", "C2", "H1", "R2", "2024-02-10", "2024-02-15", 3)
        self.assertEqual(res.reservation_type, "VIP")
        self.assertEqual(res.number_of_guests, 3)

    def test_corporate_reservation_initialization(self):
        """Test corporate reservation initialization."""
        res = CorporateReservation("RES003", "C3", "H1", "R3", "2024-03-10", "2024-03-15", 5)
        self.assertEqual(res.reservation_type, "Corporate")
        self.assertEqual(res.number_of_guests, 5)

    def test_reservation_to_dict(self):
        """Test reservation conversion to dictionary."""
        res = StandardReservation("RES001", "C1", "H1", "R1", "2024-01-10", "2024-01-15", 2)
        res_dict = res.to_dict()
        self.assertEqual(res_dict["reservation_id"], "RES001")
        self.assertEqual(res_dict["customer_id"], "C1")

    def test_reservation_from_dict_standard(self):
        """Test standard reservation creation from dictionary."""
        data = {
            "reservation_id": "RES001",
            "customer_id": "C1",
            "hotel_id": "H1",
            "room_id": "R1",
            "check_in": "2024-01-10",
            "check_out": "2024-01-15",
            "number_of_guests": 2,
            "reservation_type": "Standard"
        }
        res = StandardReservation.from_dict(data)
        self.assertEqual(res.reservation_id, "RES001")
        self.assertEqual(res.reservation_type, "Standard")

    def test_reservation_str_representation(self):
        """Test string representation of reservation."""
        res = StandardReservation("RES001", "C1", "H1", "R1", "2024-01-10", "2024-01-15", 2)
        self.assertIn("RES001", str(res))
        self.assertIn("C1", str(res))


class TestHotelManagementSystemHotels(unittest.TestCase):
    """Test cases for hotel-related operations in HotelManagementSystem."""

    def setUp(self):
        """Initialize test hotel management system."""
        self.system = HotelManagementSystem()
        self.system.hotels = []
        self.system.customers = []
        self.system.reservations = []

    @patch('builtins.input', side_effect=['H1', 'Grand Hotel', '123 Main St', 'Luxury'])
    def test_create_hotel_input(self, mock_input):
        """Test creating hotel with user input."""
        # pylint: disable=unused-argument
        self.system.create_hotel()
        self.assertEqual(len(self.system.hotels), 1)
        self.assertEqual(self.system.hotels[0].name, 'Grand Hotel')

    @patch('builtins.input', side_effect=['H1', 'H1'])
    def test_create_duplicate_hotel(self, mock_input):
        """Test that duplicate hotel IDs are rejected."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        self.system.hotels.append(hotel)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_hotel()
            self.assertIn("Hotel ID already exists!", fake_out.getvalue())

    @patch('builtins.input', side_effect=['', 'Hotel', 'Address', 'Desc'])
    def test_create_hotel_empty_id(self, mock_input):
        """Test that empty hotel IDs are rejected."""
        # pylint: disable=unused-argument
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_hotel()
            self.assertIn("Invalid", fake_out.getvalue())

    @patch('builtins.input', side_effect=['H1', '2', '101', '1', '100', '1200'])
    def test_add_room_to_hotel(self, mock_input):
        """Test adding a room to a hotel."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        self.system.hotels.append(hotel)
        self.system.add_room_to_hotel()
        self.assertEqual(len(hotel.rooms), 1)

    @patch('builtins.input', side_effect=['H1'])
    def test_add_room_hotel_not_found(self, mock_input):
        """Test adding a room when hotel is not found."""
        # pylint: disable=unused-argument
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.add_room_to_hotel()
            self.assertIn("No hotels available", fake_out.getvalue())

    @patch('builtins.input', side_effect=['H1', 'yes'])
    def test_delete_hotel(self, mock_input):
        """Test deleting a hotel."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        self.system.hotels.append(hotel)
        self.system.delete_hotel()
        self.assertEqual(len(self.system.hotels), 0)

    @patch('builtins.input', side_effect=['Grand'])
    def test_search_hotels(self, mock_input):
        """Test searching for hotels by name."""
        # pylint: disable=unused-argument
        hotel1 = Hotel("H1", "Grand Hotel", "Address 1", "Desc")
        hotel2 = Hotel("H2", "Small Inn", "Address 2", "Desc")
        self.system.hotels.extend([hotel1, hotel2])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.search_hotels()
            self.assertIn("Grand Hotel", fake_out.getvalue())

    def test_view_hotels_empty(self):
        """Test viewing hotels when none exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_hotels()
            self.assertIn("No hotels", fake_out.getvalue())

    def test_view_hotels_with_data(self):
        """Test viewing hotels with data."""
        hotel = Hotel("H1", "Grand Hotel", "Address", "Desc")
        self.system.hotels.append(hotel)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_hotels()
            self.assertIn("Grand Hotel", fake_out.getvalue())


class TestHotelManagementSystemCustomers(unittest.TestCase):
    """Test cases for customer operations in HotelManagementSystem."""

    def setUp(self):
        """Initialize test hotel management system."""
        self.system = HotelManagementSystem()
        self.system.hotels = []
        self.system.customers = []
        self.system.reservations = []

    @patch('builtins.input', side_effect=['C1', 'John', 'Doe', 'john@email.com', '1234567890'])
    def test_create_customer_input(self, mock_input):
        """Test creating customer with user input."""
        # pylint: disable=unused-argument
        self.system.create_customer()
        self.assertEqual(len(self.system.customers), 1)
        self.assertEqual(self.system.customers[0].first_name, 'John')

    @patch('builtins.input', side_effect=['C1', 'C1'])
    def test_create_duplicate_customer(self, mock_input):
        """Test that duplicate customer IDs are rejected."""
        # pylint: disable=unused-argument
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.customers.append(customer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_customer()
            self.assertIn("Invalid", fake_out.getvalue())

    @patch('builtins.input', side_effect=['C1', 'Jane', 'Smith', 'jane@email.com', '9876543210'])
    def test_update_customer(self, mock_input):
        """Test updating customer information."""
        # pylint: disable=unused-argument
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.customers.append(customer)
        self.system.update_customer()
        self.assertEqual(self.system.customers[0].first_name, 'Jane')

    @patch('builtins.input', side_effect=['C1'])
    def test_update_nonexistent_customer(self, mock_input):
        """Test updating a customer that doesn't exist."""
        # pylint: disable=unused-argument
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.update_customer()
            self.assertIn("No customers", fake_out.getvalue())

    @patch('builtins.input', side_effect=['C1', 'yes'])
    def test_delete_customer(self, mock_input):
        """Test deleting a customer."""
        # pylint: disable=unused-argument
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.customers.append(customer)
        self.system.delete_customer()
        self.assertEqual(len(self.system.customers), 0)

    @patch('builtins.input', side_effect=['C1', 'no'])
    def test_delete_customer_cancel(self, mock_input):
        """Test cancelling customer deletion."""
        # pylint: disable=unused-argument
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.customers.append(customer)
        self.system.delete_customer()
        self.assertEqual(len(self.system.customers), 1)

    def test_delete_customer_no_customers(self):
        """Test deleting customer when no customers exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.delete_customer()
            self.assertIn("No customers", fake_out.getvalue())

    def test_view_customers_empty(self):
        """Test viewing customers when none exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_customers()
            self.assertIn("No customers", fake_out.getvalue())

    def test_view_customers_with_data(self):
        """Test viewing customers with data."""
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.customers.append(customer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_customers()
            self.assertIn("John", fake_out.getvalue())


class TestHotelManagementSystemReservations(unittest.TestCase):
    """Test cases for reservation operations in HotelManagementSystem."""

    def setUp(self):
        """Initialize test hotel management system."""
        self.system = HotelManagementSystem()
        self.system.hotels = []
        self.system.customers = []
        self.system.reservations = []

    @patch('builtins.input', side_effect=['C1', 'H1', 'R1', '2024-01-10', '2024-01-15', '1', '1'])
    def test_create_standard_reservation(self, mock_input):
        """Test creating a standard reservation."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        room = SingleRoom("R1", "101", 1, 100.0)
        hotel.add_room(room)
        customer = Customer(
            "C1",
            "John",
            "Doe",
            "john@email.com",
            "1234567890"
        )
        self.system.hotels.append(hotel)
        self.system.customers.append(customer)
        self.system.create_reservation()
        self.assertEqual(len(self.system.reservations), 1)
        self.assertTrue(room.is_occupied)

    def test_create_reservation_no_hotels(self):
        """Test creating reservation when no hotels exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_reservation()
            self.assertIn("Need", fake_out.getvalue())

    @patch(
        'builtins.input',
        side_effect=[
            'C1', 'H1', 'R1', '2024-01-10', '2024-01-15', 'invalid', '1'
        ]
    )
    def test_create_reservation_invalid_guests(self, mock_input):
        """Test creating reservation with invalid guest count."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        room = SingleRoom("R1", "101", 1, 100.0)
        hotel.add_room(room)
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.hotels.append(hotel)
        self.system.customers.append(customer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_reservation()
            self.assertIn("Invalid", fake_out.getvalue())

    @patch('builtins.input', side_effect=['INVALID'])
    def test_create_reservation_invalid_customer(self, mock_input):
        """Test creating reservation with invalid customer."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.hotels.append(hotel)
        self.system.customers.append(customer)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.create_reservation()
            self.assertIn("not found", fake_out.getvalue())

    @patch('builtins.input', side_effect=['RES001', 'yes'])
    def test_cancel_reservation(self, mock_input):
        """Test cancelling a reservation."""
        # pylint: disable=unused-argument
        res = StandardReservation("RES001", "C1", "H1", "R1", "2024-01-10", "2024-01-15", 2)
        self.system.reservations.append(res)
        self.system.cancel_reservation()
        self.assertEqual(len(self.system.reservations), 0)

    @patch('builtins.input', side_effect=['RES001'])
    def test_cancel_nonexistent_reservation(self, mock_input):
        """Test cancelling a non-existent reservation."""
        # pylint: disable=unused-argument
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.cancel_reservation()
            self.assertIn("No reservations to cancel", fake_out.getvalue())

    def test_cancel_reservation_no_reservations(self):
        """Test cancelling reservation when no reservations exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.cancel_reservation()
            self.assertIn("No reservations", fake_out.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data='{[], [], []}')
    def test_load_all(self, mock_file):
        """Test loading all data from files."""
        # pylint: disable=unused-argument
        self.system.load_all()
        self.assertEqual(len(self.system.hotels), 0)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_all(self, mock_file):
        """Test saving all data to files."""
        # pylint: disable=unused-argument
        hotel = Hotel("H1", "Hotel A", "Address", "Desc")
        customer = Customer("C1", "John", "Doe", "john@email.com", "1234567890")
        self.system.hotels.append(hotel)
        self.system.customers.append(customer)
        self.system.save_all()
        mock_file.assert_called()

    def test_view_reservations_empty(self):
        """Test viewing reservations when none exist."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_reservations()
            self.assertIn("No reservations", fake_out.getvalue())

    def test_view_reservations_with_data(self):
        """Test viewing reservations with data."""
        res = StandardReservation("RES001", "C1", "H1", "R1", "2024-01-10", "2024-01-15", 2)
        self.system.reservations.append(res)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.system.view_reservations()
            self.assertIn("RES001", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
