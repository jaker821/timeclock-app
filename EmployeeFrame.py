import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from utils import get_resource_path, get_db_path  # ✅ use helpers


class EmployeeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.logout_timer = None
        self.reset_auto_logout()  # start timer

        # Bind events to reset timer
        self.bind_all("<Any-KeyPress>", lambda e: self.reset_auto_logout())
        self.bind_all("<Any-Button>", lambda e: self.reset_auto_logout())
        self.bind_all("<Motion>", lambda e: self.reset_auto_logout())

        # Image (load from AppData/resources)
        try:
            logo_path = get_resource_path("logo.png")
            self.img = tk.PhotoImage(file=logo_path)
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Image not found").pack(pady=10)
            print(f"Error loading logo: {e}")  

        # Clock
        self.clock_label = tk.Label(self, font=("Helvetica", 20, "italic"))
        self.clock_label.pack(pady=5)
        self.update_clock()

        # Employee Frame Title
        self.username_var = tk.StringVar()

        # Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=5)

        # Buttons
        tk.Button(btn_frm, text="Clock In", font=("Helvetica", 14), command=self.clock_in).grid(pady=5, padx=5, row=0, column=0, sticky="w")
        tk.Button(btn_frm, text="Clock Out", font=("Helvetica", 14), command=self.clock_out).grid(pady=5, padx=5, row=0, column=1, sticky="e")

        # Lunch Break
        tk.Button(btn_frm, text="Lunch Break", font=("Helvetica", 14), command=self.lunch_break).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(btn_frm, text="Add Time Log", font=("Helvetica", 12), command=self.add_time_log).grid(pady=10, row=2, column=0, columnspan=3)
        tk.Button(btn_frm, text="Logout", font=("Helvetica", 10), command=self.logout).grid(pady=10, row=3, column=0, columnspan=3)

    # --- Clock Update ---
    def update_clock(self):
        now = datetime.now().strftime("%a, %b-%d-%Y %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    # --- Database Helpers ---
    def get_open_shift(self):
        db_path = get_db_path()  # ✅ use AppData DB
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, clock_in_time 
                FROM time_logs 
                WHERE user_id = ? AND clock_out_time IS NULL 
                ORDER BY clock_in_time DESC LIMIT 1
            """, (self.master.current_user_id,))
            return cursor.fetchone()

    # --- Prompt Missing Clock Out ---
    def prompt_missing_clock_out(self, shift_id, clock_in_time):
        top = tk.Toplevel(self)
        top.title("Missing Clock Out")
        top.geometry("350x200")
        top.resizable(width=False, height=False)

        tk.Label(top, text=f"You forgot to clock out for {clock_in_time[:10]}").pack(pady=5)
        tk.Label(top, text="Select Clock Out Time").pack(pady=5)

        hours = [f"{i:02}" for i in range(24)]
        minutes = [f"{i:02}" for i in [0, 15, 30, 45]]

        hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
        minute_var = tk.StringVar(value="00")

        cb_frame = tk.Frame(top)
        cb_frame.pack(pady=10)

        hour_cb = ttk.Combobox(cb_frame, width=3, values=hours, textvariable=hour_var, state="readonly")
        hour_cb.grid(row=0, column=0, padx=5)
        minute_cb = ttk.Combobox(cb_frame, width=3, values=minutes, textvariable=minute_var, state="readonly")
        minute_cb.grid(row=0, column=1, padx=5)

        def save_clock_out():
            try:
                h = int(hour_var.get())
                m = int(minute_var.get())
                clock_in_dt = datetime.strptime(clock_in_time, "%Y-%m-%dT%H:%M:%S.%f")
                clock_out_dt = clock_in_dt.replace(hour=h, minute=m)

                if clock_out_dt <= clock_in_dt:
                    messagebox.showerror("Invalid Time", "Clock out must be after clock in.")
                    return

                db_path = get_db_path()
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE time_logs SET clock_out_time=?, manual_override=? WHERE id=?",
                        (clock_out_dt.isoformat(), "Y", shift_id)
                    )
                    conn.commit()

                messagebox.showinfo("Success", "Previous shift updated. You can now clock in/out.")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(top, text="Save", command=save_clock_out).pack(pady=5)

        top.grab_set()
        top.focus_set()

    # --- Clock In ---
    def clock_in(self):
        open_shift = self.get_open_shift()
        if open_shift:
            messagebox.showwarning("Warning", "You are already clocked in today!")
            return

        current_time = datetime.now().strftime("%I:%M %p")
        db_path = get_db_path()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO time_logs(user_id, clock_in_time, manual_override) VALUES(?, ?, ?)",
                (self.master.current_user_id, datetime.now().isoformat(), "N")
            )
            conn.commit()

        # --- POP-UP ---
        messagebox.showinfo("Clocked In", f"You have successfully clocked in at {current_time}")

    # --- Clock Out ---
    def clock_out(self):
        open_shift = self.get_open_shift()
        if not open_shift:
            messagebox.showwarning("Warning", "No active clock-in found.")
            return

        current_time = datetime.now().strftime("%I:%M %p")
        db_path = get_db_path()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE time_logs SET clock_out_time=?, manual_override=? WHERE id=?",
                (datetime.now().isoformat(), "N", open_shift[0])
            )
            conn.commit()

        # --- POP-UP ---
        messagebox.showinfo("Clocked Out", f"You have successfully clocked out at {current_time}")

    # --- Lunch Break ---
    def lunch_break(self):
        top = tk.Toplevel(self)
        top.title("Lunch Break")
        top.geometry("300x150")
        top.resizable(False, False)

        tk.Label(top, text="Select Lunch Break Duration:").pack(pady=10)

        options = ["10", "15", "20", "25", "30", "45", "60"]
        duration_var = tk.StringVar(value=options[0])

        combo = ttk.Combobox(top, values=options, textvariable=duration_var, state="readonly")
        combo.pack(pady=5)

        def save_lunch_break():
            minutes = int(duration_var.get())
            open_shift = self.get_open_shift()
            if not open_shift:
                messagebox.showwarning("Warning", "You must be clocked in to log a lunch break.")
                return

            db_path = get_db_path()
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO lunch_breaks (time_log_id, duration_minutes, created_at) VALUES (?, ?, ?)",
                    (open_shift[0], minutes, datetime.now().isoformat())
                )
                conn.commit()

            messagebox.showinfo("Success", f"Lunch break of {minutes} minutes recorded.")
            top.destroy()

        tk.Button(top, text="Save", command=save_lunch_break).pack(pady=10)
        top.grab_set()
        top.focus_set()

    def reset_auto_logout(self):
        if self.logout_timer:
            self.after_cancel(self.logout_timer)
        self.logout_timer = self.after(self.AUTO_LOGOUT_MINUTES * 60 * 1000, self.auto_logout)

    def auto_logout(self):
        tk.messagebox.showinfo("Auto Logout", "You have been logged out due to inactivity.")
        self.logout()

    # --- Open Add Time Log ---
    def add_time_log(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.hide_menu()
        self.master.add_time_log.pack(fill="both", expand=True)

    # --- Logout ---
    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.hide_menu()
        self.master.login_frame.pack(fill="both", expand=True)
