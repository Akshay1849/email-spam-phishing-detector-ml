import sqlite3
import os

def init_db():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "history.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        prediction TEXT,
        confidence REAL,
        phishing_score INTEGER,
        risk_level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()