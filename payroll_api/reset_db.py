import MySQLdb
import sys

try:
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root")
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS payroll_db")
    cursor.execute("CREATE DATABASE payroll_db")
    print("Database 'payroll_db' reset successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    if 'db' in locals():
        db.close()
