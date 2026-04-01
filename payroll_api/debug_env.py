import sys
import os

print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("sys.path:", sys.path)

try:
    import django
    from django.conf import settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from django.apps import apps
    for app in apps.get_app_configs():
        print(f"App: {app.label}, Name: {app.name}, Path: {app.path}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
