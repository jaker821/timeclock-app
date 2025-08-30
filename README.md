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
1. Adding calculation of hours for employees over set date range
2. Adding EXPORT button to admin page. Export to a .csv file
3. Handling user error (forgetting to clock in, or missing days)
4. Feature for admin to update PINS for users
5. Add a FILE and HELP dropdown (contains guide for app, and logout, createuser, and view users page)
   

---


## Changelog

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
