from django.db import models
from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.employees.models import Employee


class SalaryStructure(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "salary_structures"


class Payroll(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()

    total_gross = models.DecimalField(max_digits=15, decimal_places=2)
    total_net = models.DecimalField(max_digits=15, decimal_places=2)

    status = models.CharField(max_length=50)

    locked = models.BooleanField(default=False)

    class Meta:
        db_table = "payrolls"


class PayrollItem(BaseModel):

    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.CASCADE,
        related_name="items"
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    gross_salary = models.DecimalField(max_digits=15, decimal_places=2)
    net_salary = models.DecimalField(max_digits=15, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = "payroll_items"
