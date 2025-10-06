import sqlite3

conn = sqlite3.connect("DB/all_users.db")
cursor = conn.cursor()

UID = 1

cursor.execute("SELECT * FROM users WHERE UID=?", (UID,))
row = cursor.fetchone()
print(row)
if row:
    print("User UID:", row[0])
else:
    print("No user found with that cookie.")
