
import sqlite3
from contextlib import contextmanager
from datetime import date
from typing import List, Optional, Tuple, Any

DB_NAME = "car_rental.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            );""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS vehicles(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                daily_rate REAL NOT NULL,
                vehicle_type TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1
            );""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS rentals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                total_cost REAL NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('active','finished')),
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
            );""")


# ------------ Customers -------------
def add_customer(name: str, email: str, phone: str) -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO customers(name, email, phone) VALUES (?,?,?)", (name, email, phone))
        return cur.lastrowid


def list_customers() -> List[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone FROM customers ORDER BY id")
        return cur.fetchall()


def get_customer(customer_id: int) -> Optional[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone FROM customers WHERE id=?", (customer_id,))
        return cur.fetchone()


# ------------ Vehicles -------------
def add_vehicle(brand: str, model: str, year: int, daily_rate: float, vehicle_type: str) -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vehicles(brand, model, year, daily_rate, vehicle_type, available)
            VALUES (?,?,?,?,?,1)
        """, (brand, model, year, daily_rate, vehicle_type))
        return cur.lastrowid


def list_vehicles(only_available: bool = False) -> List[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        if only_available:
            cur.execute("""SELECT id, brand, model, year, daily_rate, vehicle_type, available
                           FROM vehicles WHERE available=1 ORDER BY id""")
        else:
            cur.execute("""SELECT id, brand, model, year, daily_rate, vehicle_type, available
                           FROM vehicles ORDER BY id""")
        return cur.fetchall()


def search_vehicles(keyword: str) -> List[Tuple[Any, ...]]:
    like = f"%{keyword.lower()}%"
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""SELECT id, brand, model, year, daily_rate, vehicle_type, available
                       FROM vehicles
                       WHERE lower(brand) LIKE ? OR lower(model) LIKE ? OR lower(vehicle_type) LIKE ?
                       ORDER BY id""", (like, like, like))
        return cur.fetchall()


def get_vehicle(vehicle_id: int) -> Optional[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""SELECT id, brand, model, year, daily_rate, vehicle_type, available
                       FROM vehicles WHERE id=?""", (vehicle_id,))
        return cur.fetchone()


def set_vehicle_availability(vehicle_id: int, available: bool) -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE vehicles SET available=? WHERE id=?", (1 if available else 0, vehicle_id))


# ------------ Rentals -------------
def add_rental(customer_id: int, vehicle_id: int, start_date: date, end_date: date, total_cost: float) -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rentals(customer_id, vehicle_id, start_date, end_date, total_cost, status)
            VALUES (?,?,?,?,?, 'active')
        """, (customer_id, vehicle_id, start_date.isoformat(), end_date.isoformat(), total_cost))
        return cur.lastrowid


def list_rentals(status: Optional[str] = None) -> List[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        if status:
            cur.execute("""SELECT id, customer_id, vehicle_id, start_date, end_date, total_cost, status
                           FROM rentals WHERE status=? ORDER BY id""", (status,))
        else:
            cur.execute("""SELECT id, customer_id, vehicle_id, start_date, end_date, total_cost, status
                           FROM rentals ORDER BY id""")
        return cur.fetchall()


def get_rental(rental_id: int) -> Optional[Tuple[Any, ...]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""SELECT id, customer_id, vehicle_id, start_date, end_date, total_cost, status
                       FROM rentals WHERE id=?""", (rental_id,))
        return cur.fetchone()


def finish_rental(rental_id: int) -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE rentals SET status='finished' WHERE id=?", (rental_id,))


def has_overlapping_rental(vehicle_id: int, start_date: date, end_date: date) -> bool:
    with get_conn() as conn:
        cur = conn.cursor()
        # Check for any active rental that overlaps the requested period
        cur.execute("""
            SELECT COUNT(*)
            FROM rentals
            WHERE vehicle_id=? AND status='active' AND NOT (
                date(end_date) < date(?) OR date(start_date) > date(?)
            )
        """, (vehicle_id, start_date.isoformat(), end_date.isoformat()))
        (count,) = cur.fetchone()
        return count > 0
