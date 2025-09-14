from abc import ABC, abstractmethod
from dataclasses import dataclass

# ---- Data Model ----
@dataclass(frozen=True)
class Trip:
    origin: str
    destination: str
    stops: int                 # Number of stations between origin and destination

# ---- Abstract Base Class (Interface) ----
class TransportService(ABC):
    """Abstract base class for all transport services in Auckland Transport."""

    @abstractmethod
    def plan(self, trip: Trip) -> str:
        """Return a description of the trip plan."""
        pass

    @abstractmethod
    def fare(self, trip: Trip) -> float:
        """Return the estimated fare in NZD based on stops."""
        pass

# ---- Concrete Implementations ----
class TrainService(TransportService):
    def plan(self, trip: Trip) -> str:
        return f"Train from {trip.origin} to {trip.destination}"
    def fare(self, trip: Trip) -> float:
        # Example rule: each stop costs $1.5
        return trip.stops * 1.5

class BusService(TransportService):
    def plan(self, trip: Trip) -> str:
        return f"Bus from {trip.origin} to {trip.destination}"
    def fare(self, trip: Trip) -> float:
        # Example rule: each stop costs $0.8
        return trip.stops * 0.8

# ---- Factory ----
class Factory:
    @staticmethod
    def get_service(mode: str) -> TransportService:
        if mode == "train":
            return TrainService()
        elif mode == "bus":
            return BusService()
        else:
            raise ValueError(f"Unknown transport mode: {mode}")


# ---- Client (uses Factory + singleton) ----
class ATransport:
    def __init__(self, service: TransportService):
        self.service = service

    def plan_trip(self, trip: Trip) -> str:
        return self.service.plan(trip)

    def calculate_fare(self, trip: Trip) -> float:
        return self.service.fare(trip)


# ---- Demo ----
if __name__ == "__main__":
    # Example trip: from Maukau to Albany with 10 stops
    trip = Trip(origin="Maukau", destination="Albany", stops=10)

    for mode in ["train", "bus"]:
        service = Factory.get_service(mode)
        print(service.plan(trip))
        print(f"Fare: ${service.fare(trip):.2f}")