import tkinter as tk
from datetime import datetime
import sqlite3
from tkinter import messagebox

class EmployeeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 20)

        #Clock
        self.clock_label = tk.Label(self, font=("Helvetica", 20, "italic"))
        self.clock_label.pack(pady=10)

        # Update Clock
        self.update_clock()

        # Button Frame
        btn_frm = tk.Frame(self)
        btn_frm.pack(pady=10)

        # Buttons
        tk.Button(btn_frm, text = "Clock In", font = ("Helvetica", 14), command = self.clock_in).grid(pady=5, padx=5, row=0, column=0, sticky = "w")
        tk.Button(btn_frm, text = "Clock Out", font = ("Helvetica", 14), command = self.clock_out).grid(pady=5, padx=5, row=0, column=1, sticky = "e")
        tk.Button(btn_frm, text = "Logout", font = ("Helvetica", 14), command = self.logout).grid(pady=5, row=1, column=0, columnspan=2)

    def clock_in(self):
        # Grab Current Time
        current_time = datetime.now().isoformat()

        # Open DB connection and insert clock-in time
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()

            # Check if there's an existing clock-in without clock-out
            cursor.execute("SELECT id, user_id FROM time_logs WHERE user_id = ? AND clock_out_time IS NULL ORDER BY clock_in_time DESC LIMIT 1", (self.master.current_user_id,))
            row = cursor.fetchone()

            # If there's a clock-in without clock-out, don't allow clock-in
            if row:
                tk.messagebox.showwarning("Warning", "You are already clocked in!")
                print("You are already clocked in!")
                return
            else:
                cursor.execute("INSERT INTO time_logs(user_id, clock_in_time) VALUES(?, ?)", (self.master.current_user_id, current_time))
                conn.commit()

        # Print Clock In Time for debugging
        print("Clocked In", current_time)

    def clock_out(self):
        # Grab Current Time
        current_time = datetime.now().isoformat()

        # Open DB connection and update clock-out time for the latest clock-in without clock-out
        with sqlite3.connect('timeclock.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, id FROM time_logs 
                WHERE user_id = ? AND clock_out_time IS NULL
                ORDER BY clock_in_time DESC LIMIT 1
            """, (self.master.current_user_id,))

            row = cursor.fetchone()

            if row:
                latest_id = row[1]
                cursor.execute("""
                    UPDATE time_logs
                    SET clock_out_time = ?
                    WHERE id = ?
                """, (current_time, latest_id))
            else:
                print("No active clock-in found. Please clock in first.")
                tk.messagebox.showwarning("Warning", "No active clock-in found. Please clock in first.")
                return
            
            conn.commit()
    
        print("Clocked Out", current_time)

    def update_clock(self):
        now = datetime.now().strftime("%a" + ", " + "%b-%d-%Y %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)
    
    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
