"""
Leave Management App Settings
==============================
Centralized configuration for the leave_management module.
Import these constants in models, serializers, and views instead of
hard-coding values.

Usage:
    from apps.leave_management.settings import LEAVE_SETTINGS
    max_days = LEAVE_SETTINGS['MAX_LEAVE_DAYS_PER_REQUEST']
"""

# ──────────────────────────────────────────────
#  Leave Request Status Choices
# ──────────────────────────────────────────────
LEAVE_STATUS_PENDING = 'Pending'
LEAVE_STATUS_APPROVED = 'Approved'
LEAVE_STATUS_REJECTED = 'Rejected'
LEAVE_STATUS_CANCELLED = 'Cancelled'

LEAVE_STATUS_CHOICES = (
    (LEAVE_STATUS_PENDING, 'Pending'),
    (LEAVE_STATUS_APPROVED, 'Approved'),
    (LEAVE_STATUS_REJECTED, 'Rejected'),
    (LEAVE_STATUS_CANCELLED, 'Cancelled'),
)

# Statuses that are considered "active" (count against balance)
ACTIVE_LEAVE_STATUSES = [LEAVE_STATUS_PENDING, LEAVE_STATUS_APPROVED]

# ──────────────────────────────────────────────
#  Leave Type Defaults
# ──────────────────────────────────────────────
DEFAULT_YEARLY_QUOTA = 12           # Default annual leave quota per employee
MAX_YEARLY_QUOTA = 365              # Upper bound for yearly quota validation
MIN_YEARLY_QUOTA = 0                # Lower bound for yearly quota

DEFAULT_CARRY_FORWARD_ALLOWED = False
DEFAULT_MAX_CARRY_FORWARD = 0       # Max days that can be carried forward
MAX_CARRY_FORWARD_LIMIT = 30        # Absolute upper limit for carry-forward

DEFAULT_IS_PAID_LEAVE = True

# ──────────────────────────────────────────────
#  Leave Request Rules
# ──────────────────────────────────────────────
MAX_LEAVE_DAYS_PER_REQUEST = 30     # Maximum days allowed in a single request
MIN_LEAVE_DAYS_PER_REQUEST = 0.5    # Minimum days (supports half-day leaves)
ALLOW_HALF_DAY_LEAVE = True         # Enable / disable half-day leave requests
ALLOW_BACKDATED_LEAVE = False       # Allow leave requests for past dates
MAX_BACKDATE_DAYS = 7               # How many days in the past a request can go
ALLOW_FUTURE_LEAVE = True           # Allow leave requests for future dates
MAX_ADVANCE_DAYS = 90               # How far ahead a leave can be requested

# ──────────────────────────────────────────────
#  Leave Balance Settings
# ──────────────────────────────────────────────
AUTO_ALLOCATE_ON_JOINING = True     # Auto-create balance records for new employees
PRO_RATE_ON_JOINING = True          # Pro-rate quota based on joining date
ALLOW_NEGATIVE_BALANCE = False      # Allow leave usage beyond allocated quota
MAX_NEGATIVE_BALANCE = 0            # Max negative balance if allowed (days)

# ──────────────────────────────────────────────
#  Carry-Forward Policy
# ──────────────────────────────────────────────
CARRY_FORWARD_EXPIRY_MONTHS = 3     # Carried-forward days expire after N months
CARRY_FORWARD_RESET_MONTH = 1      # Month (1-12) when carry-forward resets (Jan)

# ──────────────────────────────────────────────
#  Financial / Calendar Year
# ──────────────────────────────────────────────
LEAVE_YEAR_START_MONTH = 1          # Month when the leave year starts (1 = Jan)
LEAVE_YEAR_START_DAY = 1            # Day of the month when leave year starts

# ──────────────────────────────────────────────
#  Approval Workflow
# ──────────────────────────────────────────────
REQUIRE_APPROVAL = True             # Leaves require manager approval
AUTO_APPROVE_IF_BALANCE = False     # Auto-approve if employee has enough balance
APPROVAL_LEVELS = 1                 # Number of approval levels (1 = direct manager)
NOTIFY_ON_REQUEST = True            # Send notification when leave is requested
NOTIFY_ON_APPROVAL = True           # Send notification when leave is approved
NOTIFY_ON_REJECTION = True          # Send notification when leave is rejected

# ──────────────────────────────────────────────
#  Weekend & Holiday Configuration
# ──────────────────────────────────────────────
# Days of the week: 0 = Monday, 6 = Sunday
WEEKEND_DAYS = [5, 6]               # Saturday & Sunday
EXCLUDE_WEEKENDS = True             # Exclude weekends from leave day count
EXCLUDE_HOLIDAYS = True             # Exclude company holidays from leave day count

