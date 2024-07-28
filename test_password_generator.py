import os
import django
from django.contrib.auth.hashers import make_password

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')

# Configure Django
django.setup()

# Now Django settings are configured, you can use make_password
hashed_password = make_password('password123')
print(hashed_password)
