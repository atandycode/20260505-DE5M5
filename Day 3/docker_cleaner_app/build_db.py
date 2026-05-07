import sqlite3
import os

def create_database():

    conn = sqlite3.connect('/app/data/cleaned_books.db')
    # print(f"Data directory contents: {os.listdir('/app/data')}")
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                Title    TEXT,
                Checkout    TEXT,
                Returned    TEXT,
                Week_Allowance INTEGER,
                Cust_ID  INTEGER,
                Book_Checkout_Days    INTEGER
                )
            """)

    # print(f"Data directory after creation: {os.listdir('/app/data')}")
    conn.commit()
    conn.close()

    print("Database and tables created successfully")