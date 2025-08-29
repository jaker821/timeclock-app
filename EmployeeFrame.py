import tkinter as tk
from datetime import datetime

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
        print("Logged In")

    def clock_out(self):
        print("Logged Out")

    def update_clock(self):
        now = datetime.now().strftime("%a" + ", " + "%b-%d-%Y %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)
    
    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
