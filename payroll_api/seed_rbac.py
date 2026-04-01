import os
import django
import uuid

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import sys
sys.path.append('d:\\pay\\PayrollApplication')
django.setup()

from apps.user.models import User, Role, Permission, UserRole, RolePermission
from apps.companies.models import Company

def seed_data():
    print("Seeding data...")

    # 1. Create Superadmin (Platform Level)
    if not User.objects.filter(username='superadmin').exists():
        User.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='admin123'
        )
        print("Superadmin created.")

    # 2. Create Permissions
    permissions_data = [
        ('Company', 'view_company', 'Can view company details'),
        ('Company', 'edit_company', 'Can edit company details'),
        ('Employee', 'manage_employees', 'Can manage all employees'),
        ('Payroll', 'process_payroll', 'Can process payroll'),
        ('Salary', 'manage_salary', 'Can manage salary structures'),
        ('Attendance', 'manage_attendance', 'Can manage attendance'),
    ]

    permission_objs = {}
    for module, code, desc in permissions_data:
        perm, created = Permission.objects.get_or_create(
            module=module,
            code=code,
            defaults={'description': desc}
        )
        permission_objs[code] = perm
        if created:
            print(f"Permission created: {code}")

    # 3. Create a Test Company
    company, created = Company.objects.get_or_create(
        name="Tech Corp",
        defaults={
            'email': 'contact@techcorp.com',
            'registration_number': 'REG123456'
        }
    )
    if created:
        print("Company 'Tech Corp' created.")

    # 4. Create Roles for the Company
    # Company Admin Role (All Permissions)
    comp_admin_role, created = Role.objects.get_or_create(
        company=company,
        name="Company Admin",
        defaults={'description': 'Full access to company modules'}
    )
    if created:
        for perm in permission_objs.values():
            RolePermission.objects.create(role=comp_admin_role, permission=perm)
        print("Company Admin role created and permissions assigned.")

    # HR Admin Role (Employee, Payroll, Salary)
    hr_role, created = Role.objects.get_or_create(
        company=company,
        name="HR Admin",
        defaults={'description': 'Management of employees, salary, and payroll'}
    )
    if created:
        hr_perms = ['manage_employees', 'process_payroll', 'manage_salary']
        for code in hr_perms:
            RolePermission.objects.create(role=hr_role, permission=permission_objs[code])
        print("HR Admin role created and permissions assigned.")

    # 5. Create Users
    # Company Admin User
    if not User.objects.filter(username='tech_admin').exists():
        admin_user = User.objects.create_user(
            username='tech_admin',
            email='admin@techcorp.com',
            password='password123',
            company=company,
            is_staff=True # Allow access to django admin
        )
        UserRole.objects.create(user=admin_user, role=comp_admin_role)
        print("Company Admin user created.")

    # HR Admin User
    if not User.objects.filter(username='tech_hr').exists():
        hr_user = User.objects.create_user(
            username='tech_hr',
            email='hr@techcorp.com',
            password='password123',
            company=company,
            is_staff=True # Allow access to django admin
        )
        UserRole.objects.create(user=hr_user, role=hr_role)
        print("HR Admin user created.")

if __name__ == "__main__":
    seed_data()
