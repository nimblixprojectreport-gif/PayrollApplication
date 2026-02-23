from apps.employees.models import Employee
from apps.leave_management.models import LeaveType

print('--- EMPLOYEES ---')
for e in Employee.objects.all()[:3]:
    print(f'Employee ID: {e.id} | Name: {e.first_name} {e.last_name}')

print('\n--- LEAVE TYPES ---')
for lt in LeaveType.objects.all()[:3]:
    print(f'Leave Type ID: {lt.id} | Name: {lt.name}')
