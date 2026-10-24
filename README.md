# 📋 To-Do List Manager

A complete desktop To-Do List application built with **Python 3**, **Tkinter**, and **MySQL 8.0+**.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

---

## ✨ Features

- **Add Tasks** — title, description, priority (Low / Medium / High), optional due date.
- **View Tasks** — scrollable table showing ID, title, priority, status, due date, created date.
- **Update Tasks** — edit any field including status (Pending / In Progress / Completed).
- **Delete Tasks** — with confirmation dialog.
- **Search** — find tasks by title keyword.
- **Filter** — by status, priority, or both.
- **Dashboard** — live counts of Total, Pending, In Progress, Completed, and Overdue tasks.
- **Persistent Storage** — all data is saved in MySQL and survives application restarts.

---

## 📁 Project Structure

```
todo_list/
├── app.py              # Tkinter GUI and event handling
├── database.py         # MySQL connection and DB initialization
├── task_manager.py     # CRUD operations, validation, search, filter, dashboard
├── requirements.txt    # Python package dependencies
├── .env                # MySQL credentials (do NOT commit)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🛠️ Prerequisites

Make sure the following are installed on your system:

| Tool               | Version   | Download Link                                         |
|---------------------|-----------|-------------------------------------------------------|
| Python              | 3.8+      | https://www.python.org/downloads/                     |
| MySQL Server        | 8.0+      | https://dev.mysql.com/downloads/mysql/                |
| MySQL Workbench     | Latest    | https://dev.mysql.com/downloads/workbench/            |
| VS Code             | Latest    | https://code.visualstudio.com/                        |

Verify installations:

```bash
python --version
mysql --version
```

---

## 🚀 Setup Instructions

### Step 1 — Clone or Create the Project Folder

Place the `todo_list/` folder on your Desktop (or anywhere you prefer).

### Step 2 — Create a Virtual Environment

Open a terminal inside the `todo_list/` folder:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Step 3 — Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 4 — Configure MySQL Credentials

Open the `.env` file and replace the placeholder with your actual MySQL password:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=YourActualPassword
MYSQL_DATABASE=todo_db
```

> **Note:** The application will create the `todo_db` database and `tasks` table automatically on first run. You do **not** need to run any SQL manually.

### Step 5 — (Optional) Create the Database Manually

If you prefer to create the database yourself using MySQL Workbench, run this SQL script:

```sql
CREATE DATABASE IF NOT EXISTS todo_db;

USE todo_db;

CREATE TABLE IF NOT EXISTS tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(150) NOT NULL,
    description TEXT,
    priority    VARCHAR(20) DEFAULT 'Medium',
    status      VARCHAR(20) DEFAULT 'Pending',
    due_date    DATE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Step 6 — Run the Application

Make sure your virtual environment is active, then:

```bash
python app.py
```

The application window will open and you can start managing your tasks!

---

## 📖 How to Use

1. **Add a Task** — Fill in the Title (required), Description, Priority, and Due Date. Click **➕ Add**.
2. **View / Select a Task** — Click any row in the table to load its details into the form.
3. **Update a Task** — Select a task, modify the form fields, and click **✏️ Update**.
4. **Complete a Task** — Select a task and click **✅ Complete** to set its status to Completed.
5. **Delete a Task** — Select a task and click **🗑️ Delete**. Confirm the deletion in the popup.
6. **Search** — Type a keyword in the search box and press Enter or click **Search**.
7. **Filter** — Use the Status and Priority dropdowns. Tasks filter automatically.
8. **Show All** — Click **Show All** to reset all filters and display every task.
9. **Clear Form** — Click **🔄 Clear** to reset the form fields.

---

## ❗ Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Can't connect to MySQL server` | MySQL Server is not running | Start the MySQL service from Windows Services or System Preferences |
| `Access denied for user 'root'` | Wrong password in `.env` | Update `MYSQL_PASSWORD` in `.env` with the correct password |
| `No module named 'mysql.connector'` | Package not installed | Run `pip install mysql-connector-python` |
| `No module named 'tkcalendar'` | Package not installed | Run `pip install tkcalendar` |
| `No module named 'dotenv'` | Package not installed | Run `pip install python-dotenv` |
| `_tkinter.TclError: no display` | Running on a headless server | This is a desktop app — run it on a machine with a display |

---

## 🔒 Security Notes

- Database credentials are stored in `.env` which is excluded from Git via `.gitignore`.
- All SQL queries use **parameterized statements** to prevent SQL injection.
- Never hard-code passwords in source files.

---

## 📄 License

This project is for educational purposes. Feel free to use and modify it.
