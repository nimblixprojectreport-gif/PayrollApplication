from django.contrib import admin
from .models import Company, CompanySettings

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_name', 'registration_number', 'email', 'is_active', 'created_at')
    search_fields = ('name', 'legal_name', 'registration_number', 'email')
    list_filter = ('is_active', 'state', 'country')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('company', 'payroll_cycle', 'pf_enabled', 'esi_enabled', 'created_at')
    search_fields = ('company__name',)
    list_filter = ('payroll_cycle', 'pf_enabled', 'esi_enabled')
    readonly_fields = ('id', 'created_at')
