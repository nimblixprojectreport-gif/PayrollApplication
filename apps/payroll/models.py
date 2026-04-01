import uuid
from django.db import models
from apps.companies.models import Company
from apps.employees.models import Employee
from apps.user.models import User

class Payroll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payrolls')
    
    month = models.IntegerField()
    year = models.IntegerField()
    
    total_employees = models.IntegerField(default=0)
    total_gross = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(max_length=50, default='Draft') # Draft, Processed, Finalized, Locked
    
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_payrolls')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    finalized_at = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)

    class Meta:
        db_table = 'payrolls'
        unique_together = [('company', 'month', 'year')]

    def __str__(self):
        return f"Payroll {self.month}/{self.year} - {self.company.name}"

class PayrollItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='items')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_items')
    
    working_days = models.IntegerField()
    present_days = models.IntegerField()
    leave_days = models.IntegerField()
    lop_days = models.IntegerField()
    payable_days = models.IntegerField()
    
    gross_salary = models.DecimalField(max_digits=15, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2)
    net_salary = models.DecimalField(max_digits=15, decimal_places=2)
    
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'payroll_items'
        unique_together = [('payroll', 'employee')]

    def __str__(self):
        return f"{self.employee.first_name} - {self.payroll}"

class PayrollItemComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payroll_item = models.ForeignKey(PayrollItem, on_delete=models.CASCADE, related_name='components')
    
    component_name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=50) # Earning, Deduction
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'payroll_item_components'

    def __str__(self):
        return f"{self.component_name}: {self.amount}"

class Payslip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payroll_item = models.OneToOneField(PayrollItem, on_delete=models.CASCADE, related_name='payslip')
    
    payslip_number = models.CharField(max_length=150, unique=True)
    file_path = models.CharField(max_length=500, blank=True)
    
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payslips'

    def __str__(self):
        return f"Payslip {self.payslip_number}"
