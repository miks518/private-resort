import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)

try:
    send_mail(
        subject="Test Exception",
        message="Test message",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print("Success")
except Exception as e:
    print("Exception caught:", e)
