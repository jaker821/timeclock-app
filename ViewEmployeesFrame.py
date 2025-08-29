import tkinter as tk
from tkinter import ttk
import sqlite3

class ViewEmployeesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Title
        tk.Label(self, text = "Employees", font=("Helvetica", 16, "bold")).pack(pady = 10)

        # Tree View
        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Role"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Role", text="Role")
        self.tree.pack(fill = "both", expand = True)

        self.load_users()

        # Back Button
        tk.Button(self, text = "Back to Admin", command = self.back_page).pack()


    def load_users(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load users from DB
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

            for col in ("ID", "Username", "Role"):
                self.tree.column(col, width = 100, anchor = "center", stretch = True)
                self.tree.heading(col, text = col.title())

    def back_page(self):
        self.pack_forget()
        self.master.admin_frame.pack(fill = "both", expand = True)
