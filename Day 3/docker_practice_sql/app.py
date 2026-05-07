import psycopg2

conn = psycopg2.connect(
    host = 'localhost',
    port = 5432,
    database = 'my_db',
    user = 'postgres',
    password = 'password'
)

cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS customers (
               id   SERIAL PRIMARY KEY,
               name VARCHAR(100),
               email    VARCHAR(100),
               age INTEGER,
               signup_date DATE
               )
               """)

cursor.execute("""
                INSERT INTO customers (name, email, age, signup_date)
               VALUES (%s, %s, %s, %s)
"""), ('John Smith', 'john@email.com', 30, '2024-01-01')

conn.commit()

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()