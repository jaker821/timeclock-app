import tkinter as tk

class EmployeeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Image
        self.img = tk.PhotoImage(file = "resources/logo.png")
        self.img_small = self.img.subsample(2, 2)
        tk.Label(self, image=self.img_small).pack(pady = 20)

        # Buttons
        tk.Button(self, text = "Clock In", command = self.clock_in).pack()
        tk.Button(self, text = "Clock Out", command = self.clock_out).pack()
        tk.Button(self, text = "Logout", command = self.logout).pack()

    def clock_in(self):
        print("Logged In")

    def clock_out(self):
        print("Logged Out")

    def logout(self):
        self.pack_forget()
        self.master.login_frame.clear_fields()
        self.master.login_frame.pack(fill = "both", expand = True)
