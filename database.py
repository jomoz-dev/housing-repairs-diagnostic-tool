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

    message TEXT,

    assessment_date TEXT
)
""")

try:
    cursor.execute(
        "ALTER TABLE assessments ADD COLUMN assessment_date TEXT"
    )
except sqlite3.OperationalError:
    pass

connection.commit()

connection.close()

print("Database created.")