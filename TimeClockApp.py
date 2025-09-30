import tkinter as tk
from tkinter import messagebox
from LoginFrame import LoginFrame
from EmployeeFrame import EmployeeFrame
from AdminFrame import AdminFrame
from CreateUserFrame import CreateUserFrame
from ViewEmployeesFrame import ViewEmployeesFrame
from ExportDataFrame import ExportDataFrame
from AddTimeLog import AddTimeLog

import sqlite3
import bcrypt
import shutil
import os
from datetime import datetime
import glob
from utils import get_resource_path, get_db_path  # <-- use helper functions

class TimeClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Clock App")
        self.geometry("500x350")
        self.resizable(width=False, height=False)

        self.current_user_id = None
        self.current_username = None
        self.current_window = "login_frame"

        self.protocol("WM_DELETE_WINDOW", self.safe_quit)

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
            self.add_time_log = AddTimeLog(self)

            self.login_frame.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Frame Error", f"Error creating frames:\n{e}")
            self.destroy()

        

    def initialize_database(self):
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lunch_breaks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_log_id INTEGER NOT NULL,
                duration_minutes INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(time_log_id) REFERENCES time_logs(id)
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

            hashed_pin = bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, PIN, role) VALUES (?, ?, ?)",
                ("admin", hashed_pin, "admin")
            )
            conn.commit()
            messagebox.showinfo("Success", "Admin user created successfully.")
            top.destroy()

        tk.Button(top, text="Save", command=save_pin).pack(pady=20)
        self.wait_window(top)

    def cleanup_old_backups(self, backup_folder=None, max_backups=500):
        if backup_folder is None:
            backup_folder = get_resource_path("backups")

        backups = glob.glob(os.path.join(backup_folder, "*.db"))
        if len(backups) <= max_backups:
            return

        backups.sort(key=os.path.getctime)  # oldest first
        for old_backup in backups[:-max_backups]:
            try:
                os.remove(old_backup)
                print(f"Deleted old backup: {old_backup}")
            except Exception as e:
                print(f"Failed to delete {old_backup}: {e}")

    def backup_database(self, db_path=None, backup_folder=None):
        if db_path is None:
            db_path = get_db_path()
        if backup_folder is None:
            backup_folder = get_resource_path("backups")

        os.makedirs(backup_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_folder, f"time_tracker_backup_{timestamp}.db")
        try:
            shutil.copy2(db_path, backup_file)
            print(f"Database backup created: {backup_file}")
            self.cleanup_old_backups(backup_folder, max_backups=500)
        except Exception as e:
            print(f"Error creating database backup: {e}")

    def safe_quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.backup_database()
            self.conn.close()
            self.destroy()
