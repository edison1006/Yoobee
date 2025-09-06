
# Car Rental System (CLI, Python, OOP + Strategy Pattern)

A command-line Car Rental System built with Python that demonstrates OOP principles
(encapsulation, abstraction, inheritance, polymorphism), uses the **Strategy Pattern**
for pricing, persists data with **SQLite** (standard library `sqlite3`), and includes
robust input validation and error handling.

> **How to run**
> 1) Ensure Python 3.10+ is installed.
> 2) (Optional) Create and activate a virtual environment.
> 3) Install dependencies: `pip install -r requirements.txt` (no external deps; safe to run).
> 4) Start the app: `python main.py`
> 5) (Optional) Seed sample data: from the menu choose "Seed sample data" once, or run `python seed.py`.

## Features
- Add/list/search **Vehicles** (EconomyCar, SUV, Truck via inheritance from `Vehicle`)
- Add/list **Customers**
- Create **Rentals**, return vehicles, view active/finished rentals
- **SQLite** persistence (database file `car_rental.db` auto-created on first run)
- **Strategy Pattern** for pricing (standard, SUV premium, weekend discount)
- Robust validation: date parsing, input validation, overlapping-rental checks, availability
- Clear separation of concerns: `models`, `repository`, `services`, `pricing`, `cli`, `utils`

## OOP & Pattern Mapping
- **Encapsulation**: attributes protected via properties and service layer
- **Abstraction**: abstract base classes for `Vehicle` and `PricingStrategy`
- **Inheritance**: `EconomyCar`, `SUV`, `Truck` inherit from `Vehicle`
- **Polymorphism**: vehicle string representations; pricing strategies implement `compute_cost`
- **Design Pattern**: **Strategy Pattern** (`pricing.py`) determines pricing behavior by vehicle type and dates

## Project Structure
```
car_rental_cli/
├── README.md
├── requirements.txt
├── main.py
├── cli.py
├── models.py
├── pricing.py
├── repository.py
├── services.py
├── utils.py
├── seed.py
└── car_rental.db           (created at first run)
```

## Notes
- No manual config needed; DB initializes itself.
- `requirements.txt` is included but empty (standard library only).
- Works fully offline; tested on Python 3.10+.
