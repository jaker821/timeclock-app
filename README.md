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
- (Optional) Google Sheets API for backup and syncing data


---


## Upcoming Fixes

1. Handling user error (forgetting to clock in, or missing days)
2. Data backups
3. Application packaged into a .exe file
4. General UI tweaks and fixes
   

---


## Changelog

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
