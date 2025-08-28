import tkinter as tk
import sqlite3
from datetime import datetime


def db_connect():
    conn = sqlite3.connect('timeclock.db')
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        PIN TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        clock_in_time TEXT,
        clock_out_time TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    return conn, cursor



def main():
    conn, cursor = db_connect()

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
    current_time = datetime.now().isoformat()

    with sqlite3.connect('timeclock.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO time_logs(user_id, clock_in_time) VALUES(?, ?)", (1, current_time))
        conn.commit()

    print("Clocked In", current_time)



def clock_out():
    current_time = datetime.now().isoformat()

    with sqlite3.connect('timeclock.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id FROM time_logs 
            WHERE user_id = ? AND clock_out_time IS NULL
            ORDER BY clock_in_time DESC LIMIT 1
        """, (1,))

        row = cursor.fetchone()

        if row:
            latest_id = row[0]
            cursor.execute("""
                UPDATE time_logs
                SET clock_out_time = ?
                WHERE id = ?
            """, (current_time, latest_id))
        conn.commit()
    
    print("Clocked Out", current_time)









if __name__ == "__main__":
    main()