from django.contrib import admin
from .models import (
    Payroll, PayrollItem, PayrollItemComponent, 
    PayrollFormula, Payslip, SalaryStructure, 
    SalaryStructureComponent, EmployeeSalaryStructure
)

@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')

@admin.register(SalaryStructureComponent)
class SalaryStructureComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'salary_structure', 'component_type', 'amount')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'company', 'status', 'total_net', 'locked')
    list_filter = ('status', 'locked', 'year', 'month')

@admin.register(PayrollItem)
class PayrollItemAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll', 'gross_salary', 'net_salary', 'is_paid')
    list_filter = ('is_paid',)

@admin.register(PayrollItemComponent)
class PayrollItemComponentAdmin(admin.ModelAdmin):
    list_display = ('payroll_item', 'component_name', 'component_type', 'amount')

@admin.register(PayrollFormula)
class PayrollFormulaAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')

@admin.register(EmployeeSalaryStructure)
class EmployeeSalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary_structure', 'base_salary')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('payslip_number', 'payroll_item', 'generated_at')
