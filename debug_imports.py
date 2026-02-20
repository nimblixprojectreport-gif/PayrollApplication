import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll_feb.settings')
django.setup()

from apps.employees.models import Employee
from apps.leave_management.models import LeaveType

print("Employee model imported successfully")
print("LeaveType model imported successfully")
