#!/usr/bin/env python3
"""
Script to run tests with different JSON data sets.
Copies test files to main files and runs the system.
"""

import json
import os
import shutil
import sys


TEST_DATA_DIR = "test_data"
TEST_SETS = {
    "empty": {
        "hotels": "test_empty_hotels.json",
        "customers": "test_empty_customers.json",
        "reservations": "test_empty_reservations.json"
    },
    "basic": {
        "hotels": "test_basic_hotels.json",
        "customers": "test_basic_customers.json",
        "reservations": "test_basic_reservations.json"
    },
    "negative": {
        "hotels": "test_negative_hotels.json",
        "customers": "test_negative_customers.json",
        "reservations": "test_negative_reservations.json"
    },
    "full": {
        "hotels": "test_full_hotels.json",
        "customers": "test_full_customers.json",
        "reservations": "test_full_reservations.json"
    }
}

BACKUP_SUFFIX = ".backup"


def backup_original_files():
    """Backs up original files if they exist"""
    files = ["hotels.json", "customers.json", "reservations.json"]
    backed_up = []

    for filename in files:
        if os.path.exists(filename):
            backup_name = filename + BACKUP_SUFFIX
            shutil.copy(filename, backup_name)
            backed_up.append(filename)

    if backed_up:
        print(f"✓ Backup created for: {', '.join(backed_up)}")
    return backed_up


def restore_original_files():
    """Restores original files from backup"""
    files = ["hotels.json", "customers.json", "reservations.json"]
    restored = []

    for filename in files:
        backup_name = filename + BACKUP_SUFFIX
        if os.path.exists(backup_name):
            shutil.move(backup_name, filename)
            restored.append(filename)

    if restored:
        print(f"✓ Files restored: {', '.join(restored)}")


def load_test_data(test_name):
    """Loads the specified test data set"""
    if test_name not in TEST_SETS:
        print(f"✗ Test set '{test_name}' does not exist")
        print(f"Available options: {', '.join(TEST_SETS.keys())}")
        return False

    test_set = TEST_SETS[test_name]
    print(f"\n{'='*70}")
    print(f"Loading test set: {test_name.upper()}")
    print(f"{'='*70}\n")

    # Backup originals
    backup_original_files()

    # Copy test files
    try:
        for target_file, source_file in test_set.items():
            source_path = os.path.join(TEST_DATA_DIR, source_file)

            if not os.path.exists(source_path):
                print(f"✗ Test file not found: {source_path}")
                restore_original_files()
                return False

            shutil.copy(source_path, f"{target_file}.json")
            print(f"✓ Copied: {source_file} → {target_file}.json")

        return True
    except (OSError, IOError) as e:
        print(f"✗ Error copying files: {e}")
        restore_original_files()
        return False


def display_statistics():
    """Displays statistics of loaded data"""
    try:
        with open("hotels.json", encoding="utf-8") as f:
            hotels = json.load(f)
        with open("customers.json", encoding="utf-8") as f:
            customers = json.load(f)
        with open("reservations.json", encoding="utf-8") as f:
            reservations = json.load(f)

        print("\n📊 LOADED DATA STATISTICS:")
        print(f"   • Hotels:       {len(hotels)}")
        print(f"   • Customers:    {len(customers)}")
        print(f"   • Reservations: {len(reservations)}")

        if hotels:
            total_rooms = sum(len(h.get("rooms", [])) for h in hotels)
            occupied = sum(
                sum(1 for r in h.get("rooms", []) if r.get("is_occupied"))
                for h in hotels
            )
            print(f"   • Rooms:        {total_rooms} total, {occupied} occupied")

        print()
    except (OSError, IOError, json.JSONDecodeError) as e:
        print(f"Error reading statistics: {e}")


def main():
    """Main function to run tests with specified data set."""
    if len(sys.argv) < 2:
        print("\nUSAGE: python run_tests_with_data.py <test_set>")
        print("\nAvailable test sets:")
        for test_name in TEST_SETS:
            print(f"  • {test_name}")
        print("\nExample:")
        print("  python run_tests_with_data.py basic")
        print("  python run_tests_with_data.py negative")
        sys.exit(1)

    test_name = sys.argv[1]

    if load_test_data(test_name):
        display_statistics()
        print("✓ Data loaded successfully")
        print("✓ Now you can run: python main.py")
        print()
    else:
        print("✗ Error loading data")
        sys.exit(1)


if __name__ == "__main__":
    main()
