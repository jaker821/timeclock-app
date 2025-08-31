import tkinter as tk
from tkinter import ttk
import sqlite3
import bcrypt
from tkinter import messagebox

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

        # Bind a double-click event to the Treeview widget
        self.tree.bind("<Double-1>", self.edit_user)


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
                if not row[1] == "DEVELOPER_ADMIN":  # Exclude DEV user
                    self.tree.insert("", "end", values=row)
                    continue

            for col in ("ID", "Username", "Role"):
                self.tree.column(col, width = 100, anchor = "center")
                self.tree.heading(col, text = col.title())



    def edit_user(self, event):
        # Get the selected item
        selected_item = self.tree.selection()

        # Check if an item is selected
        if selected_item:
            # Get user details
            item = self.tree.item(selected_item)
            user_id, username, role = item['values']

            # Open the edit user dialog
            def edit_user_dialog(user_id, username):
                # Create a new window for editing user
                edit_user = tk.Toplevel(self)
                edit_user.title("Edit User")
                edit_user.geometry("300x250")

                # Delete User Functionality
                tk.Label(edit_user, text = "Delete User", font=("Helvetica", 12)).pack(pady=10)


                # Delete user functionality
                def delete_user(user_id, username):
                    if tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {username}?"):
                        with sqlite3.connect('timeclock.db') as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                            conn.commit()
                        tk.messagebox.showinfo("User Deleted", f"User {username} has been deleted.")
                        edit_user.destroy()
                        self.load_users()

                # Delete Button
                tk.Button(edit_user, text = f"Delete User: {username}", fg="red", command = lambda: delete_user(user_id, username)).pack(pady=5)

                # Edit User PIN Functionality
                tk.Label(edit_user, text=f"Edit PIN for Username: {username}", font=("Helvetica", 12)).pack(pady=10)
                tk.Label(edit_user, text="New PIN:").pack(pady=5)
                new_pin_entry = tk.Entry(edit_user, show="*")
                new_pin_entry.pack(pady=5)

                
                # Save button functionality
                def save_new_pin():
                    # Get the new PIN
                    new_pin = new_pin_entry.get()

                    # Validate and update the PIN in the database
                    if new_pin:
                        hashed_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt())
                        with sqlite3.connect('timeclock.db') as conn:
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET PIN = ? WHERE id = ?", (hashed_pin, user_id))
                            conn.commit()
                        tk.messagebox.showinfo("Success", f"PIN updated for user {username}.")
                        edit_user.destroy()

                    # Prompt user to enter a new PIN
                    else:
                        tk.messagebox.showerror("Error", "Please enter a new PIN.")

                # Save Button
                tk.Button(edit_user, text="Save", command=save_new_pin).pack(pady=10)
                edit_user.mainloop()

                

            # Open the edit user dialog
            edit_user_dialog(user_id, username)


    def back_page(self):
        self.master.current_window = "admin_frame"
        self.pack_forget()
        self.master.admin_frame.pack(fill = "both", expand = True)
