import tkinter as tk
import sqlite3
import tkinter.messagebox
import bcrypt

class ManageUsersFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Form Frame
        form_frm = tk.Frame(self)
        form_frm.pack()

        # Title
        tk.Label(form_frm, text = "Create New User").grid(row=1, column=1, columnspan=3, pady=10)

        # Create Username Input
        tk.Label(form_frm, text = "Username").grid(row=2, column=1, padx=10, pady=5, sticky = "e")
        self.username_entry = tk.Entry(form_frm)
        self.username_entry.grid(row=2, column=2, padx=5, pady=5)

        # Create PIN Input
        tk.Label(form_frm, text = "PIN").grid(row=3, column=1, padx=10, pady=5, sticky = "e")
        self.pin_entry = tk.Entry(form_frm, show = "*")
        self.pin_entry.grid(row=3, column=2, padx=10, pady=5)

        # Create User Button
        create_btn = tk.Button(form_frm, text = "Create", command=self.create_user)
        create_btn.grid(row=7, column=0, columnspan=3, pady=20)

        # Logout and Back Button
        tk.Button(self, text = "Back to Admin", command = self.back_page).pack()
        tk.Button(self, text = "Logout", command = self.logout).pack()
        

    def create_user(self):
        username = self.username_entry.get()
        pin = self.pin_entry.get()

        hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt())

        with sqlite3.connect('timeclock.db') as conn:
            
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if username == "" or pin == "":
                tk.messagebox.showerror("Missing Fields", "Please fill in all fields.")
                return
            elif row:
                tk.messagebox.showerror("User already exists", f"Username {username} already exists. Please choose a different username.")
                self.clear_fields()
                return
            else:
                cursor.execute("INSERT INTO users (username, PIN, role) VALUES (?, ?, ?)", (username, hashed_pin, "employee"))
                self.clear_fields()
                tk.messagebox.showinfo("User Created", f"Username: {username} Pin: {pin}")
                


            conn.commit()


    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)


    def back_page(self):
        self.pack_forget()
        self.master.admin_frame.pack(fill = "both", expand = True)

    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
