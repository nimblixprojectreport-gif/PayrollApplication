from django.db import models
import uuid

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField()
    user_id = models.UUIDField()
    module_name = models.CharField(max_length=150)
    action = models.CharField(max_length=150)
    record_id = models.UUIDField(null=True, blank=True)
    old_data = models.TextField(null=True, blank=True)
    new_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module_name} - {self.action} at {self.created_at}"
