from abc import ABC, abstractmethod
from dataclasses import dataclass

# ---- Data Model ----
@dataclass(frozen=True
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

class RoadService(TransportService):
    @abstractmethod

class SeaService(TransportService):
    @abstractmethod

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
    
class TaxiService(TransportService):
    def plan(self, trip: Trip) -> str:
        return f"Taxi from {trip.origin} to {trip.destination}"
    def fare(self, trip: Trip) -> float:
        # Example rule: flat rate of $20 plus $2 per stop
        return 20 + (trip.stops * 2)

class BikeService(TransportService):
    def plan(self, trip: Trip) -> str:
        return f"Bike from {trip.origin} to {trip.destination}"
    def fare(self, trip: Trip) -> float:
        # Example rule: flat rate of $5
        return 5.0
    
class BoatService(TransportService):
    def plan(self, trip: Trip) -> str:
        return f"Boat from {trip.origin} to {trip.destination}"
    def fare(self, trip: Trip) -> float:
        # Example rule: flat rate of $30
        return 30.0

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
    
if __name__ == "__main__":
    # Example usage
    trip = Trip(origin="Mankau", destination="Long Bay", stops=10)
    
    # Using Train Service
    train_service = Factory.get_service("train")
    transport = ATransport(train_service)
    print(transport.plan_trip(trip))  # Output: Train from Mankau to Long Bay
    print(f"Fare: ${transport.calculate_fare(trip):.2f}")  # Output: Fare: $15.00
    
    # Using Bus Service
    bus_service = Factory.get_service("bus")
    transport = ATransport(bus_service)
    print(transport.plan_trip(trip))  # Output: Bus from Mankau to Long Bay
    print(f"Fare: ${transport.calculate_fare(trip):.2f}")  # Output: Fare: $8.00