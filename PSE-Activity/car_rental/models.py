
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional


class Vehicle(ABC):
    """Abstract base class for all vehicles."""
    def __init__(self, brand: str, model: str, year: int, daily_rate: float):
        self._brand = brand
        self._model = model
        self._year = year
        self._daily_rate = daily_rate
        self._available = True  # encapsulated availability

    # Encapsulation via properties
    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def year(self) -> int:
        return self._year

    @property
    def daily_rate(self) -> float:
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Daily rate must be positive.")
        self._daily_rate = value

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, value: bool) -> None:
        self._available = bool(value)

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        ...

    def __str__(self) -> str:
        return f"{self.vehicle_type}: {self.brand} {self.model} ({self.year}) - ${self.daily_rate:.2f}/day"


class EconomyCar(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Economy"


class SUV(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "SUV"


class Truck(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Truck"


@dataclass
class Customer:
    id: Optional[int]
    name: str
    email: str
    phone: str


@dataclass
class Rental:
    id: Optional[int]
    customer_id: int
    vehicle_id: int
    start_date: date
    end_date: date
    total_cost: float
    status: str  # 'active' or 'finished'
