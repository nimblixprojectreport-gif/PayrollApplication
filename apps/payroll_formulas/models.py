import uuid
from django.db import models
from apps.companies.models import Company
from apps.employees.models import Employee


class SalaryStructure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='salary_structures')

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salary_structures'
        unique_together = [('company', 'name')]

    def __str__(self):
        return self.name


class SalaryStructureVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='versions')

    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salary_structure_versions'

    def __str__(self):
        return f"{self.salary_structure.name} v{self.effective_from}"


class SalaryComponent(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('Earning', 'Earning'),
        ('Deduction', 'Deduction'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='salary_components')

    name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPE_CHOICES)

    is_taxable = models.BooleanField(default=False)
    is_pf_applicable = models.BooleanField(default=False)
    is_esi_applicable = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salary_components'
        unique_together = [('company', 'name')]

    def __str__(self):
        return f"{self.name} ({self.component_type})"


class PayrollFormula(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_formulas')

    name = models.CharField(max_length=150)
    formula_expression = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payroll_formulas'

    def __str__(self):
        return self.name


class SalaryStructureComponentMapping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salary_structure_version = models.ForeignKey(SalaryStructureVersion, on_delete=models.CASCADE, related_name='component_mappings')
    salary_component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE, related_name='structure_mappings')
    formula = models.ForeignKey(PayrollFormula, on_delete=models.SET_NULL, null=True, blank=True, related_name='component_mappings')

    calculation_type = models.CharField(max_length=50, default='Fixed')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salary_structure_component_mappings'

    def __str__(self):
        return f"{self.salary_structure_version} → {self.salary_component.name}"


class EmployeeSalary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_assignments')
    salary_structure_version = models.ForeignKey(SalaryStructureVersion, on_delete=models.CASCADE, related_name='employee_salaries')

    effective_from = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employee_salaries'

    def __str__(self):
        return f"{self.employee} - {self.salary_structure_version}"
