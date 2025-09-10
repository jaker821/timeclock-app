import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class EmployeeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        try:
            self.img = tk.PhotoImage(file="resources/logo.png")
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
        self.username_var.set("Employee Username: ")
        tk.Label(self, textvariable=self.username_var, font=("Helvetica", 12, "bold")).pack(pady=5)

        # Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)

        # Buttons
        tk.Button(btn_frm, text="Clock In", font=("Helvetica", 14), command=self.clock_in).grid(pady=5, padx=5, row=0, column=0, sticky="w")
        tk.Button(btn_frm, text="Clock Out", font=("Helvetica", 14), command=self.clock_out).grid(pady=5, padx=5, row=0, column=1, sticky="e")
        tk.Button(btn_frm, text="Logout", font=("Helvetica", 14), command=self.logout).grid(pady=5, row=1, column=0, columnspan=2)

    # --- Clock Update ---
    def update_clock(self):
        now = datetime.now().strftime("%a, %b-%d-%Y %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    # --- Database Helpers ---
    def get_open_shift(self):
        with sqlite3.connect('timeclock.db') as conn:
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

                with sqlite3.connect('timeclock.db') as conn:
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
            clock_in_dt = datetime.strptime(open_shift[1], "%Y-%m-%dT%H:%M:%S.%f")
            if clock_in_dt.date() < datetime.now().date():
                self.prompt_missing_clock_out(open_shift[0], open_shift[1])
                return
            else:
                messagebox.showwarning("Warning", "You are already clocked in today!")
                return

        current_time = datetime.now().isoformat()
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO time_logs(user_id, clock_in_time, manual_override) VALUES(?, ?, ?)",
                (self.master.current_user_id, current_time, "N")
            )
            conn.commit()
        print("Clocked In", current_time)

    # --- Clock Out ---
    def clock_out(self):
        open_shift = self.get_open_shift()
        if not open_shift:
            messagebox.showwarning("Warning", "No active clock-in found. Please clock in first.")
            return

        clock_in_dt = datetime.strptime(open_shift[1], "%Y-%m-%dT%H:%M:%S.%f")
        if clock_in_dt.date() < datetime.now().date():
            self.prompt_missing_clock_out(open_shift[0], open_shift[1])
            return

        current_time = datetime.now().isoformat()
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE time_logs SET clock_out_time=?, manual_override=? WHERE id=?",
                (current_time, "N", open_shift[0])
            )
            conn.commit()
        print("Clocked Out", current_time)

    # --- Logout ---
    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.hide_menu()
        self.master.login_frame.pack(fill="both", expand=True)
