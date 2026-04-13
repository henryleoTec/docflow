# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        # User submitted the form
        form = RegisterForm(request.POST)

        if form.is_valid():
            # All fields passed validation — save the user
            user = form.save()

            # --- Send Welcome Email ---
            subject = "Welcome to DocFlow!"

            # render_to_string turns a template into a plain string
            # We pass the user object so the template can use {{ user.username }}
            body = render_to_string(
                "accounts/emails/welcome_email.html",
                {"user": user}
            )

            email = EmailMessage(
                subject,          # email subject line
                body,             # email body (our HTML template)
                to=[user.email]   # recipient — the new user's email
            )
            email.content_subtype = "html"
            # Tell the email client to render this as HTML
            # Without this, HTML tags show as raw text in the inbox

            email.send()
            # Actually sends the email via Gmail SMTP

            # --- Log the user in automatically after registering ---
            login(request, user)
            # login() creates a session for the user
            # After this, request.user is the logged-in user everywhere

            messages.success(request, "Account created! Welcome to DocFlow.")
            # messages is Django's flash message system
            # It stores a one-time message that shows on the next page
            # then disappears automatically

            return redirect("document-list")

    else:
        # GET request — user just visited the page, show empty form
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # AuthenticationForm is Django's built-in login form
        # It takes username + password and validates them against the database
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # get_user() returns the authenticated User object
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # next parameter: if user was redirected to login from another page,
            # send them back there after logging in
            next_url = request.GET.get("next", "document-list")
            return redirect(next_url)

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    # logout() destroys the session — user is now anonymous
    messages.info(request, "You've been logged out.")
    return redirect("login")
