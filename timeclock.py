import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from TimeClockApp import TimeClockApp
import bcrypt


# Admin setup window
def admin_setup(conn, cursor):
    # Create a modal window to set up the admin user
    admin_setup_window = tk.Toplevel()
    admin_setup_window.title("Admin Setup")
    admin_setup_window.geometry("300x200")
    admin_setup_window.resizable(width=False, height=False)

    # Admin PIN label and entry
    tk.Label(admin_setup_window, text="Set Admin PIN", font=("Helvetica", 14)).pack(pady=10)
    pin_entry = tk.Entry(admin_setup_window, show="*")
    pin_entry.pack(pady=5)

    # Save PIN button
    def save_pin():
        # Get PIN and encode to bytes
        admin_pin_bytes = pin_entry.get().encode('utf-8')

        # Validate a PIN was entered
        if not admin_pin_bytes:
            messagebox.showerror("Missing PIN", "Please enter a PIN for the admin user.")
            return
    
        # Hash the PIN and insert admin user into DB
        hashed_pin = bcrypt.hashpw(admin_pin_bytes, bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, PIN, role) VALUES (?, ?, ?)", ('admin', hashed_pin, 'admin'))

        # Commit changes
        conn.commit()

        # Close the setup window
        admin_setup_window.destroy()

    # Save PIN button
    tk.Button(admin_setup_window, text="Save", command=save_pin).pack(pady=20)

    # Make the window modal and focused on top
    admin_setup_window.transient()
    admin_setup_window.grab_set()
    admin_setup_window.lift()
    admin_setup_window.focus_force()

    return admin_setup_window


def db_connect(root):
    conn = sqlite3.connect('timeclock.db')
    cursor = conn.cursor()


    # Creat tables if they don't exist
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

    # Create ADMIN user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    row = cursor.fetchone()

    # If no admin user, prompt to create one
    if not row:
        win = admin_setup(conn, cursor)
        root.wait_window(win)


    conn.commit()

    return conn, cursor

def main():
    root = TimeClockApp()
    root.withdraw()

    # Initialize Database
    conn, cursor = db_connect(root)

    # Initialize GUI and Login Screen
    root.deiconify()
    root.mainloop()









if __name__ == "__main__":
    main()