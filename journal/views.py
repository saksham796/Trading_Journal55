from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpRequest


@login_required
@csrf_protect
def unlock(request: HttpRequest):
    if request.method == 'POST':
        pwd = request.POST.get('password', '')
        if not pwd:
            messages.error(request, 'Password is required to unlock your data')
        else:
            # Store unlock password only in session for current browser session
            request.session['unlock_pwd'] = pwd
            request.session.modified = True
            return redirect('journal:dashboard')
    return render(request, 'journal/unlock.html')


@login_required
def dashboard(request: HttpRequest):
    # Client-side storage only; no server persistence or fetching
    unlock_pwd = request.session.get('unlock_pwd')
    return render(request, 'journal/dashboard.html', {
        'is_unlocked': bool(unlock_pwd),
    })


@login_required
@csrf_protect
def add_trade(request: HttpRequest):
    # Gate by unlock, but do not persist on the server
    if not request.session.get('unlock_pwd'):
        messages.error(request, 'Please unlock with your password first.')
        return redirect('journal:unlock')
    # The form submission is handled entirely in the browser via JavaScript
    return render(request, 'journal/add_trade.html')
