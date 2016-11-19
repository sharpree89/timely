from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager
from django.contrib import messages
from django.core.urlresolvers import reverse

def login_home(request):

    return render(request, 'login_app/login.html')

def register_home(request):

    return render(request, 'login_app/register.html')

def register(request):
    if request.method == 'POST':
        user = User.objects.register(request.POST)
    if user[0]:
        request.session['user_id'] = user[1].id
        request.session['username'] = user[1].username

        return redirect(reverse ('appts:appts'))

    for error in user[1]:
            messages.error(request, error)

    return redirect(reverse ('login:register_home'))

def login(request):
    user = User.objects.login(request.POST)
    if user[0]:
        request.session['user_id'] = user[1].id
        request.session['username'] = user[1].username

        return redirect(reverse ('appts:appts'))

    for error in user[1]:
        messages.error(request, error)

    return redirect(reverse ('login:login_home'))

# def success(request):
#     return render(request, 'login_app/success.html')
