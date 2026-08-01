import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'expense_tracker.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123"))
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 250.0,  "Food",          "2026-08-01", "Lunch at cafe"),
        (user_id, 120.0,  "Transport",     "2026-08-03", "Auto fare"),
        (user_id, 1500.0, "Bills",         "2026-08-05", "Electricity bill"),
        (user_id, 800.0,  "Health",        "2026-08-08", "Pharmacy"),
        (user_id, 600.0,  "Entertainment", "2026-08-10", "Movie tickets"),
        (user_id, 2200.0, "Shopping",      "2026-08-12", "Clothes"),
        (user_id, 350.0,  "Food",          "2026-08-15", "Groceries"),
        (user_id, 450.0,  "Other",         "2026-08-18", "Miscellaneous"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()
