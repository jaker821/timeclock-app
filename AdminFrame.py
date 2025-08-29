import tkinter as tk
import sqlite3

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 20)

        # Buttons
        tk.Label(self, text = "Admin Frame").pack(pady = 20)
        tk.Button(self, text = "Manage Users", command = self.manage_users).pack(pady = 10)
        tk.Button(self, text = "Logout", command = self.logout).pack()

    def manage_users(self):
        self.pack_forget()
        self.master.manage_users_frame.pack(fill = "both", expand = True)

    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
