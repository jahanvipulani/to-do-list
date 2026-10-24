"""
database.py — MySQL Connection and Database Initialization

This module handles:
- Loading MySQL credentials from the .env file
- Creating and returning database connections
- Initializing the 'todo_db' database and 'tasks' table
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read MySQL credentials from environment variables
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "todo_db")


def get_connection():
    """
    Create and return a MySQL connection to the 'todo_db' database.

    Returns:
        mysql.connector.connection.MySQLConnection or None
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"[Database Error] Could not connect to MySQL: {e}")
        return None


def close_connection(connection):
    """
    Safely close a MySQL connection.

    Args:
        connection: A MySQL connection object.
    """
    if connection and connection.is_connected():
        connection.close()


def initialize_database():
    """
    Create the 'todo_db' database and the 'tasks' table if they don't exist.

    This function connects to MySQL without specifying a database first,
    creates the database, then creates the tasks table inside it.

    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    try:
        # Step 1: Connect to MySQL server (no database selected)
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Step 2: Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        print(f"[Database] Database '{DB_NAME}' is ready.")

        # Step 3: Switch to the database
        cursor.execute(f"USE `{DB_NAME}`")

        # Step 4: Create the tasks table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            title       VARCHAR(150) NOT NULL,
            description TEXT,
            priority    VARCHAR(20) DEFAULT 'Medium',
            status      VARCHAR(20) DEFAULT 'Pending',
            due_date    DATE,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("[Database] Table 'tasks' is ready.")

        cursor.close()
        close_connection(connection)
        return True

    except Error as e:
        print(f"[Database Error] Initialization failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Auto-initialize when this module is first imported
# ---------------------------------------------------------------------------
if not initialize_database():
    print(
        "\n[FATAL] Could not initialize the database.\n"
        "Please check:\n"
        "  1. MySQL Server is running.\n"
        "  2. The credentials in your .env file are correct.\n"
        "  3. The MySQL user has permission to create databases.\n"
    )
