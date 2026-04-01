from django.contrib import admin
from .models import User, Role, Permission, RolePermission, UserRole


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'company', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'company']
    search_fields = ['username', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_system_role', 'created_at']
    list_filter = ['company', 'is_system_role']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['module', 'code', 'description']
    list_filter = ['module']
    search_fields = ['module', 'code']
    readonly_fields = ['id']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']
    list_filter = ['role']
    readonly_fields = ['id']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    readonly_fields = ['id']
