
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List


class PricingStrategy(ABC):
    """Strategy interface for pricing."""
    @abstractmethod
    def compute_cost(self, days: int, base_daily_rate: float, start: date, end: date) -> float:
        ...


class StandardPricing(PricingStrategy):
    def compute_cost(self, days: int, base_daily_rate: float, start: date, end: date) -> float:
        return round(days * base_daily_rate, 2)


class SUVPremiumPricing(PricingStrategy):
    """Adds a 20% premium for SUVs."""
    def compute_cost(self, days: int, base_daily_rate: float, start: date, end: date) -> float:
        return round(days * base_daily_rate * 1.20, 2)


class WeekendDiscountPricing(PricingStrategy):
    """10% off for weekend days (Sat/Sun)."""
    def compute_cost(self, days: int, base_daily_rate: float, start: date, end: date) -> float:
        d = start
        total = 0.0
        while d <= end:
            rate = base_daily_rate * 0.9 if d.weekday() >= 5 else base_daily_rate  # 5=Sat,6=Sun
            total += rate
            d += timedelta(days=1)
        return round(total, 2)


class PricingContext:
    """Selects a pricing strategy based on vehicle type and/or dates."""
    def __init__(self, vehicle_type: str):
        self.vehicle_type = vehicle_type

    def choose(self, start: date, end: date) -> PricingStrategy:
        # Example rules:
        # - SUV gets a premium strategy
        # - For all vehicles, if the rental includes weekend days, apply weekend discount strategy
        # - Otherwise standard
        includes_weekend = any(((start.toordinal() + i) % 7) in (5, 6) for i in range((end - start).days + 1))
        if self.vehicle_type == "SUV":
            return SUVPremiumPricing()
        if includes_weekend:
            return WeekendDiscountPricing()
        return StandardPricing()
