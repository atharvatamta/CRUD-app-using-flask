# 🗂️ ONGC Digital Backup Register System

This project digitizes ONGC's current physical register system used to log data backups. It provides a web-based interface for secure login, role-based access, and management of backup records — streamlining the process of tracking backup activities, eliminating the need for manual registers.

---

## 🚀 Features

### 👤 Authentication
- Secure login for admins and users
- Passwords hashed using bcrypt
- Session-based login using Flask-Login

### 🧑‍💼 Admin Functionality
- Add new backup entries
- Delete existing entries
- Search/filter records by date, username, group name, details, or tape number

### 👥 User Functionality
- View all backup entries
- Search/filter entries (read-only access)

---

## 🧾 Data Fields

Each backup entry includes:

- 📅 **Date of Entry**
- 🙍 **Username**
- 🏢 **Group Name**
- 📝 **Details about the Entry**
- 💽 **Tape Number**

---

## 🛠️ Tech Stack

| Layer        | Technology         |
|--------------|--------------------|
| Frontend     | HTML, CSS, JavaScript, Bootstrap |
| Backend      | Python, Flask       |
| Authentication | Flask-Login, bcrypt |
| Database     | SQLite             |

---

## 📁 Project Structure
ongc_register/
├── app.py # Main Flask application
├── database.db # SQLite database file
├── templates/ # HTML templates
│ ├── base.html
│ ├── login.html
│ ├── admin_dashboard.html
│ └── user_dashboard.html
├── static/ # Static assets (CSS, JS)
│ └── style.css
└── README.md # This file

---

## ⚙️ Setup Instructions
**Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ongc-register.git
   cd ongc-register






