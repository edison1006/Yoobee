
from __future__ import annotations
from typing import Optional
from services import CarRentalService, ValidationError
from utils import input_int, input_float, input_date


def print_header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def list_vehicles(service: CarRentalService, only_available: bool = False):
    items = service.list_vehicles(only_available=only_available)
    if not items:
        print("No vehicles found.")
        return
    for (vid, brand, model, year, rate, vtype, avail) in items:
        print(f"[{vid}] {brand} {model} ({year}) - ${rate:.2f}/day - {vtype} - {'Available' if avail else 'Rented'}")


def list_customers(service: CarRentalService):
    items = service.list_customers()
    if not items:
        print("No customers found.")
        return
    for (cid, name, email, phone) in items:
        print(f"[{cid}] {name} | {email} | {phone}")


def add_vehicle(service: CarRentalService):
    print_header("Add Vehicle")
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    year = input_int("Year (e.g., 2022): ")
    rate = input_float("Daily rate (e.g., 49.99): ")
    print("Type options: Economy, SUV, Truck")
    vtype = input("Vehicle type: ").strip().title()
    try:
        vid = service.add_vehicle(brand, model, year, rate, vtype)
        print(f"Vehicle added with id {vid}.")
    except ValidationError as e:
        print(f"Error: {e}")


def add_customer(service: CarRentalService):
    print_header("Add Customer")
    name = input("Full name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    try:
        cid = service.add_customer(name, email, phone)
        print(f"Customer added with id {cid}.")
    except ValidationError as e:
        print(f"Error: {e}")


def create_rental(service: CarRentalService):
    print_header("Create Rental")
    list_customers(service)
    customer_id = input_int("Customer id: ")
    list_vehicles(service, only_available=True)
    vehicle_id = input_int("Vehicle id: ")
    start = input_date("Start date (YYYY-MM-DD): ")
    end = input_date("End date   (YYYY-MM-DD): ")
    try:
        rid = service.create_rental(customer_id, vehicle_id, start, end)
        print(f"Rental created with id {rid}.")
    except ValidationError as e:
        print(f"Error: {e}")


def return_vehicle(service: CarRentalService):
    print_header("Return Vehicle")
    items = service.list_rentals(status="active")
    if not items:
        print("No active rentals.")
        return
    for (rid, cid, vid, s, e, total, status) in items:
        print(f"[{rid}] Customer {cid} | Vehicle {vid} | {s} -> {e} | Total ${total:.2f}")
    rid = input_int("Rental id: ")
    try:
        service.return_vehicle(rid)
        print("Vehicle returned. Rental finished.")
    except ValidationError as e:
        print(f"Error: {e}")


def search_vehicles(service: CarRentalService):
    print_header("Search Vehicles")
    kw = input("Keyword (brand/model/type): ").strip()
    items = service.search_vehicles(kw)
    if not items:
        print("No matches.")
        return
    for (vid, brand, model, year, rate, vtype, avail) in items:
        print(f"[{vid}] {brand} {model} ({year}) - ${rate:.2f}/day - {vtype} - {'Available' if avail else 'Rented'}")


def list_rentals(service: CarRentalService, status: Optional[str] = None):
    items = service.list_rentals(status=status)
    if not items:
        print("No rentals found.")
        return
    for (rid, cid, vid, s, e, total, st) in items:
        print(f"[{rid}] Customer {cid} | Vehicle {vid} | {s} -> {e} | ${total:.2f} | {st}")


def seed_sample_data(service: CarRentalService):
    # Idempotent-ish seeding: try to add fixed customers/vehicles; ignore duplicates gracefully
    try:
        service.add_customer("Alice Smith", "alice@example.com", "+64 21 123 4567")
    except Exception:
        pass
    try:
        service.add_customer("Bob Lee", "bob@example.com", "+64 27 765 4321")
    except Exception:
        pass
    try:
        service.add_vehicle("Toyota", "Corolla", 2021, 45.0, "Economy")
    except Exception:
        pass
    try:
        service.add_vehicle("Nissan", "X-Trail", 2022, 80.0, "SUV")
    except Exception:
        pass
    try:
        service.add_vehicle("Ford", "Ranger", 2023, 95.0, "Truck")
    except Exception:
        pass
    print("Sample data seeded (customers & vehicles).")


def main_menu():
    service = CarRentalService()
    while True:
        print_header("Car Rental System - Main Menu")
        print("1) List all vehicles")
        print("2) List available vehicles")
        print("3) Search vehicles")
        print("4) Add vehicle")
        print("5) List customers")
        print("6) Add customer")
        print("7) Create rental")
        print("8) Return vehicle")
        print("9) List rentals (all)")
        print("10) List rentals (active)")
        print("11) List rentals (finished)")
        print("12) Seed sample data")
        print("0) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_vehicles(service, only_available=False)
        elif choice == "2":
            list_vehicles(service, only_available=True)
        elif choice == "3":
            search_vehicles(service)
        elif choice == "4":
            add_vehicle(service)
        elif choice == "5":
            list_customers(service)
        elif choice == "6":
            add_customer(service)
        elif choice == "7":
            create_rental(service)
        elif choice == "8":
            return_vehicle(service)
        elif choice == "9":
            list_rentals(service, status=None)
        elif choice == "10":
            list_rentals(service, status="active")
        elif choice == "11":
            list_rentals(service, status="finished")
        elif choice == "12":
            seed_sample_data(service)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_menu()
