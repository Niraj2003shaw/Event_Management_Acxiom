# Event Mangement Project Acxiom# 🎉 Event Management System

A web-based Event Management System developed using **Python Flask** and **SQLite**.  
This system allows Admin and Users to manage events, memberships, transactions, and view reports.

---

## 🚀 Features

### 🔐 Authentication
- Login system with session management
- Role-based access control (Admin & User)
- Password field hidden
- Registration with duplicate username check

---

### 🛠 Maintenance Module (Admin Only)
- Add Events
- Add Memberships
- Update Membership (Extend / Cancel)
- Delete Membership
- Radio button selection for membership duration (default 6 months)
- All fields mandatory validation

---

### 💳 Transactions Module
- Add transactions
- Select event from dropdown
- Store transaction amount
- Accessible by both Admin and User

---

### 📊 Reports Module
- View all events
- View total transactions
- View total revenue (SUM function)
- Data fetched dynamically from database

---

## 🗄 Database Used

SQLite database with following tables:

- `users`
- `events`
- `membership`
- `transactions`

---

## 🛠 Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2 Templates

---

## 🔑 Default Login Credentials

Admin:
Username: admin
Password: admin

User
Username: user
Password: user

event_management/
│
├── app.py
├── database.db
├── templates/
│ ├── login.html
│ ├── dashboard.html
│ ├── maintenance.html
│ ├── transaction.html
│ ├── report.html
│ └── register.html
│
└── static/
└── style.css

## ▶️ How to Run the Project

1. Clone the repository:


2. Navigate into the folder:


3. Create virtual environment:


4. Install dependencies:


5. Run the application:

6. Open browser:
http://127.0.0.1:5000


