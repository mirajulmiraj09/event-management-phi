

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from users.forms import CustomRegistrationForm


# ---------------------------
# SIGN UP VIEW
# ---------------------------
def sign_up(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Assign default "Participant" group
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


# ---------------------------
# SIGN IN VIEW
# ---------------------------
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect by role/group
            if user.is_superuser:
                return redirect('admin-dashboard')
            elif user.groups.filter(name='Organizer').exists():
                return redirect('organizer-dashboard')
            elif user.groups.filter(name='Participant').exists():
                return redirect('participant-dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/sign_in.html')


# ---------------------------
# SIGN OUT VIEW
# ---------------------------
def sign_out(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
