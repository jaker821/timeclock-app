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


## Project Structure
```plaintext
timeclock-app/
├── timeclock.py        # Main application
├── validators.py       # Input sanitization functions
├── db/                 # Database files
│   └── timeclock.db
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md
```

---


### Clone the repository
git clone https://github.com/jaker821/timeclock-app
cd timeclock-app

### Create and activate a virtual environment
python -m venv venv
ven\Scripts\activate

### Install Dependencies
pip install -r requirements.txt

### Run the app
python timeclock.py


---


# Author
Built by **Jacob Reilly**