import sqlite3
import pandas as pd

def save_to_database(df, table_name):
    conn = sqlite3.connect('/app/data/cleaned_books.db')

    df.to_sql(
        name = table_name,
        con = conn,
        if_exists='append',
        index=False
    )

    conn.close()

    print(f"Saved {len(df)} rows to {table_name}")