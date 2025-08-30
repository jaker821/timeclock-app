import tkinter as tk
import sqlite3
from datetime import datetime
from TimeClockApp import TimeClockApp


def db_connect():
    conn = sqlite3.connect('timeclock.db')
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        PIN TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        clock_in_time TEXT,
        clock_out_time TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    return conn, cursor

def main():
    # Initialize Database
    conn, cursor = db_connect()

    # Initialize GUI and Login Screen
    app = TimeClockApp()

    app.mainloop()









if __name__ == "__main__":
    main()