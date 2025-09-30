import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt

# Import the APPDATA-aware path utility
from utils import get_db_path


class ViewEmployeesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Title
        tk.Label(self, text="Employees", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Role"), show='headings')
        for col in ("ID", "Username", "Role"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.load_users()

        # Back Button
        tk.Button(self, text="Back", command=self.back_page).pack(pady=5)

        # Double-click event for editing
        self.tree.bind("<Double-1>", self.edit_user)

    def load_users(self):
        """Reload the employee list from the DB."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            rows = cursor.fetchall()

            for row in rows:
                if row[1] != "DEVELOPER_ADMIN":  # skip dev admin
                    self.tree.insert("", "end", values=row)

    def edit_user(self, event):
        """Open the edit user dialog for the selected user."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        user_id, username, role = self.tree.item(selected_item)['values']

        edit_user = tk.Toplevel(self)
        edit_user.title(f"Edit User: {username}")
        edit_user.geometry("300x250")
        edit_user.grab_set()
        edit_user.focus_set()
        edit_user.transient(self)

        # --- Delete Section ---
        tk.Label(edit_user, text="Delete User", font=("Helvetica", 12)).pack(pady=5)

        def delete_user():
            if messagebox.askyesno("Confirm Delete", f"Delete user {username}?"):
                with sqlite3.connect(get_db_path()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                messagebox.showinfo("User Deleted", f"{username} removed.")
                edit_user.destroy()
                self.load_users()

        tk.Button(edit_user, text=f"Delete {username}", fg="red", command=delete_user).pack(pady=5)

        # --- Update PIN Section ---
        tk.Label(edit_user, text=f"Change PIN for {username}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(edit_user, text="New PIN:").pack()
        new_pin_entry = tk.Entry(edit_user, show="*")
        new_pin_entry.pack(pady=5)

        def save_new_pin():
            new_pin = new_pin_entry.get()
            if not new_pin:
                messagebox.showerror("Error", "Enter a new PIN.")
                return
            hashed_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt())
            with sqlite3.connect(get_db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET PIN = ? WHERE id = ?", (hashed_pin, user_id))
                conn.commit()
            messagebox.showinfo("Success", f"PIN updated for {username}.")
            edit_user.destroy()

        tk.Button(edit_user, text="Save PIN", command=save_new_pin).pack(pady=10)

        # Block until closed
        self.wait_window(edit_user)

    def back_page(self):
        self.master.current_window = "admin_frame"
        self.pack_forget()
        self.master.admin_frame.pack(fill="both", expand=True)
