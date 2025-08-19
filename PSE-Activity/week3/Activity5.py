import sqlite3

connection = sqlite3.connect("sample.db")
db_cursor = connection.cursor()

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
""")

db_cursor.execute("SELECT COUNT(*) FROM Users")
users_count = db_cursor.fetchone()[0]
if users_count == 0:
    db_cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
    db_cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    Stu_ID INTEGER PRIMARY KEY,
    Stu_name TEXT,
    Stu_address TEXT
)
""")

db_cursor.execute("""
INSERT INTO Students (Stu_ID, Stu_name, Stu_address)
VALUES (?, ?, ?)
ON CONFLICT(Stu_ID) DO UPDATE SET
    Stu_name=excluded.Stu_name,
    Stu_address=excluded.Stu_address;
""", (1, "Alice", "123 Main St"))

db_cursor.execute("""
INSERT INTO Students (Stu_ID, Stu_name, Stu_address)
VALUES (?, ?, ?)
ON CONFLICT(Stu_ID) DO UPDATE SET
    Stu_name=excluded.Stu_name,
    Stu_address=excluded.Stu_address;
""", (2, "Bob", "456 Oak Ave"))

connection.commit()

print("Users Table:")
db_cursor.execute("SELECT * FROM Users")
for row in db_cursor.fetchall():
    print(row)

print("\nStudents Table:")
db_cursor.execute("SELECT * FROM Students")
for row in db_cursor.fetchall():
    print(row)

connection.close()
