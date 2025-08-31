import tkinter as tk
import sqlite3

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 20)

        # Admin Frame Title
        # tk.Label(self, text = "Admin", font=("Helvetica", 20, "bold")).pack(pady = 10)

        # Employee Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)

        # Create Employee Buttons
        tk.Button(btn_frm, text = "Create Employees", font=("Helvetica", 14), command = self.create_user).grid(row = 0, column = 0, padx = 5)
        tk.Button(btn_frm, text = "View Employees", font = ("Helvetica", 14), command = self.view_employees).grid(row = 0, column = 1, padx = 5)

        # Employee Time Button
        tk.Button(self, text = "View Employee Time Logs", font=("Helvetica", 14), command = lambda: print("View Employee Time Logs")).pack(pady = 10)

        # Logout Button
        tk.Button(self, text = "Logout", command = self.logout).pack(pady = 30)

    def create_user(self):
        self.master.current_window = "create_user_frame"
        self.pack_forget()
        self.master.create_user_frame.pack(fill = "both", expand = True)

    def view_employees(self):
        self.master.current_window = "view_employees_frame"
        self.pack_forget()
        self.master.view_employees_frame.pack(fill = "both", expand = True)
        print("View Employees")

    def logout(self):
        self.pack_forget()
        self.master.login_frame.hide_menu()
        self.master.login_frame.clear_fields()
        
        self.master.login_frame.pack(fill = "both", expand = True)
