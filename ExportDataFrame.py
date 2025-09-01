from tkinter import *
import tkinter as tk
import sqlite3
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog
import csv


class ExportDataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Variables
        self.start_date = None
        self.end_date = None

        # Image
        try:
            self.img = tk.PhotoImage(file = "resources/logo.png")
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady = 10)
        except Exception as e:
            tk.Label(self, text = "Image not found").pack(pady = 10)
            print(f"Error loading logo: {e}")

        # Title
        tk.Label(self, text = "Export Time Logs", font = ("Helvetica", 16, "bold")).pack(pady = 10)  

        # Start Date Label
        start_date_frm = tk.Frame(self)
        start_date_frm.pack(pady = 10)
        tk.Label(start_date_frm, text = "Start Date: ").grid(row = 0, column = 0)
        self.start_date = DateEntry(start_date_frm, width = 12, background = 'darkblue', foreground = 'white', borderwidth = 2)
        self.start_date.grid(row = 0, column = 1)

        # End Date Label
        end_date_frm = tk.Frame(self)
        end_date_frm.pack(pady = 10)
        tk.Label(end_date_frm, text = "End Date: ").grid(row = 0, column = 0)
        self.end_date = DateEntry(end_date_frm, width = 12, background = 'darkblue', foreground = 'white', borderwidth = 2)
        self.end_date.grid(row = 0, column = 1)
        
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady = 10)
        self.export_btn = tk.Button(btn_frame, text = "Export to .csv", font = ("Helvetica", 12), command = self.collect_time_logs)
        self.export_btn.grid(row = 0, column = 0, pady = 5)
        self.back_btn = tk.Button(btn_frame, text = "Back", font = ("Helvetica", 10), command = self.back_page)
        self.back_btn.grid(row = 1, column = 0)


    def select_start_date(self):
        self.open_calendar("start")
    
    def select_end_date(self):
        self.open_calendar("end")

    def open_calendar(self, start_or_end):
        top = Toplevel(self)
        top.title("Select Date")

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(fill="both", expand=True)

        def on_select():
            if start_or_end == "start":
                self.start_date = cal.get_date()
            elif start_or_end == "end":
                self.end_date = cal.get_date()
            top.destroy()

        tk.Button(top, text="OK", command=on_select).pack()
        print(self.start_date, self.end_date)

    def collect_time_logs(self):
        start_date = self.start_date.get_date().strftime("%Y-%m-%d") + " T00:00:00.000000"
        end_date = self.end_date.get_date().strftime("%Y-%m-%d") + " T23:59:59.000000"

        emp_totals = {}

        with sqlite3.connect("timeclock.db") as conn:
            cursor = conn.cursor()

            cursor.execute("""
                    SELECT u.username, t.clock_in_time, t.clock_out_time 
                    FROM time_logs t 
                    JOIN users u ON t.user_id = u.id 
                    WHERE t.clock_in_time >= ?
                           AND (t.clock_out_time <= ? OR t.clock_out_time IS NULL) 
                    ORDER BY u.id ASC
                    """, (start_date, end_date))
            data = cursor.fetchall()

            for row in data:
                print(row)
                username = row[0]
                clock_in = row[1]
                clock_out = row[2]

                if clock_out is None:
                    continue

                clock_in_dt = datetime.strptime(clock_in, "%Y-%m-%dT%H:%M:%S.%f")
                clock_out_dt = datetime.strptime(clock_out, "%Y-%m-%dT%H:%M:%S.%f")

                hours_worked = (clock_out_dt - clock_in_dt).total_seconds() / 3600

                if username in emp_totals:
                    emp_totals[username] += hours_worked
                else:
                    emp_totals[username] = hours_worked

            
        self.export_to_csv(emp_totals)


    def export_to_csv(self, emp_totals):
        # File Destination Dialog
        file_destination = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Save CSV File")

        # Check if a file was selected
        if not file_destination:
            return

        # Save file
        try:
            with open(file_destination, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                # Write header
                writer.writerow(["Username", "Hours Worked"])

                # Write data
                for username, hours_worked in emp_totals.items():
                    writer.writerow([username, round(hours_worked, 2)])

                # Show success message
                tk.messagebox.showinfo("Success", f"File saved successfully to:\n{file_destination}")

        # Handle errors
        except Exception as e:
            # Show error message
            tk.messagebox.showerror("Error", f"Error saving file: {e}")
            print(f"Error saving file: {e}")
            return



    def back_page(self):
        self.master.current_window = "admin_frame"
        self.pack_forget()
        self.master.admin_frame.pack(fill = "both", expand = True)
