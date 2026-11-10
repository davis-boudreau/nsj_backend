import os
import django
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cptn_api.settings")
django.setup()

from django.contrib.auth import get_user_model
# Ensure this matches your models.py class name exactly
from journey.models import CPTNUserProfile 

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not all([username, email, password]):
    print("⚠️ Skipping Superuser: missing env vars.")
    exit(0)

try:
    with transaction.atomic():
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )

        if created:
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"✅ Superuser '{username}' created.")
        else:
            print(f"ℹ️ Superuser '{username}' already exists.")

        # Match your CPTNUserProfile fields
        profile, p_created = CPTNUserProfile.objects.get_or_create(
            user=user,
            defaults={
                'is_driver': True,
                'is_rider': True,
                'default_seats': 4
            }
        )
        if p_created:
            print(f"✅ CPTNUserProfile created for '{username}'.")

except Exception as e:
    print(f"❌ Error in superuser script: {e}")
    exit(1)