
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Expense:
    """Represents a single expense item."""
    description: str
    amount: float

    def __post_init__(self) -> None:
        # Validate description
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Description must be a non-empty string.")

        # Validate and normalize amount
        try:
            amt = float(self.amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a number.")

        if amt < 0:
            raise ValueError("Amount must be non-negative.")

        # Normalize to 2 decimal places (currency-style)
        object.__setattr__(self, "amount", round(amt, 2))


class ExpenseTracker:
    """Tracks expenses and computes totals."""

    def __init__(self) -> None:
        self._expenses: List[Expense] = []

    def add_expense(self, description: str, amount: float) -> Expense:
        """Add a new expense and return the created Expense object."""
        expense = Expense(description, amount)
        self._expenses.append(expense)
        return expense

    def total(self) -> float:
        """Return the total amount of all recorded expenses (rounded to 2 decimals)."""
        return round(sum(e.amount for e in self._expenses), 2)

    def list_expenses(self) -> List[Expense]:
        """Return a copy of the current expense list."""
        return list(self._expenses)


if __name__ == "__main__":
    # Minimal interactive demo
    print("Personal Expense Tracker (type 'q' to quit)")
    tracker = ExpenseTracker()
    while True:
        desc = input("Description: ").strip()
        if desc.lower() == "q":
            break
        amt_str = input("Amount: ").strip()
        if amt_str.lower() == "q":
            break
        try:
            tracker.add_expense(desc, float(amt_str))
            print(f"Added: {desc} - ${float(amt_str):.2f}")
            print(f"Current total: ${tracker.total():.2f}\n")
        except Exception as e:
            print(f"Error: {e}\n")

    print(f"Final total: ${tracker.total():.2f}")
