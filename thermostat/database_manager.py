import os
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="thermostat.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(base_dir, db_name)
        self.initialize_database()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def initialize_database(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    temperature_f REAL NOT NULL,
                    humidity REAL NOT NULL,
                    mode TEXT NOT NULL,
                    set_point INTEGER NOT NULL,
                    status TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alert_level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    temperature_f REAL,
                    humidity REAL,
                    mode TEXT
                )
            """)

            conn.commit()

    def insert_reading(self, temperature_f, humidity, mode, set_point, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO readings (timestamp, temperature_f, humidity, mode, set_point, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, temperature_f, humidity, mode, set_point, status))
            conn.commit()

    def insert_alert(self, alert_level, message, temperature_f=None, humidity=None, mode=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alerts (timestamp, alert_level, message, temperature_f, humidity, mode)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, alert_level, message, temperature_f, humidity, mode))
            conn.commit()

    def get_recent_readings(self, limit=10):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, temperature_f, humidity, mode, set_point, status
                FROM readings
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_recent_alerts(self, limit=10):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, alert_level, message, temperature_f, humidity, mode
                FROM alerts
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()