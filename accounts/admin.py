# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Add our custom fields to the admin panel display
    model = CustomUser
    list_display = ["username", "email", "email_verified", "is_staff"]
    # list_display controls which columns show in the admin user list

    # Add our custom fields to the edit form in admin
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("bio", "avatar", "email_verified")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
