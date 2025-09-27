from tkinter import *
import tkinter as tk
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog
from tkinter import ttk


class AddTimeLog(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.bind("<Return>", self.on_enter_key)

        self.add_date = None
        self.add_start_time = None
        self.add_end_time = None


        # Image
        try:
            self.img = tk.PhotoImage(file="resources/logo.png")
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Image not found").pack(pady=10)
            print(f"Error loading logo: {e}")

        # Title
        tk.Label(self, text="Add Time Log", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Date Label
        date_frm = tk.Frame(self)
        date_frm.pack(pady=5)
        tk.Label(date_frm, text="Select Date: ").grid(row=0, column=0)
        self.start_date = DateEntry(
            date_frm, width=12, background="darkblue", foreground="white", borderwidth=2
        )
        self.start_date.grid(row=1, column=0, padx=10, pady=5)

        # Generate times from 6:30 AM to 7:30 PM in 15-minute increments
        times = []
        for hour in range(6, 20):  # 6 to 19
            for minute in [0, 15, 30, 45]:
                if hour == 6 and minute < 30:  # skip before 6:30
                    continue
                if hour == 19 and minute > 30:  # skip after 7:30 PM
                    continue
                times.append(f"{hour:02d}:{minute:02d}")

        # Start Time
        time_frm = tk.Frame(self)
        time_frm.pack(pady=5)
        tk.Label(time_frm, text="Shift Start: ").grid(row=0, column=0)
        self.start_time_combo = ttk.Combobox(time_frm, width=10, values=times, state="readonly")
        self.start_time_combo.grid(row=1, column=0, padx=10, pady=5)

        # End Time
        tk.Label(time_frm, text="Shift End: ").grid(row=0, column=1)
        self.end_time_combo = ttk.Combobox(time_frm, width=10, values=times, state="readonly")
        self.end_time_combo.grid(row=1, column=1)

        # Buttons Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)
        add_btn = tk.Button(btn_frm, text="Add Log", font=("Helvetica", 14), command=lambda: self.add_time_log(self.start_date.get_date().strftime("%Y-%m-%d"), self.start_time_combo.get(), self.end_time_combo.get(), 'Y'))
        add_btn.grid(row=0, column=1, padx=10)

        back_btn = tk.Button(btn_frm, text="Back", font=("Helvetica", 14), command=self.back_page)
        back_btn.grid(row=0, column=0, pady=5)

        # Enter key binding
        self.start_time_combo.bind("<Return>", self.on_enter_key)
        self.end_time_combo.bind("<Return>", self.on_enter_key)



    def add_time_log(self, date, clock_in, clock_out, manual_override):
        # Parse the clock-in and clock-out times
        start = datetime.strptime(f"{date} {clock_in}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date} {clock_out}", "%Y-%m-%d %H:%M")

        # Validate times
        if end <= start:
            messagebox.showerror("Invalid Time", "Clock-out time must be after clock-in time.")
            return
        
        # Validate date
        if datetime.now() > start:
            messagebox.showerror("Invalid Time", "Clock-in date cannot be in the past.")
            return
        
        if datetime.now() + timedelta(days=7) < start:
            messagebox.showerror("Invalid Time", "Clock-in date cannot be more than 7 days in the future.")
            return

        # Format times to ISO-like format with microseconds
        formatted_start = start.strftime("%Y-%m-%dT%H:%M:%S.%f")
        formatted_end = end.strftime("%Y-%m-%dT%H:%M:%S.%f")

        # Store in database
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO time_logs(user_id, clock_in_time, clock_out_time, manual_override) VALUES(?, ?, ?, ?)",
                (self.master.current_user_id, formatted_start, formatted_end, manual_override)
            )
            conn.commit()

        print("Time log added:", formatted_start, formatted_end, manual_override)
        messagebox.showinfo("Success", "Time log added successfully.")
        self.start_date.set_date(datetime.now().date())
        self.start_time_combo.set('')
        self.end_time_combo.set('')


    def on_enter_key(self, event):
        self.add_time_log(self.start_date.get_date().strftime("%Y-%m-%d"), self.start_time_combo.get(), self.end_time_combo.get(), 'Y')

    def back_page(self):
        self.pack_forget()
        self.master.emp_frame.pack(fill="both", expand=True)