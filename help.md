# 🕒 TimeClock App - Admin Help Guide

Welcome to the **TimeClock App (Admin Panel)**.  
This guide explains the features available to administrators.  

---

## 📋 Features for Admins

### 1. **Create New User**
- Navigate to the **"Create User"** page.  
- Enter the following:
  - **Username** (must be unique).  
  - **PIN** (numeric code the employee uses to log in).  
  - **Role** (choose **employee** or **admin**).  
- Click **"Create User"** to save them to the system.  
- A success message will confirm the new user was added.

---

### 2. **View All Users**
- Navigate to the **"View Users"** page.  
- A list of all users will be shown in a table.  
- The table includes:
  - **User ID**  
  - **Username**  
  - **Role**  
- ⚠️ At this stage, you **cannot edit or delete** users from this view (read-only).

---

### 3. **Clock In / Clock Out (Employees Only)**
- Employees log in using their **username** and **PIN**.  
- They can press **Clock In** or **Clock Out** from their dashboard.  
- Each action is recorded in the database and will later be used for reporting.  
- Admins do not clock in/out unless also acting as employees.

---

### 4. **Help Menu**
- This page (Help Guide) can always be accessed from the **Help Menu**.  
- It explains all admin functions in one place.  

---

## ⚙️ Future Features (Planned)
- Export reports of hours worked by employees for a custom date range.  
- Allow admin to reset or update a user’s PIN.  
- Logging system for error/debug tracking.  

---

## 📝 Notes
- Data is stored locally in the database file: **timeclock.db**.  
- Make regular backups of this file to ensure no data is lost.  
- Users’ PINs are currently stored in plain text. A future update will add **PIN hashing** for better security.

---

👤 **Admin Reminder:** Only admins can access the **Create User**, **View Users**, and **Help Menu** pages. Employees only see their personal dashboard.
