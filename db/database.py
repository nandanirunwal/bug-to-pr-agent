import sqlite3
import os
from datetime import datetime

DB_PATH = "db/runs.db"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS runs")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_file TEXT,
            bug_found TEXT,
            fixed INTEGER,
            pr_url TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database ready!")

def save_run(input_file: str, bug_found: str, fixed: bool, pr_url: str, status: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO runs (timestamp, input_file, bug_found, fixed, pr_url, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        input_file,
        bug_found,
        1 if fixed else 0,
        pr_url or "",
        status
    ))
    conn.commit()
    conn.close()
    print("Run saved to database!")

def get_all_runs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM runs")
    rows = cursor.fetchall()
    conn.close()
    return rows