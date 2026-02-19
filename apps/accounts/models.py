from django.db import models
from apps.core.models import BaseModel
from apps.companies.models import Company


class User(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="users"
    )

    username = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)

    password_hash = models.TextField()

    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["email"]),
        ]


class Role(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="roles"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    is_system_role = models.BooleanField(default=False)

    class Meta:
        db_table = "roles"


class Permission(BaseModel):

    module = models.CharField(max_length=150)
    code = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    class Meta:
        db_table = "permissions"


class RolePermission(BaseModel):

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "role_permissions"


class UserRole(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_roles"

