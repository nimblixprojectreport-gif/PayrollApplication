from django.db import models
from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.employees.models import Employee


class Shift(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "shifts"


class Attendance(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    date = models.DateField()

    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)

    class Meta:
        db_table = "attendance"
