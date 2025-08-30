import tkinter as tk
from LoginFrame import LoginFrame
from EmployeeFrame import EmployeeFrame
from AdminFrame import AdminFrame
from ManageUsersFrame import ManageUsersFrame
from ViewEmployeesFrame import ViewEmployeesFrame

class TimeClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Clock App")
        self.geometry("500x350")
        self.resizable(width=False, height=False)

        self.current_user_id = None
        self.current_username = None

        self.login_frame = LoginFrame(self)
        self.emp_frame = EmployeeFrame(self)
        self.admin_frame = AdminFrame(self)
        self.manage_users_frame = ManageUsersFrame(self)
        self.view_employees_frame = ViewEmployeesFrame(self)

        self.login_frame.pack(fill="both", expand=True)
        