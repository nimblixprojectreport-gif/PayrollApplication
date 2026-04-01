from django.db import models

import uuid
from django.db import models
from django.core.exceptions import ValidationError


class SalaryStructure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "salary_structures"
        unique_together = ("company_id", "name")  # optional but common

    def __str__(self):
        return f"{self.name}"


class SalaryStructureVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salary_structure = models.ForeignKey(
        SalaryStructure,
        on_delete=models.CASCADE,
        related_name="versions",
        db_column="salary_structure_id",
    )
    effective_from = models.DateField()
    effective_to = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "salary_structure_versions"
        ordering = ["-effective_from"]

    def clean(self):
        # effective_to should be >= effective_from if provided
        if self.effective_to and self.effective_to < self.effective_from:
            raise ValidationError("effective_to cannot be before effective_from.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class SalaryComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=150)
    component_type = models.CharField(max_length=50)  # e.g. EARNING / DEDUCTION
    is_taxable = models.BooleanField(default=False)
    is_pf_applicable = models.BooleanField(default=False)
    is_esi_applicable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "salary_components"
        unique_together = ("company_id", "name")  # optional but common

    def __str__(self):
        return self.name


class PayrollFormula(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=150)
    formula_expression = models.TextField()  # store expression text
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payroll_formulas"
        unique_together = ("company_id", "name")  # optional but common

    def __str__(self):
        return self.name

# Create your models here.
import uuid
from django.db import models
from django.core.exceptions import ValidationError


class SalaryStructureComponentMapping(models.Model):
    CALC_TYPES = (
        ("FIXED", "FIXED"),          # use value
        ("PERCENT", "PERCENT"),      # value is percent
        ("FORMULA", "FORMULA"),      # use formula_id
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    salary_structure_version = models.ForeignKey(
        "SalaryStructureVersion",
        on_delete=models.CASCADE,
        related_name="component_mappings",
        db_column="salary_structure_version_id",
    )

    salary_component = models.ForeignKey(
        "SalaryComponent",
        on_delete=models.CASCADE,
        related_name="structure_mappings",
        db_column="salary_component_id",
    )

    formula = models.ForeignKey(
        "PayrollFormula",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="structure_mappings",
        db_column="formula_id",
    )

    calculation_type = models.CharField(max_length=50, choices=CALC_TYPES)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "salary_structure_component_mappings"
        ordering = ["display_order", "created_at"]
        # Prevent duplicates for same version+component
        unique_together = ("salary_structure_version", "salary_component")

    def clean(self):
        # Validation logic based on calculation_type
        if self.calculation_type == "FORMULA":
            if not self.formula:
                raise ValidationError("formula is required when calculation_type is FORMULA.")
            # value can be null for formula type (optional)
        else:
            # FIXED or PERCENT
            if self.value is None:
                raise ValidationError("value is required when calculation_type is FIXED or PERCENT.")
            if self.formula is not None:
                raise ValidationError("formula must be null unless calculation_type is FORMULA.")

            if self.calculation_type == "PERCENT":
                # common validation (0 to 100)
                if self.value < 0 or self.value > 100:
                    raise ValidationError("For PERCENT, value must be between 0 and 100.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)