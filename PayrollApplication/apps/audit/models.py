from django.db import models
from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.accounts.models import User


class AuditLog(BaseModel):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    module_name = models.CharField(max_length=150)

    action = models.CharField(max_length=150)

    record_id = models.UUIDField()

    old_data = models.JSONField(null=True)
    new_data = models.JSONField(null=True)

    class Meta:
        db_table = "audit_logs"
