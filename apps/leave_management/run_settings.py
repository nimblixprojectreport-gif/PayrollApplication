import os
import sys
from pathlib import Path

# Import original settings
try:
    from payroll_feb.settings import *
except ImportError:
    # If we are running from within leave_management
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from payroll_feb.settings import *

# Fix sys.path first to allow both 'apps.x' and 'x' imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

from payroll_feb.settings import *

# Fix INSTALLED_APPS to use top-level names to match the imports in user/models.py
# This prevents 'RuntimeError: Model class ... doesn't declare an explicit app_label'
NEW_INSTALLED_APPS = []
for app in INSTALLED_APPS:
    if app.startswith('apps.'):
        # Convert 'apps.leave_management' to 'leave_management'
        NEW_INSTALLED_APPS.append(app.split('.')[-1])
    else:
        NEW_INSTALLED_APPS.append(app)

INSTALLED_APPS = NEW_INSTALLED_APPS

# Handle other broken apps if necessary
# For example, if 'user' has a name='users' mismatch, we can fix it here?
# Actually, if we use top-level 'user', Django will look for 'user/apps.py'
# and find 'UsersConfig' with name='users'.mismatch again!
# So we also need to exclude 'user' if it's still broken, or fix its config in memory.

# Since we can't touch user/apps.py, let's just exclude 'user' for now to get leave_management running
INSTALLED_APPS = [app for app in NEW_INSTALLED_APPS if app not in ['user', 'apps.user']]

# Isolate URLs to only leave_management to avoid broken imports in other apps' urls.py
ROOT_URLCONF = 'apps.leave_management.urls'


