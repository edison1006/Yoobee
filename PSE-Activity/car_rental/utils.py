
from __future__ import annotations
from datetime import datetime, date
from typing import Tuple


DATE_FMT = "%Y-%m-%d"  # ISO-like date input


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s.strip(), DATE_FMT).date()
    except Exception as e:
        raise ValueError(f"Invalid date '{s}'. Expected format YYYY-MM-DD.") from e


def input_date(prompt: str) -> date:
    while True:
        s = input(prompt).strip()
        try:
            return parse_date(s)
        except ValueError as e:
            print(e)


def input_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except Exception:
            print("Please enter a valid integer.")


def input_float(prompt: str) -> float:
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if v <= 0:
                print("Please enter a positive number.")
                continue
            return v
        except Exception:
            print("Please enter a valid number.")
