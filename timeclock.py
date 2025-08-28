import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Timeclock App")
    root.geometry("400x300")

    label = tk.Label(root, text="Time Clock Application")
    label.pack()

    clock_in_btn = tk.Button(root, text="Clock In", command=clock_in)
    clock_in_btn.pack(padx=10, pady=10)
    
    clock_out_btn = tk.Button(root, text="Clock Out", command=clock_out)
    clock_out_btn.pack(padx=10, pady=10)

    root.mainloop()

def clock_in():
    print("Clocked In")

def clock_out():
    print("Clocked Out")


if __name__ == "__main__":
    main()