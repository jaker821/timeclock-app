import tkinter as tk
import sqlite3
from tkinter import filedialog, messagebox
import shutil
import os

from utils import get_resource_path, get_appdata_path, get_db_path


class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        try:
            logo_path = get_resource_path("logo.png")
            self.img = tk.PhotoImage(file=logo_path)
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Image not found").pack(pady=10)
            print(f"Error loading logo: {e}")

        # Employee Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)

        # Create Employee Buttons
        tk.Button(btn_frm, text="Create Employees", font=("Helvetica", 14), command=self.create_user).grid(row=0, column=0, padx=5)
        tk.Button(btn_frm, text="View Employees", font=("Helvetica", 14), command=self.view_employees).grid(row=0, column=1, padx=5)

        # Export Employee Time Logs Button
        tk.Button(self, text="Export Time Logs", font=("Helvetica", 14), command=self.export_data_frame).pack(pady=10)

        # Restore Backup Button
        tk.Button(self, text="Restore Backup", font=("Helvetica", 10), command=self.restore_backup).pack(pady=5)

        # Logout Button
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def create_user(self):
        self.master.current_window = "create_user_frame"
        self.pack_forget()
        self.master.create_user_frame.pack(fill="both", expand=True)

    def view_employees(self):
        self.master.current_window = "view_employees_frame"
        self.pack_forget()
        self.master.view_employees_frame.pack(fill="both", expand=True)

    def export_data_frame(self):
        self.master.current_window = "export_data_frame"
        self.pack_forget()
        self.master.export_data_frame.pack(fill="both", expand=True)

    def restore_backup(self):
        # AppData backups folder
        backups_dir = get_appdata_path("backups")

        # Ask admin to select a backup file
        backup_file = filedialog.askopenfilename(
            title="Select Backup to Restore",
            filetypes=[("SQLite Database", "*.db")],
            initialdir=backups_dir
        )

        if backup_file:
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Restore",
                f"Are you sure you want to restore from:\n{os.path.basename(backup_file)}?\nThis will overwrite the current database."
            )
            if confirm:
                try:
                    # Close existing DB connection
                    self.master.conn.close()

                    # Main DB path in AppData
                    db_path = get_db_path()


                    # Copy backup over main database
                    shutil.copy2(backup_file, db_path)

                    # Reopen DB connection
                    self.master.conn, self.master.cursor = self.master.initialize_database()

                    messagebox.showinfo("Restore Complete", "Backup successfully restored.")
                except Exception as e:
                    messagebox.showerror("Restore Failed", f"Could not restore backup:\n{e}")

    def logout(self):
        self.pack_forget()
        self.master.login_frame.hide_menu()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill="both", expand=True)
