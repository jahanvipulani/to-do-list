"""
task_manager.py — CRUD Operations, Search, Filter, and Dashboard Stats

This module contains all business logic for managing tasks:
- Add, view, update, delete tasks
- Search tasks by title
- Filter tasks by status and/or priority
- Calculate dashboard statistics
- Input validation
"""

from datetime import date, datetime
from database import get_connection, close_connection
from mysql.connector import Error


# ──────────────────────────────────────────────
#  Validation Helpers
# ──────────────────────────────────────────────

VALID_PRIORITIES = ("Low", "Medium", "High")
VALID_STATUSES = ("Pending", "In Progress", "Completed")


def validate_title(title):
    """
    Check that a task title is not empty or whitespace-only.

    Returns:
        (bool, str): (True, cleaned_title) or (False, error_message)
    """
    if not title or not title.strip():
        return False, "Task title cannot be empty."
    if len(title.strip()) > 150:
        return False, "Task title must be 150 characters or fewer."
    return True, title.strip()


def validate_priority(priority):
    """Ensure priority is one of the allowed values."""
    if priority not in VALID_PRIORITIES:
        return False, f"Priority must be one of: {', '.join(VALID_PRIORITIES)}."
    return True, priority


def validate_status(status):
    """Ensure status is one of the allowed values."""
    if status not in VALID_STATUSES:
        return False, f"Status must be one of: {', '.join(VALID_STATUSES)}."
    return True, status


def validate_due_date(due_date_str):
    """
    Validate and parse a due-date string (YYYY-MM-DD).
    An empty string means no due date (returns None).

    Returns:
        (bool, date | None | str)
    """
    if not due_date_str or not due_date_str.strip():
        return True, None  # due date is optional
    try:
        parsed = datetime.strptime(due_date_str.strip(), "%Y-%m-%d").date()
        return True, parsed
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


# ──────────────────────────────────────────────
#  CREATE
# ──────────────────────────────────────────────

def add_task(title, description="", priority="Medium", due_date_str=""):
    """
    Insert a new task into the database.

    Args:
        title (str): Task title (required).
        description (str): Task description (optional).
        priority (str): 'Low', 'Medium', or 'High'.
        due_date_str (str): Due date as 'YYYY-MM-DD' or empty string.

    Returns:
        (bool, str): (success, message)
    """
    # Validate inputs
    ok, result = validate_title(title)
    if not ok:
        return False, result
    title = result

    ok, result = validate_priority(priority)
    if not ok:
        return False, result

    ok, result = validate_due_date(due_date_str)
    if not ok:
        return False, result
    due_date = result

    # Insert into database
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO tasks (title, description, priority, due_date)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, description, priority, due_date))
        connection.commit()
        task_id = cursor.lastrowid
        cursor.close()
        return True, f"Task '{title}' added successfully (ID: {task_id})."
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


# ──────────────────────────────────────────────
#  READ
# ──────────────────────────────────────────────

def get_all_tasks():
    """
    Retrieve all tasks, ordered by creation date (newest first).

    Returns:
        (bool, list[dict] | str)
    """
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        cursor.close()
        return True, tasks
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


def get_task_by_id(task_id):
    """
    Retrieve a single task by its ID.

    Returns:
        (bool, dict | str)
    """
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        if task:
            return True, task
        return False, f"No task found with ID {task_id}."
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


# ──────────────────────────────────────────────
#  UPDATE
# ──────────────────────────────────────────────

def update_task(task_id, title, description="", priority="Medium",
                status="Pending", due_date_str=""):
    """
    Update an existing task.

    Returns:
        (bool, str)
    """
    # Validate
    ok, result = validate_title(title)
    if not ok:
        return False, result
    title = result

    ok, result = validate_priority(priority)
    if not ok:
        return False, result

    ok, result = validate_status(status)
    if not ok:
        return False, result

    ok, result = validate_due_date(due_date_str)
    if not ok:
        return False, result
    due_date = result

    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor()
        query = """
            UPDATE tasks
            SET title = %s, description = %s, priority = %s,
                status = %s, due_date = %s
            WHERE id = %s
        """
        cursor.execute(query, (title, description, priority,
                               status, due_date, task_id))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"No task found with ID {task_id}."
        cursor.close()
        return True, f"Task '{title}' updated successfully."
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


# ──────────────────────────────────────────────
#  DELETE
# ──────────────────────────────────────────────

def delete_task(task_id):
    """
    Delete a task by its ID.

    Returns:
        (bool, str)
    """
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"No task found with ID {task_id}."
        cursor.close()
        return True, "Task deleted successfully."
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


# ──────────────────────────────────────────────
#  SEARCH & FILTER
# ──────────────────────────────────────────────

def search_tasks(keyword):
    """
    Search tasks whose title contains the given keyword (case-insensitive).

    Returns:
        (bool, list[dict] | str)
    """
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE title LIKE %s ORDER BY created_at DESC"
        cursor.execute(query, (f"%{keyword}%",))
        tasks = cursor.fetchall()
        cursor.close()
        return True, tasks
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


def filter_tasks(status=None, priority=None):
    """
    Filter tasks by status and/or priority.
    Pass None (or 'All') to skip a filter.

    Returns:
        (bool, list[dict] | str)
    """
    connection = get_connection()
    if not connection:
        return False, "Could not connect to the database."

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status and status != "All":
            query += " AND status = %s"
            params.append(status)
        if priority and priority != "All":
            query += " AND priority = %s"
            params.append(priority)

        query += " ORDER BY created_at DESC"
        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
        cursor.close()
        return True, tasks
    except Error as e:
        return False, f"Database error: {e}"
    finally:
        close_connection(connection)


# ──────────────────────────────────────────────
#  DASHBOARD STATISTICS
# ──────────────────────────────────────────────

def get_dashboard_stats():
    """
    Calculate summary statistics for the dashboard.

    Returns:
        dict with keys: total, pending, in_progress, completed, overdue
    """
    stats = {
        "total": 0,
        "pending": 0,
        "in_progress": 0,
        "completed": 0,
        "overdue": 0,
    }

    connection = get_connection()
    if not connection:
        return stats

    try:
        cursor = connection.cursor(dictionary=True)

        # Total tasks
        cursor.execute("SELECT COUNT(*) AS count FROM tasks")
        stats["total"] = cursor.fetchone()["count"]

        # Pending tasks
        cursor.execute("SELECT COUNT(*) AS count FROM tasks WHERE status = 'Pending'")
        stats["pending"] = cursor.fetchone()["count"]

        # In Progress tasks
        cursor.execute("SELECT COUNT(*) AS count FROM tasks WHERE status = 'In Progress'")
        stats["in_progress"] = cursor.fetchone()["count"]

        # Completed tasks
        cursor.execute("SELECT COUNT(*) AS count FROM tasks WHERE status = 'Completed'")
        stats["completed"] = cursor.fetchone()["count"]

        # Overdue tasks: due_date is in the past AND status is NOT 'Completed'
        cursor.execute(
            "SELECT COUNT(*) AS count FROM tasks "
            "WHERE due_date < CURDATE() AND status != 'Completed'"
        )
        stats["overdue"] = cursor.fetchone()["count"]

        cursor.close()
    except Error as e:
        print(f"[Dashboard Error] {e}")
    finally:
        close_connection(connection)

    return stats
