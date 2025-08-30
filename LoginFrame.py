import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 20)

        # Form Frame
        form_frm = tk.Frame(self)
        form_frm.pack()

        # Title
        tk.Label(form_frm, text = "Login", font=("Helvetica", 16, "bold")).grid(row=1, column=1, columnspan=3, pady=5)

        # Username
        tk.Label(form_frm, text = "Username", font=("Helvetica", 12)).grid(row=2, column=1, padx=10, pady=5, sticky = "e")
        self.username_entry = tk.Entry(form_frm)
        self.username_entry.grid(row=2, column=2, padx=5, pady=5)

        # PIN
        tk.Label(form_frm, text = "PIN", font=("Helvetica", 12)).grid(row=3, column=1, padx=10, pady=5, sticky = "e")
        self.pin_entry = tk.Entry(form_frm, show = "*")
        self.pin_entry.grid(row=3, column=2, padx=10, pady=5)

        # Login Button
        login_btn = tk.Button(form_frm, text = "Submit", font=("Helvetica", 12), command=self.login)
        login_btn.grid(row=7, column=0, columnspan=3, pady=20)


    # Function to handle login
    def login(self):
        # Get username and PIN, encode the PIN to bytes
        username = self.username_entry.get()
        pin = self.pin_entry.get().encode('utf-8')

        # Open DB connection and verify credentials
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, role, pin FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

            # CHECK if the row exists
            if row:
                # Assign user_id, role and hashed_pin from DB
                user_id, role, hashed_pin = row

                # Verify PIN exists and matches
                if not bcrypt.checkpw(pin, hashed_pin):
                    self.clear_fields()
                    messagebox.showerror("Login Failed", "Invalid PIN")
                    return
                
                # If credentials are valid, switch to EmployeeFrame
                if role == "admin":
                    self.master.current_user_id = user_id
                    self.pack_forget()
                    self.master.admin_frame.pack(fill = "both", expand = True)
                elif role == "employee":
                    self.master.current_user_id = user_id
                    self.master.current_username = username
                    self.master.emp_frame.username_var.set(f"Employee: {self.master.current_username}")
                    self.pack_forget()
                    self.master.emp_frame.pack(fill = "both", expand = True)
            else:
                # If credentials are invalid, show error message
                self.clear_fields()
                tk.messagebox.showerror("Login Failed", "Invalid username")


        

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)