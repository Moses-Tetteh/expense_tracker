"""
Settings package for expense_tracker project.
Import appropriate settings based on DJANGO_SETTINGS_MODULE environment variable.
"""
import os

# Determine which settings module to use
environment = os.getenv('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .production import *
elif environment == 'staging':
    from .staging import *
else:
    from .development import *
