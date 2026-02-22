from models import Hotel, Customer, SingleRoom, DoubleRoom, Suite
from models import StandardReservation, VIPReservation, CorporateReservation
from utils import DataManager
from datetime import datetime


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

    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "="*50)
            print("🏨 HOTEL MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Manage Hotels")
            print("2. Manage Customers")
            print("3. Manage Reservations")
