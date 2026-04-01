"""
Payroll App Settings
====================
Centralized configuration for the payroll module.
Import these constants in models, serializers, and views instead of
hard-coding values.

Usage:
    from apps.payroll.settings import PAYROLL_SETTINGS
    status_draft = PAYROLL_SETTINGS['STATUS_DRAFT']
"""

# ──────────────────────────────────────────────
#  Payroll Status Choices
# ──────────────────────────────────────────────
PAYROLL_STATUS_DRAFT = 'Draft'
PAYROLL_STATUS_GENERATED = 'Generated'
PAYROLL_STATUS_FINALIZED = 'Finalized'
PAYROLL_STATUS_LOCKED = 'Locked'
PAYROLL_STATUS_PAID = 'Paid'

PAYROLL_STATUS_CHOICES = (
    (PAYROLL_STATUS_DRAFT, 'Draft'),
    (PAYROLL_STATUS_GENERATED, 'Generated'),
    (PAYROLL_STATUS_FINALIZED, 'Finalized'),
    (PAYROLL_STATUS_LOCKED, 'Locked'),
    (PAYROLL_STATUS_PAID, 'Paid'),
)

# ──────────────────────────────────────────────
#  Payroll Component Types
# ──────────────────────────────────────────────
COMPONENT_TYPE_EARNING = 'Earning'
COMPONENT_TYPE_DEDUCTION = 'Deduction'

COMPONENT_TYPE_CHOICES = (
    (COMPONENT_TYPE_EARNING, 'Earning'),
    (COMPONENT_TYPE_DEDUCTION, 'Deduction'),
)

# ──────────────────────────────────────────────
#  Tax & Compliance Settings
# ──────────────────────────────────────────────
DEFAULT_PF_RATE = 12.0          # Employee PF contribution rate (%)
DEFAULT_PF_EMPLOYER_RATE = 12.0 # Employer PF contribution rate (%)
DEFAULT_ESI_RATE = 0.75         # Employee ESI contribution rate (%)
DEFAULT_ESI_EMPLOYER_RATE = 3.25 # Employer ESI contribution rate (%)

# ──────────────────────────────────────────────
#  Payroll Cycle Defaults
# ──────────────────────────────────────────────
DEFAULT_PAYROLL_CYCLE = 'Monthly'
PAYROLL_CYCLE_CHOICES = (
    ('Monthly', 'Monthly'),
    ('Fortnightly', 'Fortnightly'),
    ('Weekly', 'Weekly'),
)

# ──────────────────────────────────────────────
#  Payslip Configuration
# ──────────────────────────────────────────────
PAYSLIP_PREFIX = 'PS-'
ALLOW_PAYSLIP_DOWNLOAD_AFTER_FINAL_ONLY = True
INCLUDE_COMPANY_LOGO_IN_PAYSLIP = True

# ──────────────────────────────────────────────
#  Pagination & API Defaults
# ──────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ──────────────────────────────────────────────
#  Aggregated Settings Dictionary
# ──────────────────────────────────────────────
PAYROLL_SETTINGS = {
    # Status
    'STATUS_DRAFT': PAYROLL_STATUS_DRAFT,
    'STATUS_GENERATED': PAYROLL_STATUS_GENERATED,
    'STATUS_FINALIZED': PAYROLL_STATUS_FINALIZED,
    'STATUS_LOCKED': PAYROLL_STATUS_LOCKED,
    'STATUS_PAID': PAYROLL_STATUS_PAID,
    'STATUS_CHOICES': PAYROLL_STATUS_CHOICES,

    # Component Types
    'COMPONENT_TYPE_EARNING': COMPONENT_TYPE_EARNING,
    'COMPONENT_TYPE_DEDUCTION': COMPONENT_TYPE_DEDUCTION,
    'COMPONENT_TYPE_CHOICES': COMPONENT_TYPE_CHOICES,

    # Compliance
    'DEFAULT_PF_RATE': DEFAULT_PF_RATE,
    'DEFAULT_ESI_RATE': DEFAULT_ESI_RATE,

    # Cycles
    'DEFAULT_PAYROLL_CYCLE': DEFAULT_PAYROLL_CYCLE,
    'PAYROLL_CYCLE_CHOICES': PAYROLL_CYCLE_CHOICES,

    # Payslip
    'PAYSLIP_PREFIX': PAYSLIP_PREFIX,
    'ALLOW_PAYSLIP_DOWNLOAD_AFTER_FINAL_ONLY': ALLOW_PAYSLIP_DOWNLOAD_AFTER_FINAL_ONLY,

    # API
    'DEFAULT_PAGE_SIZE': DEFAULT_PAGE_SIZE,
    'MAX_PAGE_SIZE': MAX_PAGE_SIZE,
}
