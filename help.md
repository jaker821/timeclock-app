# Time Clock App - Help Guide

Welcome to the **Time Clock App**! This guide will help you understand how to use the application, whether you are an **employee** or an **admin**.

---

## Table of Contents

1. [Login](#login)
2. [Employee Functions](#employee-functions)
   - Clock In
   - Clock Out
   - Lunch Break
   - Add Time Log
   - Logout
3. [Admin Functions](#admin-functions)
   - Create Employees
   - View Employees
   - Export Time Logs
   - Restore Database Backup
   - Logout
4. [Keyboard Shortcuts](#keyboard-shortcuts)
5. [Exported Excel Files](#exported-excel-files)
6. [Troubleshooting](#troubleshooting)

---

## Login

1. Open the app (`timeclock.py`).
2. Enter your **username** and **PIN**.
3. Press **Submit** or hit **Enter**.
4. Depending on your role:
   - **Admin**: Redirected to the Admin Dashboard.
   - **Employee**: Redirected to the Employee Dashboard.

**Notes:**
- PINs are securely hashed using `bcrypt`.
- First-time use will require you to set an **Admin PIN**.

---

## Employee Functions

### Clock In

- Click **Clock In** to log your start time.
- If you forget to clock out on a previous day, the app will prompt you to select a missing clock-out time before allowing a new clock-in.

### Clock Out

- Click **Clock Out** to log your end time.
- Cannot clock out if no active clock-in exists.
- Cannot clock out for previous days without entering missing shift times.

### Lunch Break

- Click **Lunch Break** to log a break during your shift.
- A dropdown menu will appear allowing you to select the break duration: 10, 15, 20, 25, or 30 minutes.
- You can add multiple lunch breaks for a single shift if needed.
- Breaks are subtracted automatically from your total worked hours for accurate payroll and overtime calculation.
- Must be clocked in to log a lunch break.

### Add Time Log

- Opens a form to manually add future or past time logs for payroll purposes.

### Logout

- Click **Logout** to return to the login screen.
- Your session will end and all data will be saved automatically.

---

## Admin Functions

### Create Employees

1. Click **Create Employees**.
2. Fill in **Username** and **PIN**.
3. Click **Create**.
4. New employees are automatically saved to the database.
5. You cannot create duplicate usernames.

### View Employees

- Shows a list of all employees (excluding `DEVELOPER_ADMIN`) with ID, username, and role.
- **Double-click** a user to:
  - Delete the user.
  - Update their PIN.

### Export Time Logs

1. Click **Export Time Logs**.
2. Select **Start Date** and **End Date**.
3. Click **Export to Excel**.
4. The app will generate an Excel file containing:
   - **Totals Sheet:** Total hours worked per employee.
   - **Audit Log Sheet:** Daily shifts, with **manual override/adjusted shifts highlighted in red** and **lunch breaks shown as `X Lunch break`**.

### Restore Database Backup

1. Click **Restore Backup**.
2. Select a backup file from the `backups` folder.
3. Confirm the restore. This **overwrites the current database**.

### Logout

- Click **Logout** to return to the login screen.
- Menu bar and admin session end.

---

## Admin Notes on Lunch Breaks

- Lunch breaks are recorded per employee per shift.
- Breaks are automatically subtracted from the shift hours when exporting time logs, ensuring overtime is calculated correctly.
- In the **Audit Log** sheet of the exported Excel file, lunch breaks are displayed as `X Lunch break`, where `X` is the total minutes of the break.

---

## Keyboard Shortcuts

- **Enter**: Submit login credentials.
- **Double-click**: Edit a user in the View Employees frame.

---

## Exported Excel Files

- Uses `OpenPyXL` for Excel export.
- Two sheets:
  - **Totals:** Employee total hours.
  - **Audit Log:** Daily clock-in and clock-out times.
- **Red cells** indicate manual overrides (e.g., missed clock-outs).

---

## Troubleshooting

- **App does not start:** Make sure `timeclock.db` exists or let the app create it on first run.
- **Image not found:** The logo file `resources/logo.png` is missing. The app will still run.
- **PIN issues:** PINs must be entered correctly; they are hashed.
- **Database errors:** The admin can restore a previous backup.

---

## Additional Notes

- All backups are stored in the `backups` folder.
- Old backups are automatically cleaned to keep a maximum of 500 backups.
- First-time setup requires an **Admin PIN**.
- The menu bar is only available for **admin users**.

---

## Author

**Jacob Reilly**  
[GitHub Repository](https://github.com/jaker821/timeclock-app)
