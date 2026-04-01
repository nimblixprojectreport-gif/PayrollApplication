"""
User App Settings
=================
Centralized configuration for the user module.
Import these constants in models, serializers, and views instead of
hard-coding values.

Usage:
    from apps.user.settings import USER_SETTINGS
    min_pass = USER_SETTINGS['MIN_PASSWORD_LENGTH']
"""

# ──────────────────────────────────────────────
#  User Roles / Types
# ──────────────────────────────────────────────
ROLE_ADMIN = 'Admin'
ROLE_MANAGER = 'Manager'
ROLE_EMPLOYEE = 'Employee'
ROLE_HR = 'HR'

ROLE_CHOICES = (
    (ROLE_ADMIN, 'Administrator'),
    (ROLE_MANAGER, 'Manager'),
    (ROLE_EMPLOYEE, 'Employee'),
    (ROLE_HR, 'Human Resources'),
)

# ──────────────────────────────────────────────
#  Password & Security Settings
# ──────────────────────────────────────────────
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
REQUIRE_SPECIAL_CHAR = True
REQUIRE_NUMBERS = True
REQUIRE_UPPER_CASE = True

# Account Lockout Settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30

# ──────────────────────────────────────────────
#  Account Status Choices
# ──────────────────────────────────────────────
STATUS_ACTIVE = 'Active'
STATUS_INACTIVE = 'Inactive'
STATUS_SUSPENDED = 'Suspended'
STATUS_PENDING = 'Pending'

STATUS_CHOICES = (
    (STATUS_ACTIVE, 'Active'),
    (STATUS_INACTIVE, 'Inactive'),
    (STATUS_SUSPENDED, 'Suspended'),
    (STATUS_PENDING, 'Pending_Verification'),
)

# ──────────────────────────────────────────────
#  Session & Token Settings
# ──────────────────────────────────────────────
# JWT / Token Expiry (if using external auth)
ACCESS_TOKEN_LIFETIME_MINUTES = 60
REFRESH_TOKEN_LIFETIME_DAYS = 7

# ──────────────────────────────────────────────
#  Pagination & API Defaults
# ──────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ──────────────────────────────────────────────
#  Aggregated Settings Dictionary
# ──────────────────────────────────────────────
USER_SETTINGS = {
    # Roles
    'ROLE_ADMIN': ROLE_ADMIN,
    'ROLE_MANAGER': ROLE_MANAGER,
    'ROLE_EMPLOYEE': ROLE_EMPLOYEE,
    'ROLE_HR': ROLE_HR,
    'ROLE_CHOICES': ROLE_CHOICES,

    # Security
    'MIN_PASSWORD_LENGTH': MIN_PASSWORD_LENGTH,
    'MAX_PASSWORD_LENGTH': MAX_PASSWORD_LENGTH,
    'REQUIRE_SPECIAL_CHAR': REQUIRE_SPECIAL_CHAR,
    'REQUIRE_NUMBERS': REQUIRE_NUMBERS,
    'REQUIRE_UPPER_CASE': REQUIRE_UPPER_CASE,
    'MAX_LOGIN_ATTEMPTS': MAX_LOGIN_ATTEMPTS,
    'LOCKOUT_DURATION_MINUTES': LOCKOUT_DURATION_MINUTES,

    # Status
    'STATUS_ACTIVE': STATUS_ACTIVE,
    'STATUS_INACTIVE': STATUS_INACTIVE,
    'STATUS_SUSPENDED': STATUS_SUSPENDED,
    'STATUS_PENDING': STATUS_PENDING,
    'STATUS_CHOICES': STATUS_CHOICES,

    # Tokens
    'ACCESS_TOKEN_LIFETIME_MINUTES': ACCESS_TOKEN_LIFETIME_MINUTES,
    'REFRESH_TOKEN_LIFETIME_DAYS': REFRESH_TOKEN_LIFETIME_DAYS,

    # API
    'DEFAULT_PAGE_SIZE': DEFAULT_PAGE_SIZE,
    'MAX_PAGE_SIZE': MAX_PAGE_SIZE,
}
