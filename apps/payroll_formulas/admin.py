from django.contrib import admin
from .models import SalaryStructure, SalaryStructureVersion, SalaryComponent, PayrollFormula, SalaryStructureComponentMapping, EmployeeSalary


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_active', 'created_at']
    list_filter = ['company', 'is_active']
    readonly_fields = ['id', 'created_at']


@admin.register(SalaryStructureVersion)
class SalaryStructureVersionAdmin(admin.ModelAdmin):
    list_display = ['salary_structure', 'effective_from', 'effective_to', 'created_at']
    list_filter = ['salary_structure']
    readonly_fields = ['id', 'created_at']


@admin.register(SalaryComponent)
class SalaryComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'component_type', 'is_taxable', 'is_active']
    list_filter = ['company', 'component_type', 'is_active']
    readonly_fields = ['id', 'created_at']


@admin.register(PayrollFormula)
class PayrollFormulaAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'created_at']
    list_filter = ['company']
    readonly_fields = ['id', 'created_at']


@admin.register(SalaryStructureComponentMapping)
class SalaryStructureComponentMappingAdmin(admin.ModelAdmin):
    list_display = ['salary_structure_version', 'salary_component', 'calculation_type', 'value']
    list_filter = ['calculation_type']
    readonly_fields = ['id', 'created_at']


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'salary_structure_version', 'effective_from']
    list_filter = ['effective_from']
    readonly_fields = ['id', 'created_at']
