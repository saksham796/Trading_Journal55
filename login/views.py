from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.utils import OperationalError


@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Do not store password; require unlock separately
                request.session.pop('unlock_pwd', None)
                return redirect('journal:unlock')
            messages.error(request, 'Invalid username or password')
        except OperationalError as e:
            # Likely missing migrations (e.g., no such table: auth_user)
            if 'no such table' in str(e).lower() and 'auth_user' in str(e).lower():
                messages.error(request, 'Initial setup required: run "python manage.py migrate" in the Trading_Journal directory, then try again.')
            else:
                messages.error(request, f'Database error: {e}')
    return render(request, 'login/page.html')


def logout(request):
    request.session.pop('unlock_pwd', None)
    auth_logout(request)
    return redirect('login:login')


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Auto-login after successful signup
                auth_login(request, user)
                request.session.pop('unlock_pwd', None)
                messages.success(request, 'Account created successfully. Please unlock your session to use the journal.')
                return redirect('journal:unlock')
            except OperationalError as e:
                if 'no such table' in str(e).lower() and 'auth_user' in str(e).lower():
                    messages.error(request, 'Initial setup required: run "python manage.py migrate" in the Trading_Journal directory, then try again.')
                else:
                    messages.error(request, f'Database error: {e}')
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', { 'form': form })