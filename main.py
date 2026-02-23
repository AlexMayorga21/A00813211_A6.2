from models.hotel import Hotel
from models.customer import Customer
from models.room import SingleRoom, DoubleRoom, Suite
from models.reservation import StandardReservation, VIPReservation, CorporateReservation
from utils import DataManager


class HotelManagementSystem:
    def __init__(self):
        self.data_manager = DataManager()
        self.hotels = self.data_manager.load_hotels()
        self.customers = self.data_manager.load_customers()
        self.reservations = self.data_manager.load_reservations()

    def save_all(self):
        """Save all data to JSON files"""
        self.data_manager.save_hotels(self.hotels)
        self.data_manager.save_customers(self.customers)
        self.data_manager.save_reservations(self.reservations)

    def load_all(self):
        """Load all data from JSON files"""
        self.hotels = self.data_manager.load_hotels()
        self.customers = self.data_manager.load_customers()
        self.reservations = self.data_manager.load_reservations()

    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "="*50)
            print("HOTEL MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Manage Hotels")
            print("2. Manage Customers")
            print("3. Manage Reservations")
            print("4. Exit")
            print("="*50)

            choice = input("Select option (1-4): ").strip()

            if choice == "1":
                self.hotel_menu()
            elif choice == "2":
                self.customer_menu()
            elif choice == "3":
                self.reservation_menu()
            elif choice == "4":
                print("Thank you for using Hotel Management System!")
                break
            else:
                print("Invalid option!")

    def hotel_menu(self):
        """Hotel management submenu"""
        while True:
            print("\n--- HOTEL MENU ---")
            print("1. Create Hotel")
            print("2. View Hotels")
            print("3. Update Hotel")
            print("4. Delete Hotel")
            print("5. Add Room to Hotel")
            print("6. Search Hotels")
            print("7. Back")

            choice = input("Select option (1-7): ").strip()

            if choice == "1":
                self.create_hotel()
            elif choice == "2":
                self.view_hotels()
            elif choice == "3":
                self.update_hotel()
            elif choice == "4":
                self.delete_hotel()
            elif choice == "5":
                self.add_room_to_hotel()
            elif choice == "6":
                self.search_hotels()
            elif choice == "7":
                break
            else:
                print("Invalid option!")

    def customer_menu(self):
        """Customer management submenu"""
        while True:
            print("\n--- CUSTOMER MENU ---")
            print("1. Create Customer")
            print("2. View Customers")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. Back")

            choice = input("Select option (1-5): ").strip()

            if choice == "1":
                self.create_customer()
            elif choice == "2":
                self.view_customers()
            elif choice == "3":
                self.update_customer()
            elif choice == "4":
                self.delete_customer()
            elif choice == "5":
                break
            else:
                print("Invalid option!")

    def reservation_menu(self):
        """Reservation management submenu"""
        while True:
            print("\n--- RESERVATION MENU ---")
            print("1. Create Reservation")
            print("2. View Reservations")
            print("3. Update Reservation")
            print("4. Cancel Reservation")
            print("5. Back")

            choice = input("Select option (1-5): ").strip()

            if choice == "1":
                self.create_reservation()
            elif choice == "2":
                self.view_reservations()
            elif choice == "3":
                self.update_reservation()
            elif choice == "4":
                self.cancel_reservation()
            elif choice == "5":
                break
            else:
                print("Invalid option!")

    # ============ HOTEL CRUD ============
    def create_hotel(self):
        print("\n--- CREATE HOTEL ---")
        hotel_id = input("Hotel ID: ").strip()
        if not hotel_id:
            print("Invalid Hotel ID!")
            return
        if any(h.hotel_id == hotel_id for h in self.hotels):
            print("Hotel ID already exists!")
            return
        name = input("Hotel Name: ").strip()
        address = input("Address: ").strip()
        description = input("Description: ").strip()
        hotel = Hotel(hotel_id, name, address, description)
        self.hotels.append(hotel)
        self.save_all()
        print("Hotel created successfully!")

    def view_hotels(self):
        if not self.hotels:
            print("\nNo hotels found.")
            return
        print("\n--- ALL HOTELS ---")
        for hotel in self.hotels:
            print(f"\n{hotel}")
            print(f"   Rooms: {len(hotel.rooms)}")

    def update_hotel(self):
        if not self.hotels:
            print("\nNo hotels to update.")
            return
        hotel_id = input("\nEnter Hotel ID to update: ").strip()
        hotel = next((h for h in self.hotels if h.hotel_id == hotel_id), None)
        if not hotel:
            print("Hotel not found!")
            return
        print(f"\nCurrent: {hotel}")
        name = input(f"New name [{hotel.name}]: ").strip() or hotel.name
        address = input(f"New address [{hotel.address}]: ").strip() or hotel.address
        description = input(f"New description [{hotel.description}]: ").strip() or hotel.description
        hotel.name = name
        hotel.address = address
        hotel.description = description
        self.save_all()
        print("Hotel updated successfully!")

    def delete_hotel(self):
        if not self.hotels:
            print("\nNo hotels to delete.")
            return
        hotel_id = input("\nEnter Hotel ID to delete: ").strip()
        hotel = next((h for h in self.hotels if h.hotel_id == hotel_id), None)
        if not hotel:
            print("Hotel not found!")
            return
        confirm = input(f"Delete '{hotel.name}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.hotels.remove(hotel)
            self.save_all()
            print("Hotel deleted successfully!")

    def add_room_to_hotel(self):
        if not self.hotels:
            print("\nNo hotels available.")
            return
        hotel_id = input("\nEnter Hotel ID: ").strip()
        hotel = next((h for h in self.hotels if h.hotel_id == hotel_id), None)
        if not hotel:
            print("Hotel not found!")
            return
        print("\nRoom Types: 1) Single  2) Double  3) Suite")
        room_type = input("Select room type (1-3): ").strip()
        room_id = input("Room ID: ").strip()
        room_number = input("Room Number: ").strip()
        try:
            floor = int(input("Floor: ").strip())
            price = float(input("Price per night: ").strip())
        except ValueError:
            print("Invalid input!")
            return
        if room_type == "1":
            room = SingleRoom(room_id, room_number, floor, price)
        elif room_type == "2":
            room = DoubleRoom(room_id, room_number, floor, price)
        elif room_type == "3":
            room = Suite(room_id, room_number, floor, price)
        else:
            print("Invalid room type!")
            return
        hotel.add_room(room)
        self.save_all()
        print("Room added successfully!")

    def search_hotels(self):
        if not self.hotels:
            print("\nNo hotels to search.")
            return
        search_term = input("\nEnter hotel name to search: ").strip().lower()
        found = [h for h in self.hotels if search_term in h.name.lower()]
        if not found:
            print("No hotels found.")
            return
        print(f"\n--- SEARCH RESULTS ({len(found)} found) ---")
        for hotel in found:
            print(f"\n{hotel}")

    # ============ CUSTOMER CRUD ============
    def create_customer(self):
        try:
            print("\n--- CREATE CUSTOMER ---")
            customer_id = input("Customer ID: ").strip()
            if not customer_id or any(c.customer_id == customer_id for c in self.customers):
                print("Invalid or duplicate Customer ID!")
                return
            first_name = input("First Name: ").strip()
            if not first_name:
                print("First name cannot be empty!")
                return
            last_name = input("Last Name: ").strip()
            if not last_name:
                print("Last name cannot be empty!")
                return
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            customer = Customer(customer_id, first_name, last_name, email, phone)
            self.customers.append(customer)
            self.save_all()
            print("Customer created successfully!")
        except Exception as e:
            print(f"[ERROR] {e}")

    def view_customers(self):
        if not self.customers:
            print("\nNo customers found.")
            return
        print("\n--- ALL CUSTOMERS ---")
        for customer in self.customers:
            print(f"\n{customer}")

    def update_customer(self):
        if not self.customers:
            print("\nNo customers to update.")
            return
        customer_id = input("\nEnter Customer ID to update: ").strip()
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            print("Customer not found!")
            return
        print(f"\nCurrent: {customer}")
        # Fixed attribute names
        first_name = (
            input(f"New first name [{customer.first_name}]: ").strip()
            or customer.first_name
        )
        last_name = (
            input(f"New last name [{customer.last_name}]: ").strip()
            or customer.last_name
        )
        email = (
            input(f"New email [{customer.email}]: ").strip()
            or customer.email
        )
        phone = (
            input(f"New phone [{customer.phone}]: ").strip()
            or customer.phone
        )

        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.phone = phone
        self.save_all()
        print("Customer updated successfully!")

    def delete_customer(self):
        if not self.customers:
            print("\nNo customers to delete.")
            return
        customer_id = input("\nEnter Customer ID to delete: ").strip()
        customer = next(
            (c for c in self.customers if c.customer_id == customer_id), None
        )
        if not customer:
            print("Customer not found!")
            return
        confirm = (
            input(
                f"Delete '{customer.first_name} {customer.last_name}'? "
                "(yes/no): "
            )
            .strip()
            .lower()
        )
        if confirm == "yes":
            self.customers.remove(customer)
            self.save_all()
            print("Customer deleted successfully!")

    # ============ RESERVATION CRUD ============
    def create_reservation(self):
        if not self.hotels or not self.customers:
            print("\nNeed at least one hotel and customer!")
            return
        print("\n--- CREATE RESERVATION ---")
        print("\nAvailable customers:")
        for c in self.customers:
            print(f"  {c.customer_id}: {c.first_name} {c.last_name}")
        customer_id = input("Customer ID: ").strip()
        if not any(c.customer_id == customer_id for c in self.customers):
            print("Customer not found!")
            return
        print("\nAvailable hotels:")
        for h in self.hotels:
            print(f"  {h.hotel_id}: {h.name}")
        hotel_id = input("Hotel ID: ").strip()
        hotel = next(
            (h for h in self.hotels if h.hotel_id == hotel_id), None
        )
        if not hotel:
            print("Hotel not found!")
            return
        available_rooms = hotel.get_available_rooms()
        if not available_rooms:
            print("No available rooms!")
            return
        print("\nAvailable rooms:")
        for r in available_rooms:
            print(
                f"  {r.room_id}: {r.room_number} - ${r.price}/night "
                f"(Capacity: {r.capacity})"
            )
        room_id = input("Room ID: ").strip()
        room = next(
            (r for r in available_rooms if r.room_id == room_id), None
        )
        if not room:
            print("Room not found!")
            return
        check_in = input("Check-in date (YYYY-MM-DD): ").strip()
        check_out = input("Check-out date (YYYY-MM-DD): ").strip()

        # Add number_of_guests input
        try:
            number_of_guests = int(
                input(f"Number of guests (max {room.capacity}): ").strip()
            )
            if number_of_guests < 1 or number_of_guests > room.capacity:
                print(
                    f"Invalid number of guests! Must be 1-{room.capacity}"
                )
                return
        except ValueError:
            print("Invalid input!")
            return

        print("\nReservation types: 1) Standard  2) VIP  3) Corporate")
        res_type = input("Select type (1-3): ").strip()
        reservation_id = f"RES{len(self.reservations) + 1:03d}"

        # Pass number_of_guests to all constructors
        if res_type == "1":
            reservation = StandardReservation(
                reservation_id,
                customer_id,
                hotel_id,
                room_id,
                check_in,
                check_out,
                number_of_guests
            )
        elif res_type == "2":
            reservation = VIPReservation(
                reservation_id,
                customer_id,
                hotel_id,
                room_id,
                check_in,
                check_out,
                number_of_guests
            )
        elif res_type == "3":
            reservation = CorporateReservation(
                reservation_id,
                customer_id,
                hotel_id,
                room_id,
                check_in,
                check_out,
                number_of_guests
            )
        else:
            print("Invalid type!")
            return

        room.is_occupied = True
        self.reservations.append(reservation)
        self.save_all()
        print("Reservation created successfully!")

    def view_reservations(self):
        if not self.reservations:
            print("\nNo reservations found.")
            return
        print("\n--- ALL RESERVATIONS ---")
        for reservation in self.reservations:
            print(f"\n{reservation}")

    def update_reservation(self):
        if not self.reservations:
            print("\nNo reservations to update.")
            return
        reservation_id = input("\nEnter Reservation ID: ").strip()
        reservation = next(
            (r for r in self.reservations if r.reservation_id == reservation_id),
            None
        )
        if not reservation:
            print("Reservation not found!")
            return
        print(f"\nCurrent: {reservation}")
        # Fixed attribute names
        check_in = (
            input(f"New check-in [{reservation.check_in}]: ").strip()
            or reservation.check_in
        )
        check_out = (
            input(f"New check-out [{reservation.check_out}]: ").strip()
            or reservation.check_out
        )

        reservation.check_in = check_in
        reservation.check_out = check_out
        self.save_all()
        print("Reservation updated successfully!")

    def cancel_reservation(self):
        if not self.reservations:
            print("\nNo reservations to cancel.")
            return
        reservation_id = input("\nEnter Reservation ID: ").strip()
        reservation = next(
            (
                r for r in self.reservations
                if r.reservation_id == reservation_id
            ),
            None
        )
        if not reservation:
            print("Reservation not found!")
            return
        for hotel in self.hotels:
            if hotel.hotel_id == reservation.hotel_id:
                for room in hotel.rooms:
                    if room.room_id == reservation.room_id:
                        room.is_occupied = False
        confirm = input(f"Cancel {reservation_id}? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.reservations.remove(reservation)
            self.save_all()
            print("Reservation cancelled!")


if __name__ == "__main__":
    system = HotelManagementSystem()
    system.run()
