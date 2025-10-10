
import unittest
from expense_tracker import ExpenseTracker, Expense


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker()

    # --- Add Expense ---
    def test_add_expense_valid(self):
        exp = self.tracker.add_expense("Coffee", 4.5)
        self.assertEqual(exp.description, "Coffee")
        self.assertEqual(exp.amount, 4.50)
        self.assertEqual(len(self.tracker.list_expenses()), 1)

    def test_add_expense_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("", 10)

    def test_add_expense_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Invalid", -1)

    def test_add_expense_rejects_nonnumeric_amount(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Invalid", "ten dollars")

    # --- Calculate Total ---
    def test_total_zero_when_empty(self):
        self.assertEqual(self.tracker.total(), 0.00)

    def test_total_multiple_items(self):
        self.tracker.add_expense("Coffee", 4.5)
        self.tracker.add_expense("Lunch", 12.40)
        self.tracker.add_expense("Bus", 3.10)
        self.assertEqual(self.tracker.total(), 20.00)

    def test_amount_rounded_to_two_decimals(self):
        self.tracker.add_expense("Weird amount", 1.999)
        self.assertEqual(self.tracker.list_expenses()[0].amount, 2.00)
        self.assertEqual(self.tracker.total(), 2.00)

    # --- Expense dataclass behavior ---
    def test_expense_is_immutable(self):
        exp = self.tracker.add_expense("Tea", 3.33)
        with self.assertRaises(Exception):
            exp.amount = 10.0


if __name__ == "__main__":
    unittest.main(verbosity=2)
