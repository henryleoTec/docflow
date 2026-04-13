# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # AbstractUser already gives you:
    # username, email, password, first_name, last_name
    # is_staff, is_active, date_joined, last_login

    # We add extra fields useful for a SaaS app
    bio = models.TextField(blank=True)
    # blank=True means this field is optional in forms
    # (it's never truly empty in DB — just an empty string "")

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    # null=True means the database column can store NULL (no image at all)
    # blank=True means it's optional in forms
    # Together they mean: "this field is completely optional"

    email_verified = models.BooleanField(default=False)
    # We'll flip this to True after user clicks verification link

    def __str__(self):
        return self.username
