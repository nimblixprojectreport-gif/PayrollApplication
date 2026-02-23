from django.db import models
from core.models import BaseModel
from employees.models import Employee


class LeaveType(BaseModel):

    name = models.CharField(max_length=150)

    yearly_quota = models.IntegerField()

    class Meta:
        db_table = "leave_types"


class LeaveRequest(BaseModel):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=50)

    class Meta:
        db_table = "leave_requests"