# ──────────────────────────────────────────────
#  Pagination & API Defaults
# ──────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 20              # Default records per page for list endpoints
MAX_PAGE_SIZE = 100                 # Maximum records per page

# ──────────────────────────────────────────────
#  Aggregated Settings Dictionary
#  (convenient single-import for views / services)
# ──────────────────────────────────────────────
LEAVE_SETTINGS = {
    # Status
    'STATUS_PENDING': LEAVE_STATUS_PENDING,
    'STATUS_APPROVED': LEAVE_STATUS_APPROVED,
    'STATUS_REJECTED': LEAVE_STATUS_REJECTED,
    'STATUS_CANCELLED': LEAVE_STATUS_CANCELLED,
    'STATUS_CHOICES': LEAVE_STATUS_CHOICES,
    'ACTIVE_LEAVE_STATUSES': ACTIVE_LEAVE_STATUSES,

    # Leave Type Defaults
    'DEFAULT_YEARLY_QUOTA': DEFAULT_YEARLY_QUOTA,
    'MAX_YEARLY_QUOTA': MAX_YEARLY_QUOTA,
    'MIN_YEARLY_QUOTA': MIN_YEARLY_QUOTA,
    'DEFAULT_CARRY_FORWARD_ALLOWED': DEFAULT_CARRY_FORWARD_ALLOWED,
    'DEFAULT_MAX_CARRY_FORWARD': DEFAULT_MAX_CARRY_FORWARD,
    'MAX_CARRY_FORWARD_LIMIT': MAX_CARRY_FORWARD_LIMIT,
    'DEFAULT_IS_PAID_LEAVE': DEFAULT_IS_PAID_LEAVE,

    # Leave Request Rules
    'MAX_LEAVE_DAYS_PER_REQUEST': MAX_LEAVE_DAYS_PER_REQUEST,
    'MIN_LEAVE_DAYS_PER_REQUEST': MIN_LEAVE_DAYS_PER_REQUEST,
    'ALLOW_HALF_DAY_LEAVE': ALLOW_HALF_DAY_LEAVE,
    'ALLOW_BACKDATED_LEAVE': ALLOW_BACKDATED_LEAVE,
    'MAX_BACKDATE_DAYS': MAX_BACKDATE_DAYS,
    'ALLOW_FUTURE_LEAVE': ALLOW_FUTURE_LEAVE,
    'MAX_ADVANCE_DAYS': MAX_ADVANCE_DAYS,

    # Leave Balance
    'AUTO_ALLOCATE_ON_JOINING': AUTO_ALLOCATE_ON_JOINING,
    'PRO_RATE_ON_JOINING': PRO_RATE_ON_JOINING,
    'ALLOW_NEGATIVE_BALANCE': ALLOW_NEGATIVE_BALANCE,
    'MAX_NEGATIVE_BALANCE': MAX_NEGATIVE_BALANCE,

    # Carry-Forward
    'CARRY_FORWARD_EXPIRY_MONTHS': CARRY_FORWARD_EXPIRY_MONTHS,
    'CARRY_FORWARD_RESET_MONTH': CARRY_FORWARD_RESET_MONTH,

    # Calendar
    'LEAVE_YEAR_START_MONTH': LEAVE_YEAR_START_MONTH,
    'LEAVE_YEAR_START_DAY': LEAVE_YEAR_START_DAY,

    # Approval
    'REQUIRE_APPROVAL': REQUIRE_APPROVAL,
    'AUTO_APPROVE_IF_BALANCE': AUTO_APPROVE_IF_BALANCE,
    'APPROVAL_LEVELS': APPROVAL_LEVELS,
    'NOTIFY_ON_REQUEST': NOTIFY_ON_REQUEST,
    'NOTIFY_ON_APPROVAL': NOTIFY_ON_APPROVAL,
    'NOTIFY_ON_REJECTION': NOTIFY_ON_REJECTION,

    # Weekends & Holidays
    'WEEKEND_DAYS': WEEKEND_DAYS,
    'EXCLUDE_WEEKENDS': EXCLUDE_WEEKENDS,
    'EXCLUDE_HOLIDAYS': EXCLUDE_HOLIDAYS,

    # Pagination
    'DEFAULT_PAGE_SIZE': DEFAULT_PAGE_SIZE,
    'MAX_PAGE_SIZE': MAX_PAGE_SIZE,
}
