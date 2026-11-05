import sqlite3

connection = sqlite3.connect("lab.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("DELETE FROM users")
cursor.executemany(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    [
        ("alice", "alice@example.test"),
        ("bob", "bob@example.test"),
        ("charlie", "charlie@example.test"),
    ],
)

connection.commit()
connection.close()
print("Lab database created with synthetic users.")
