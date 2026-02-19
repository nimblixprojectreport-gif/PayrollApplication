from django.db import models
import uuid
from django.db import models


class SalaryComponent(models.Model):

    COMPONENT_TYPES = (
        ('EARNING', 'EARNING'),
        ('DEDUCTION', 'DEDUCTION'),
        ('CONTRIBUTION', 'CONTRIBUTION'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField()
    name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)

    is_taxable = models.BooleanField(default=False)
    is_pf_applicable = models.BooleanField(default=False)
    is_esi_applicable = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company_id', 'name')

    def __str__(self):
        return self.name


class SalaryStructure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField()
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SalaryStructureVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    salary_structure = models.ForeignKey(
        SalaryStructure,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class SalaryStructureComponent(models.Model):

    CALCULATION_TYPES = (
        ('FIXED', 'FIXED'),
        ('PERCENTAGE', 'PERCENTAGE'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    salary_structure_version = models.ForeignKey(
        SalaryStructureVersion,
        on_delete=models.CASCADE,
        related_name="components"
    )

    salary_component = models.ForeignKey(
        SalaryComponent,
        on_delete=models.CASCADE
    )

    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES)
    value = models.DecimalField(max_digits=12, decimal_places=2)


# Create your models here.
