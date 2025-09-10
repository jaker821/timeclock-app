import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from TimeClockApp import TimeClockApp
import bcrypt


def main():
    app = TimeClockApp()
    app.mainloop()


if __name__ == "__main__":
    main()
