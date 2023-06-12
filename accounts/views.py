from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm

def login_user(request):
    if request.method != 'POST':
        if request.user.is_authenticated:
            return redirect('blogs:index')
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                #next_page = request.META.get('QUERY_STRING').split('=')[1]
                next_page = request.POST.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('blogs:topics')
    context = {
        'next': request.GET.get('next', ''),
        'form': form,
    }
    return render(request, 'registration/login.html', context)

def logout_user(request):
    if request.method != 'POST':
        return redirect('blogs:index')
    logout(request)
    return redirect('accounts:login')

def register(request):
    if request.method != 'POST':
        form = SignUpForm()
    else:
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in
            login(request, new_user)
            return redirect('blogs:index')
    return render(request, 'registration/register.html', {'form': form})