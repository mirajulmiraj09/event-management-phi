from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from users.forms import CustomRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


# ---------------------------
# SIGN UP VIEW
# ---------------------------
def sign_up(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            # Assign default "Participant" group
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            messages.success(request, "A Confirmation mail sent. Please check your email")
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


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
