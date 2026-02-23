from django.db import models
import uuid

class LeaveType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='leave_types')
    name = models.CharField(max_length=150)
    yearly_quota = models.IntegerField()
    carry_forward_allowed = models.BooleanField(default=False)
    max_carry_forward = models.IntegerField(default=0)
    is_paid_leave = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leave_types'
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='leave_requests', db_column='employee_id')
    leave_type_id = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_requests', db_column='leave_type_id')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leave_requests'

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1  # Inclusive
        super().save(*args, **kwargs)

class LeaveBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='leave_balances', db_column='employee_id')
    leave_type_id = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_balances', db_column='leave_type_id')
    year = models.IntegerField()
    allocated = models.IntegerField()
    used = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)

    class Meta:
        db_table = 'leave_balances'
        unique_together = ('employee_id', 'leave_type_id', 'year')

    def save(self, *args, **kwargs):
        self.remaining = self.allocated - self.used
        super().save(*args, **kwargs)
