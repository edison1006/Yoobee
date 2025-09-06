
# Optional: seed via script (the menu already has 'Seed sample data')
from services import CarRentalService

if __name__ == "__main__":
    svc = CarRentalService()
    print("Seeding sample data...")
    from cli import seed_sample_data
    seed_sample_data(svc)
    print("Done.")
