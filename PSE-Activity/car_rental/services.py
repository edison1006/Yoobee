
from __future__ import annotations
from datetime import date, timedelta
from typing import Optional, List, Tuple, Any

import repository as repo
from pricing import PricingContext


class ValidationError(Exception):
    pass


class CarRentalService:
    def __init__(self):
        repo.init_db()

    # -------- Customers --------
    def add_customer(self, name: str, email: str, phone: str) -> int:
        if not name or not email or not phone:
            raise ValidationError("Name, email, and phone are required.")
        return repo.add_customer(name.strip(), email.strip().lower(), phone.strip())

    def list_customers(self) -> List[Tuple[Any, ...]]:
        return repo.list_customers()

    # -------- Vehicles --------
    def add_vehicle(self, brand: str, model: str, year: int, daily_rate: float, vehicle_type: str) -> int:
        if not all([brand, model, vehicle_type]):
            raise ValidationError("Brand, model, and vehicle_type are required.")
        if year < 1980 or year > date.today().year + 1:
            raise ValidationError("Year is out of valid range.")
        if daily_rate <= 0:
            raise ValidationError("Daily rate must be positive.")
        return repo.add_vehicle(brand.strip(), model.strip(), year, float(daily_rate), vehicle_type.strip())

    def list_vehicles(self, only_available: bool = False) -> List[Tuple[Any, ...]]:
        return repo.list_vehicles(only_available=only_available)

    def search_vehicles(self, keyword: str) -> List[Tuple[Any, ...]]:
        return repo.search_vehicles(keyword.strip())

    # -------- Rentals --------
    def create_rental(self, customer_id: int, vehicle_id: int, start: date, end: date) -> int:
        # validate foreign keys
        customer = repo.get_customer(customer_id)
        if not customer:
            raise ValidationError(f"Customer {customer_id} does not exist.")
        vehicle = repo.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValidationError(f"Vehicle {vehicle_id} does not exist.")

        _, brand, model, year, daily_rate, vehicle_type, available = vehicle

        if start > end:
            raise ValidationError("Start date cannot be after end date.")
        if (end - start).days + 1 <= 0:
            raise ValidationError("Invalid rental duration.")
        if not available:
            raise ValidationError("Vehicle is currently not available.")
        if repo.has_overlapping_rental(vehicle_id, start, end):
            raise ValidationError("Vehicle already has an overlapping active rental.")

        days = (end - start).days + 1
        strategy = PricingContext(vehicle_type).choose(start, end)
        total_cost = strategy.compute_cost(days, float(daily_rate), start, end)

        rental_id = repo.add_rental(customer_id, vehicle_id, start, end, total_cost)
        repo.set_vehicle_availability(vehicle_id, False)
        return rental_id

    def return_vehicle(self, rental_id: int) -> None:
        rental = repo.get_rental(rental_id)
        if not rental:
            raise ValidationError(f"Rental {rental_id} does not exist.")
        _id, customer_id, vehicle_id, start_date, end_date, total_cost, status = rental
        if status != 'active':
            raise ValidationError("Rental is already finished.")
        repo.finish_rental(rental_id)
        repo.set_vehicle_availability(vehicle_id, True)

    def list_rentals(self, status: Optional[str] = None) -> List[Tuple[Any, ...]]:
        if status and status not in ('active', 'finished'):
            raise ValidationError("Status must be 'active' or 'finished'.")
        return repo.list_rentals(status=status)
