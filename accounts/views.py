from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import SignUpForm, LoginForm

"""
This module contains views for user authentication including signup and login.
It handles user registration, authentication, and displays appropriate success or error messages.
"""

def signup_view(request):
    """
    Handle user signup.

    This view processes the signup form. If the form is valid, it creates a new user and logs them in.
    Success and error messages are displayed accordingly.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered signup template.
    """
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'You have registered successfully!')
                return redirect('home')
        else:
            form = SignUpForm()
    except ValidationError as e:
        pass
    except Exception as e:
        pass

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """
    Handle user login.

    This view processes the login form. If the credentials are valid, it authenticates and logs the user in.
    Success and error messages are displayed accordingly.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered login template.
    """
    try:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    if user.is_superuser:
                        return redirect('super_home')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = LoginForm()
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'login.html', {'form': form})
