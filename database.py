
import sqlite3
import json
from datetime import datetime

DATABASE = "osrm.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            input_data TEXT,
            result_data TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_history(module, algorithm, input_data, result_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO performance_history
        (module, algorithm, input_data, result_data, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        module,
        algorithm,
        json.dumps(input_data),
        json.dumps(result_data),
        datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM performance_history
        ORDER BY id DESC
    """)

    records = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return records


def delete_history(record_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM performance_history WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()
