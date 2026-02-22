import json
from pathlib import Path
from models.hotel import Hotel
from models.customer import Customer
from models.reservation import StandardReservation, VIPReservation, CorporateReservation


class DataManager:
    def __init__(self, data_directory="data"):
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(exist_ok=True)

        self.hotels_file = self.data_dir / "hotels.json"
        self.customers_file = self.data_dir / "customers.json"
        self.reservations_file = self.data_dir / "reservations.json"

        self._initialize_files()

    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        if not self.hotels_file.exists():
            with open(self.hotels_file, 'w') as f:
                json.dump({"hotels": []}, f, indent=2)

        if not self.customers_file.exists():
            with open(self.customers_file, 'w') as f:
                json.dump({"customers": []}, f, indent=2)
