import sqlite3

connection = sqlite3.connect(
    "repairs.db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS assessments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reference TEXT,

    repair_type TEXT,

    priority TEXT,

    trade TEXT,

    attendance TEXT,

    message TEXT
)
""")

connection.commit()

connection.close()

print("Database created.")