# accounts/urls.py  (create this file)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Password reset — Django handles ALL the logic for these 4 URLs
    # You only provide the templates, Django does the heavy lifting:
    # generating tokens, validating links, updating passwords

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset/password_reset_form.html",
            email_template_name="accounts/password_reset/password_reset_form.html",
        ),
        name="password_reset",
    ),
    # ↑ Shows the form where user enters their email

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # ↑ Shown after the reset email is sent

    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    # ↑ The link in the email points here
    # <uidb64> is the user's ID encoded in base64
    # <token> is a secure one-time token Django generates

    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # ↑ Shown after password is successfully changed
]
