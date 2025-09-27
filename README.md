# Time Clock App

A desktop based application used to track employees hours with a simple "clock in," "clock out" feature.


---


## Features
- Employee Login with username and PIN
- Clock in and clock out, capturing exact times
- Admin acount, handles employees
- Automatic calculation of hours worked
- Data stored locally in a database (SQLite)
- Input validation and error handling
- Easily export data from a certain pay period range.


---


## Tech Stack
- **Python 3**
- **Tkinter** (desktop UI)
- **SQLite3** (local database)
- **OpenPyXL** (Exported Spreadsheet)
- (Optional) Google Sheets API for backup and syncing data


---


## Upcoming Fixes

1. Lunch breaks
2. Add enter key bindings to multiple frames
3. Application packaged into a .exe file
4. General UI tweaks and fixes
   

---


## Changelog

### v3.0 Overtime Calculation
 - Added - Calculating Semi-Monthly Overtime
 - Updated - help.md file for admin

### v2.7 Future Time Entries
 - Added - User can now add future shifts in case payroll is needed to be calculated a few days before.
 - Enter buttons and key bindings are no longer global
 - Enter button function added for Adding time logs

### v2.6 DB Backups
 - Added - Backups are stored for the database whenever a user quits the program.

 - Added - Admin can restore the database to a previous backup if data is lost.

### v2.5 Missing Clock Outs

 - Added - If employee forgets to clock out, the app will prompt them for that date and store it in the database. As well as a flag for it being overridden

 - Added - A highlighted cell feature to the audit log, that way the admin can see which dates were manually adjusted (i.e. missed clock out)

 - Fixed - Issue where a missing database file would cause the app to not run.
 

### v2.4 Excel and Audit Table
 - Changed - File now exports using openpyxl.

 - Added - Audit table to see each day and time worked for employees.
 
### v2.3 Employee Time Calculated
 - Added - Ability to calculate the employee time

 - Added - Admin can now export data to a spreadsheet.

 - FIXED - After creating a user in Admin view, it doesnt show up on the View Employees page unless you restart app.

### v2.1.1 Bug Fix
 - Resolved a bug that occured when navigating the admin frames using the menu buttons.

### v2.1 Menu Feature added, small UX tweaks
- Updated help link to point to help.md file.

- Tweaked button placement, sizes, and labels for better UX. Updated title font sizes for better visibility.

- Improved Enter key handling for login.


### v2.0 - Hashing PINs - (Bcrypt)
- Added hashing for user pins.

- Added the ability to set an admin PIN when the app is run for the first time.

- Added username listing on the employee frame to make sure users are on the right account.


### v1.4 - DataBase Tie in - (SQLite3)
- Added feature that allows clock in and clock out and stores in the database.


---


## Project Structure
```plaintext
timeclock-app/
|---|timeclock.py       # Main Application
|---|db/                # Database Files
    |---|timeclock.db
|---|requirements.txt   # Dependecies
|---|.gitignore
|---|README.md
```


---


### Clone the repository
```plaintext
git clone https://github.com/jaker821/timeclock-app/tree/main
cd timeclock-app
```

### Create and activate a virtual environment
```plaintext
python -m venv venv
venv\Scripts\activate
```

### Install dependencies
```plaintext
pip install -r requirements.txt
```

### Run the app
```plaintext
python timeclock.py
```


---


# Author
**Jacob Reilly**
