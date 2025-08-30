import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
import webbrowser

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

        # Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=20)

        # Login Button
        login_btn = tk.Button(btn_frm, text = "Submit", font=("Helvetica", 12), command=self.login)
        login_btn.grid(row = 0, column = 1, padx=5)

        # Quit Button
        quit_btn = tk.Button(btn_frm, text = "Quit", font=("Helvetica", 12), command=self.master.quit)
        quit_btn.grid(row = 0, column = 0, padx=5)

        # Bind Enter key to login
        self.master.bind('<Return>', self.on_enter_key)


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
                    self.show_menu()
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


    def show_menu(self):
        # MENU BAR
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)

        # Add commands to the File menu
        file_menu.add_command(label="Add Employee", command=self.master.admin_frame.create_user)
        file_menu.add_command(label="View Employees", command=self.master.admin_frame.view_employees)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.master.admin_frame.logout)
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Add commands to the Help menu
        help_menu.add_command(label="Help", command=self.open_help_site)

    def hide_menu(self):
        print("Hiding menu")
        self.master.config(menu=tk.Menu(self.master))

    def open_help_site(self):
        webbrowser.open("https://github.com/jaker821/timeclock-app/blob/main/help.md")

    def on_enter_key(self, event):
        # Check if Enter key is pressed
        if event.keysym == 'Return':
            self.login()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)