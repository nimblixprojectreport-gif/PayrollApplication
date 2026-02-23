import uuid
from django.db import models
from companies.models import Company

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.CharField(max_length=20)
    password_hash = models.TextField()
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.company.name})"

    class Meta:
        db_table = 'users'
