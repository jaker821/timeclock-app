import tkinter as tk
from LoginFrame import LoginFrame
from EmployeeFrame import EmployeeFrame
from AdminFrame import AdminFrame
from CreateUserFrame import CreateUserFrame
from ViewEmployeesFrame import ViewEmployeesFrame
from ExportDataFrame import ExportDataFrame
import sqlite3
import bcrypt
from tkinter import messagebox

class TimeClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Clock App")
        self.geometry("500x350")
        self.resizable(width=False, height=False)

        self.current_user_id = None
        self.current_username = None
        self.current_window = "login_frame"

        # Initialize the database first
        try:
            self.conn, self.cursor = self.initialize_database()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database:\n{e}")
            self.destroy()
            return

        # Now create frames safely
        try:
            self.login_frame = LoginFrame(self)
            self.emp_frame = EmployeeFrame(self)
            self.admin_frame = AdminFrame(self)
            self.create_user_frame = CreateUserFrame(self)
            self.view_employees_frame = ViewEmployeesFrame(self)
            self.export_data_frame = ExportDataFrame(self)

            self.login_frame.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Frame Error", f"Error creating frames:\n{e}")
            self.destroy()

    def initialize_database(self):
        conn = sqlite3.connect("timeclock.db")
        cursor = conn.cursor()

        # Create tables if they don't exist
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
                manual_override TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Check for admin user
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        row = cursor.fetchone()

        if not row:
            self.create_admin_modal(cursor, conn)

        conn.commit()
        return conn, cursor

    def create_admin_modal(self, cursor, conn):
        """Creates a modal Toplevel window to set the admin PIN."""
        top = tk.Toplevel(self)
        top.title("Admin Setup")
        top.geometry("300x200")
        top.resizable(width=False, height=False)
        top.grab_set()
        top.focus_set()
        top.transient(self)

        tk.Label(top, text="Set Admin PIN", font=("Helvetica", 14)).pack(pady=10)
        pin_entry = tk.Entry(top, show="*")
        pin_entry.pack(pady=5)

        def save_pin():
            pin = pin_entry.get()
            if not pin:
                messagebox.showerror("Missing PIN", "Please enter a PIN for the admin user.")
                return

            hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, PIN, role) VALUES (?, ?, ?)",
                ("admin", hashed_pin, "admin")
            )
            conn.commit()
            messagebox.showinfo("Success", "Admin user created successfully.")
            top.destroy()

        tk.Button(top, text="Save", command=save_pin).pack(pady=20)
        self.wait_window(top)
