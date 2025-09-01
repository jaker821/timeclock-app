import tkinter as tk
import sqlite3

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        try:
            self.img = tk.PhotoImage(file = "resources/logo.png")
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady = 10)
        except Exception as e:
            tk.Label(self, text = "Image not found").pack(pady = 10)
            print(f"Error loading logo: {e}")  

        # Employee Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)

        # Create Employee Buttons
        tk.Button(btn_frm, text = "Create Employees", font=("Helvetica", 14), command = self.create_user).grid(row = 0, column = 0, padx = 5)
        tk.Button(btn_frm, text = "View Employees", font = ("Helvetica", 14), command = self.view_employees).grid(row = 0, column = 1, padx = 5)

        # Export Employee Time Logs Button
        tk.Button(self, text = "Export Time Logs", font=("Helvetica", 14), command = self.export_data_frame).pack(pady = 10)

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

    def export_data_frame(self):
        self.master.current_window = "export_data_frame"
        self.pack_forget()
        self.master.export_data_frame.pack(fill = "both", expand = True)

    def logout(self):
        self.pack_forget()
        self.master.login_frame.hide_menu()
        self.master.login_frame.clear_fields()
        
        self.master.login_frame.pack(fill = "both", expand = True)
