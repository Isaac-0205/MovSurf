import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movsurf.settings')
django.setup()

from django.contrib.auth.models import User

# Create a superuser
User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
