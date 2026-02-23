import uuid
from django.db import models

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Department(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="departments")

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "departments"
        ordering = ["-created_at"]  # optional but recommended

    def __str__(self):
        return self.name
