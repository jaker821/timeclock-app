import tkinter as tk
import sqlite3

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 10)

        # Admin Frame Title
        tk.Label(self, text = "Admin Frame", font=("Helvetica", 24, "bold")).pack(pady = 10)

        # Buttons
        tk.Button(self, text = "Manage Employees", font=("Helvetica", 14), command = self.manage_users).pack(pady = 5)
        tk.Button(self, text = "View Employees", font = ("Helvetica", 14), command = self.view_employees).pack(pady = 5)
        tk.Button(self, text = "Logout", command = self.logout).pack(pady = 10)

    def manage_users(self):
        self.pack_forget()
        self.master.manage_users_frame.pack(fill = "both", expand = True)

    def view_employees(self):
        self.pack_forget()
        self.master.view_employees_frame.pack(fill = "both", expand = True)
        print("View Employees")

    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
