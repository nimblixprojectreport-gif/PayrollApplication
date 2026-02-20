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
