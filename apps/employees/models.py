from django.db import models
from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.accounts.models import User
from apps.organization.models import Department, Designation


class Employee(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee"
    )

    employee_code = models.CharField(max_length=100)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    email = models.EmailField()
    mobile = models.CharField(max_length=20)

    date_of_birth = models.DateField(null=True, blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True
    )

    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True
    )

    reporting_manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    joining_date = models.DateField()
    exit_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "employees"


class EmployeeDocument(BaseModel):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(max_length=100)

    file_path = models.CharField(max_length=500)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "employee_documents"
