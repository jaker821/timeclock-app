import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("timeclock.db")
cursor = conn.cursor()

# --- 1. Create 5 users if they don't exist ---
users = ["alice", "bob", "carol", "dave", "eve"]
for u in users:
    cursor.execute(
        "INSERT OR IGNORE INTO users(username, PIN, role) VALUES (?, ?, 'employee')",
        (u, "1234")
    )

# --- 2. Get user IDs ---
cursor.execute(
    "SELECT id, username FROM users WHERE username IN (?, ?, ?, ?, ?)",
    tuple(users)
)
user_ids = {username: uid for uid, username in cursor.fetchall()}

# --- 3. Generate shifts for 9/1/25 to 9/30/25 ---
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 9, 30)
delta = timedelta(days=1)

current_day = start_date
while current_day.date() <= end_date.date():
    for username in users:
        uid = user_ids[username]

        # Alternate shift length: mostly 8h, randomly some 9h for OT
        shift_hours = 8
        if current_day.weekday() in [2, 4] or random.random() < 0.3:  # random OT
            shift_hours = 9

        # Clock in at 9:00 AM
        clock_in = datetime.combine(current_day.date(), datetime.min.time()) + timedelta(hours=9)
        clock_out = clock_in + timedelta(hours=shift_hours)

        # Insert time log
        cursor.execute(
            "INSERT INTO time_logs(user_id, clock_in_time, clock_out_time, manual_override) VALUES (?, ?, ?, ?)",
            (uid, clock_in.isoformat(), clock_out.isoformat(), "N")
        )
        time_log_id = cursor.lastrowid

        # Add lunch break for some shifts (every 3rd day)
        if current_day.day % 3 == 0:
            lunch_duration = random.choice([15, 20, 30])
            cursor.execute(
                "INSERT INTO lunch_breaks(time_log_id, duration_minutes, created_at) VALUES (?, ?, ?)",
                (time_log_id, lunch_duration, datetime.now().isoformat())
            )

    current_day += delta

conn.commit()
conn.close()
print("Sample September 2025 data populated successfully!")
