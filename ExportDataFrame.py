from tkinter import *
import tkinter as tk
import sqlite3
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from collections import defaultdict
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side


class ExportDataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Variables
        self.start_date = None
        self.end_date = None

        # Image
        try:
            self.img = tk.PhotoImage(file="resources/logo.png")
            self.img_small = self.img.subsample(2, 2)
            tk.Label(self, image=self.img_small).pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Image not found").pack(pady=10)
            print(f"Error loading logo: {e}")

        # Title
        tk.Label(self, text="Export Time Logs", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Start Date Label
        start_date_frm = tk.Frame(self)
        start_date_frm.pack(pady=10)
        tk.Label(start_date_frm, text="Start Date: ").grid(row=0, column=0)
        self.start_date = DateEntry(
            start_date_frm, width=12, background="darkblue", foreground="white", borderwidth=2
        )
        self.start_date.grid(row=0, column=1)

        # End Date Label
        end_date_frm = tk.Frame(self)
        end_date_frm.pack(pady=10)
        tk.Label(end_date_frm, text="End Date: ").grid(row=0, column=0)
        self.end_date = DateEntry(
            end_date_frm, width=12, background="darkblue", foreground="white", borderwidth=2
        )
        self.end_date.grid(row=0, column=1)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        self.export_btn = tk.Button(
            btn_frame,
            text="Export to Excel",
            font=("Helvetica", 12),
            command=self.handle_export
        )
        self.export_btn.grid(row=0, column=0, pady=5)
        self.back_btn = tk.Button(
            btn_frame, text="Back", font=("Helvetica", 10), command=self.back_page
        )
        self.back_btn.grid(row=1, column=0)

    def handle_export(self):
        # Get dates from DateEntry widgets as strings
        start_date = self.start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date.get_date().strftime("%Y-%m-%d")

        # Collect logs
        audit_dict, emp_totals, date_range = self.collect_time_logs(start_date, end_date)

        # Export to Excel
        self.export_to_excel(audit_dict, emp_totals, date_range)

    def select_start_date(self):
        self.open_calendar("start")

    def select_end_date(self):
        self.open_calendar("end")

    def open_calendar(self, start_or_end):
        top = Toplevel(self)
        top.title("Select Date")

        cal = Calendar(
            top,
            font="Arial 14",
            selectmode="day",
            locale="en_US",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
        )
        cal.pack(fill="both", expand=True)

        def on_select():
            if start_or_end == "start":
                self.start_date.set_date(cal.get_date())
            elif start_or_end == "end":
                self.end_date.set_date(cal.get_date())
            top.destroy()

        tk.Button(top, text="OK", command=on_select).pack()
        print(self.start_date, self.end_date)

    def collect_time_logs(self, start_date, end_date):
        conn = sqlite3.connect("timeclock.db")
        cursor = conn.cursor()

        # Get all users (so we can pre-fill their days)
        cursor.execute("SELECT username FROM users WHERE role = 'employee' ORDER BY id ASC")
        all_usernames = [row[0] for row in cursor.fetchall()]

        # Build full date range
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        date_range = [start_dt + timedelta(days=i) for i in range((end_dt - start_dt).days + 1)]

        # Pre-fill audit_dict: every user, every date, empty list
        audit_dict = {username: {d: [] for d in date_range} for username in all_usernames}
        emp_totals = {username: 0 for username in all_usernames}

        # Query logs (filter only on clock_in_time)
        cursor.execute(
            """
            SELECT u.username, t.clock_in_time, t.clock_out_time 
            FROM time_logs t 
            JOIN users u ON t.user_id = u.id 
            WHERE date(t.clock_in_time) BETWEEN ? AND ?
            AND u.role = 'employee'
            ORDER BY u.id ASC
            """,
            (start_date, end_date),
        )
        data = cursor.fetchall()

        for username, clock_in, clock_out in data:
            # Parse clock in
            clock_in_dt = datetime.strptime(clock_in, "%Y-%m-%dT%H:%M:%S.%f")
            day = clock_in_dt.date()

            # Handle missing clock out
            if clock_out is None:
                shift_str = f"{clock_in_dt.strftime('%H:%M')}-???"
                audit_dict[username][day].append(shift_str)
                continue

            # Normal complete shift
            clock_out_dt = datetime.strptime(clock_out, "%Y-%m-%dT%H:%M:%S.%f")
            hours_worked = (clock_out_dt - clock_in_dt).total_seconds() / 3600
            emp_totals[username] += hours_worked

            shift_str = f"{clock_in_dt.strftime('%H:%M')}-{clock_out_dt.strftime('%H:%M')}"
            audit_dict[username][day].append(shift_str)

        conn.close()
        return audit_dict, emp_totals, date_range


    def export_to_excel(self, audit_dict, emp_totals, date_range):
        file_destination = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Excel File",
        )

        if not file_destination:
            return

        try:
            wb = Workbook()

            # --- Sheet 1: Totals ---
            ws_totals = wb.active
            ws_totals.title = "Totals"
            ws_totals.append(["Username", "Total Hours"])
            for username, total in emp_totals.items():
                ws_totals.append([username, round(total, 2)])

            # --- Sheet 2: Audit Log ---
            ws_audit = wb.create_sheet("Audit Log")

            # Header row: Username + dates
            header = ["Username"] + [d.strftime("%Y-%m-%d") for d in date_range]
            ws_audit.append(header)

            # Rows: one per user
            for username in sorted(audit_dict.keys()):
                row = [username]
                for d in date_range:
                    shifts = audit_dict[username].get(d, [])
                    row.append("; ".join(shifts) if shifts else "")
                ws_audit.append(row)

            # Auto column widths
            for ws in [ws_totals, ws_audit]:
                for col in ws.columns:
                    max_length = 0
                    col_letter = get_column_letter(col[0].column)
                    for cell in col:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    ws.column_dimensions[col_letter].width = max_length + 2

            from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

            # Styling helpers
            bold_font = Font(bold=True)
            header_fill = PatternFill(start_color="FFD966", end_color="FFD966", fill_type="solid")  # light yellow
            center_align = Alignment(horizontal="center", vertical="center")
            thin_border = Border(
                left=Side(style="thin"),
                right=Side(style="thin"),
                top=Side(style="thin"),
                bottom=Side(style="thin"),
            )

            # Apply to both sheets
            for ws in [ws_totals, ws_audit]:
                # Freeze top row
                ws.freeze_panes = "B2"

                # Style headers
                for cell in ws[1]:
                    cell.font = bold_font
                    cell.fill = header_fill
                    cell.alignment = center_align

                # Apply borders and auto-width
                for col in ws.columns:
                    col_letter = get_column_letter(col[0].column)
                    max_length = 0
                    for cell in col:
                        # Borders
                        cell.border = thin_border
                        # Track max width
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    # Set width (minimum 12)
                    ws.column_dimensions[col_letter].width = max(max_length + 2, 12)

            wb.save(file_destination)
            tk.messagebox.showinfo("Success", f"File saved successfully to:\n{file_destination}")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving file: {e}")
            print(f"Error saving file: {e}")

    def back_page(self):
        self.master.current_window = "admin_frame"
        self.pack_forget()
        self.master.admin_frame.pack(fill="both", expand=True)
