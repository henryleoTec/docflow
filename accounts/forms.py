# accounts/forms.py  (create this file)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    # UserCreationForm is Django's built-in form that handles:
    # username, password1, password2 (confirm password)
    # and all the password validation rules automatically

    # We add the email field ourselves because we need it
    # required=True means the form won't submit without it
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser      # use our custom user, not Django's default
        fields = [
            "username",
            "email",
            "password1",   # password
            "password2",   # confirm password
        ]
        # UserCreationForm handles password matching validation automatically

    def save(self, commit=True):
        # Override save() to store the email before saving
        # commit=False means "prepare the user object but don't write to DB yet"
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # cleaned_data is a dictionary of validated form values
        # Django runs validation (required fields, email format etc.) first
        # then stores results in cleaned_data — always use this, never raw POST data

        if commit:
            user.save()  # now actually write to the database
        return user
