import sqlite3
import os
from datetime import datetime

DB_PATH = "data/sentineleye.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            screenshot_path TEXT,
            threat_level TEXT,
            threat_type TEXT,
            confidence INTEGER,
            description TEXT,
            reason TEXT,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(screenshot_path, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scans (timestamp, screenshot_path, threat_level, threat_type, confidence, description, reason, action)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        screenshot_path,
        result["threat_level"],
        result["threat_type"],
        result.get("confidence", 0),
        result["description"],
        result.get("reason", ""),
        result["action"]
    ))
    conn.commit()
    conn.close()

def get_all_scans():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database updated!")
