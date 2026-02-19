from django.db import models
from apps.core.models import BaseModel


class Company(BaseModel):

    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)

    registration_number = models.CharField(max_length=100, unique=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    tan_number = models.CharField(max_length=20, blank=True, null=True)
    pf_number = models.CharField(max_length=50, blank=True, null=True)
    esi_number = models.CharField(max_length=50, blank=True, null=True)
    professional_tax_number = models.CharField(max_length=50, blank=True, null=True)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    timezone = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "companies"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]


class CompanySettings(BaseModel):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="settings"
    )

    financial_year_start_month = models.IntegerField()

    payroll_cycle = models.CharField(max_length=50)

    pf_enabled = models.BooleanField(default=True)
    esi_enabled = models.BooleanField(default=True)
    professional_tax_enabled = models.BooleanField(default=True)
    tds_enabled = models.BooleanField(default=True)

    attendance_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "company_settings"
