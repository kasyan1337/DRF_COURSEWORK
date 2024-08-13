import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")
django.setup()

# pytest_plugins = [
#     'django_db_setup',
# ]
