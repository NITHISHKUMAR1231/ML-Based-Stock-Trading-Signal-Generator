import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("stocks.db") #connection string
cursor = conn.cursor()

# Drop table if exists (optional, to recreate fresh)
cursor.execute("DROP TABLE IF EXISTS stocks")

# Create table without P&L
cursor.execute("""
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date REAL not null
    name TEXT NOT NULL,
    average_price REAL NOT NULL,
    closing_price REAL NOT NULL
)
""")

# Insert minimum 10 records
stocks_data = [
    ("TATA", 450.0, 470.0),
    ("RELIANCE", 2500.0, 2550.0),
    ("INFY", 1400.0, 1380.0),
    ("HDFCBANK", 1600.0, 1650.0),
    ("ICICIBANK", 900.0, 880.0),
    ("SBIN", 600.0, 620.0),
    ("WIPRO", 400.0, 420.0),
    ("LT", 2200.0, 2250.0),
    ("BAJFINANCE", 7000.0, 7100.0),
    ("ADANIPORTS", 800.0, 780.0)
]

cursor.executemany("""
INSERT INTO stocks (name, average_price, closing_price)
VALUES (?, ?, ?) 
""", stocks_data)


conn.commit()
cursor.execute("SELECT * FROM stocks")
rows = cursor.fetchall()

print("\n📊 Stock Records:\n")

for row in rows:
    print(row)

conn = sqlite3.connect("stocks.db")

df = pd.read_sql_query("SELECT * FROM stocks", conn)

df["P&L"] = df["closing_price"] - df["average_price"]

df.to_csv("stocks.csv", index=False)
conn.close()
print("✅ Exported using pandas")
print("Database created successfully with 10 records!")
