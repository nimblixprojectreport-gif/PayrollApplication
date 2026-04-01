import MySQLdb
import sys

try:
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS payroll_db")
    print("Database 'payroll_db' created or already exists.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    if 'db' in locals():
        db.close()
