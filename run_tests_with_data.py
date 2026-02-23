#!/usr/bin/env python3
"""
Script para ejecutar pruebas con diferentes conjuntos de datos JSON.
Copia los archivos de prueba a los archivos principales y ejecuta el sistema.
"""

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
    """Respalda los archivos originales si existen"""
    files = ["hotels.json", "customers.json", "reservations.json"]
    backed_up = []

    for filename in files:
        if os.path.exists(filename):
            backup_name = filename + BACKUP_SUFFIX
            shutil.copy(filename, backup_name)
            backed_up.append(filename)

    if backed_up:
        print(f"✓ Backup creado para: {', '.join(backed_up)}")
    return backed_up


def restore_original_files():
    """Restaura los archivos originales del backup"""
    files = ["hotels.json", "customers.json", "reservations.json"]
    restored = []

    for filename in files:
        backup_name = filename + BACKUP_SUFFIX
        if os.path.exists(backup_name):
            shutil.move(backup_name, filename)
            restored.append(filename)

    if restored:
        print(f"✓ Archivos restaurados: {', '.join(restored)}")


def load_test_data(test_name):
    """Carga el conjunto de prueba especificado"""
    if test_name not in TEST_SETS:
        print(f"✗ Conjunto de prueba '{test_name}' no existe")
        print(f"Opciones disponibles: {', '.join(TEST_SETS.keys())}")
        return False

    test_set = TEST_SETS[test_name]
    print(f"\n{'='*70}")
    print(f"Cargando conjunto de prueba: {test_name.upper()}")
    print(f"{'='*70}\n")

    # Respaldar originales
    backup_original_files()

    # Copiar archivos de prueba
    try:
        for target_file, source_file in test_set.items():
            source_path = os.path.join(TEST_DATA_DIR, source_file)

            if not os.path.exists(source_path):
                print(f"✗ Archivo de prueba no encontrado: {source_path}")
                restore_original_files()
                return False

            shutil.copy(source_path, f"{target_file}.json")
            print(f"✓ Copiado: {source_file} → {target_file}.json")

        return True
    except Exception as e:
        print(f"✗ Error al copiar archivos: {e}")
        restore_original_files()
        return False


def display_statistics():
    """Muestra estadísticas de los datos cargados"""
    import json

    try:
        with open("hotels.json") as f:
            hotels = json.load(f)
        with open("customers.json") as f:
            customers = json.load(f)
        with open("reservations.json") as f:
            reservations = json.load(f)

        print("\n📊 ESTADÍSTICAS DE DATOS CARGADOS:")
        print(f"   • Hoteles:       {len(hotels)}")
        print(f"   • Clientes:      {len(customers)}")
        print(f"   • Reservaciones: {len(reservations)}")

        if hotels:
            total_rooms = sum(len(h.get("rooms", [])) for h in hotels)
            occupied = sum(
                sum(1 for r in h.get("rooms", []) if r.get("is_occupied"))
                for h in hotels
            )
            print(f"   • Habitaciones:  {total_rooms} total, {occupied} ocupadas")

        print()
    except Exception as e:
        print(f"Error al leer estadísticas: {e}")


def main():
    if len(sys.argv) < 2:
        print("\nUSO: python run_tests_with_data.py <test_set>")
        print("\nConjuntos disponibles:")
        for test_name, test_set in TEST_SETS.items():
            print(f"  • {test_name}")
        print("\nEjemplo:")
        print("  python run_tests_with_data.py basic")
        print("  python run_tests_with_data.py negative")
        sys.exit(1)

    test_name = sys.argv[1]

    if load_test_data(test_name):
        display_statistics()
        print("✓ Datos cargados correctamente")
        print("✓ Ahora puedes ejecutar: python main.py")
        print()
    else:
        print("✗ Error al cargar datos")
        sys.exit(1)


if __name__ == "__main__":
    main()

