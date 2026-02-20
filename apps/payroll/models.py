from django.db import models
import uuid
from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.employees.models import Employee

class SalaryStructure(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "salary_structures"

class SalaryStructureComponent(BaseModel):
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name="components")
    name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=50) # Earning, Deduction
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    formula = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = "salary_structure_components"

class Payroll(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_employees = models.IntegerField(default=0)
    total_gross = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_net = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default='Draft')
    generated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="generated_payrolls")
    generated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)

    class Meta:
        db_table = "payrolls"

class PayrollItem(BaseModel):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name="items")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    working_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    leave_days = models.IntegerField(default=0)
    lop_days = models.IntegerField(default=0)
    payable_days = models.IntegerField(default=0)
    gross_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "payroll_items"

class PayrollItemComponent(BaseModel):
    payroll_item = models.ForeignKey(PayrollItem, on_delete=models.CASCADE, related_name="components")
    component_name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=50) # Earning, Deduction
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = "payroll_item_components"

class PayrollFormula(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    formula_expression = models.TextField()

    class Meta:
        db_table = "payroll_formulas"

class EmployeeSalaryStructure(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="salary_structure")
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = "employee_salary_structures"

class Payslip(BaseModel):
    payroll_item = models.OneToOneField(PayrollItem, on_delete=models.CASCADE, related_name="payslip")
    payslip_number = models.CharField(max_length=150, null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "payslips"
