from fastapi import FastAPI
import sqlite3
import os

# Create and set the app server
app = FastAPI(title="Math Microservice with SQLite")
DB_PATH = "operations.db"

# THis methods sets the connection to the database of the app
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# THis method initiates the creation of the table of the operations
def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                input TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

#This method will insert and save the data of operations in the table
def save_operation(operation: str, input_data: str, result: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO operations (operation, input, result) VALUES (?, ?, ?)",
        (operation, input_data, result)
    )
    conn.commit()
    conn.close()