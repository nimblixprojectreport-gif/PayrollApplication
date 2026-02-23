from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'company', 'is_active', 'created_at')
    list_filter = ('company', 'is_active')
    search_fields = ('username', 'email', 'mobile')
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_login')
