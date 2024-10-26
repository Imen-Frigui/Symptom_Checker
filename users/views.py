from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from users.forms import SignUpForm
import logging
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            logger.warning(f"Signup form is invalid: {form.errors}")
            messages.error(request, f"There was an error with your signup: {form.errors}")
    else:
        form = SignUpForm()

    return render(request, 'back_office/pages/sign-up.html', {'form': form})

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile was updated successfully!')
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user)
    
#     return render(request, 'back_office/pages/profile.html', {'form': form})


@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was updated successfully!')
                return redirect('profile')

    return render(request, 'back_office/pages/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'back_office/pages/profile.html', {'profile_form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in after password change
            messages.success(request, 'Your password was updated successfully!')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'back_office/pages/change_password.html', {'password_form': password_form})