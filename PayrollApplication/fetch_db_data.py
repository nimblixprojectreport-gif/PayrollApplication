import MySQLdb

try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="root",
        db="hrms_db"
    )
    cursor = db.cursor()

    print("--- COMPANIES ---")
    cursor.execute("SELECT id, name FROM companies LIMIT 3")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]}")

    print("\n--- EMPLOYEES ---")
    cursor.execute("SELECT id, first_name, last_name FROM employees LIMIT 3")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]} {row[2]}")

    print("\n--- LEAVE TYPES ---")
    cursor.execute("SELECT id, name FROM leave_types LIMIT 3")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]}")

    db.close()
except Exception as e:
    print(f"Error: {e}")
