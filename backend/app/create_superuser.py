import os
import django

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# from django.contrib.auth.models import User
from accounts.models import MyUser as User

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpassword")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password, is_verified=True, is_paid=True, payment_plan="premium")
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")
