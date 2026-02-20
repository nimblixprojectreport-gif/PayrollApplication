import uuid
from django.db import models

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100)
    pan_number = models.CharField(max_length=20)
    tan_number = models.CharField(max_length=20)
    pf_number = models.CharField(max_length=50)
    esi_number = models.CharField(max_length=50)
    professional_tax_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    timezone = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class CompanySettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='settings')
    financial_year_start_month = models.IntegerField(default=4)
    payroll_cycle = models.CharField(max_length=50, default='Monthly')
    pf_enabled = models.BooleanField(default=False)
    esi_enabled = models.BooleanField(default=False)
    professional_tax_enabled = models.BooleanField(default=False)
    tds_enabled = models.BooleanField(default=False)
    attendance_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_settings'
        verbose_name_plural = 'Company Settings'

    def __str__(self):
        return f"Settings for {self.company.name}"
