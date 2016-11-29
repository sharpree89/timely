from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import datetime
from . import models
from .models import Appt, ApptManager
from ..login_app.models import User, UserManager
from django.db.models import Q
from django.contrib import messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

#-------------------------------------------------------------------------------
# APPOINTMENT ROUTES

def login_home(request):

    return render(request, 'login_app/login.html')

def register_home(request):

    return render(request, 'login_app/register.html')

def appts(request):

    now = datetime.datetime.now()

    context = {
        'my_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_date__gte=now)
            ).exclude(my_status='Complete'
            ).order_by('my_date', 'my_time'),

        'today': now.strftime('%A, ' + '%B ' + '%d, ' + '%Y'),
        # 'appt': Appt.objects.all(),
        'right_now': datetime.datetime.now().time()

        # 'my_future_appts':
        #     Appt.objects.filter(
        #     Q(user__id=request.session['user_id']) &
        #     Q(my_date__gte=now)
        #     ).exclude(my_date__lte=now, my_date__gte=now
        #     ).exclude(my_status='Complete'
        #     ).order_by('my_date', 'my_time'),
        #
        # 'my_today_appts':
        #     Appt.objects.filter(
        #     Q(user__id=request.session['user_id']) &
        #     Q(my_date__lte=now, my_date__gte=now)
        #     ).exclude(my_status='Complete'
        #     ).order_by('my_time')
    }
    return render(request, 'main_app/appts.html', context)

def history(request):

    now = datetime.datetime.now()

    context = {
        'my_past_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_status='Complete')
            ).order_by('updated_at'
            ).reverse()
    }
    return render(request, 'main_app/history.html', context)

def missed(request):

    now = datetime.datetime.now()

    context = {
        'my_missed_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_date__lte=now) &
            Q(my_status='Pending')
            ).exclude(my_date__lte=now, my_date__gte=now
            ).order_by('my_date', 'my_time'
            ).reverse()
    }
    return render(request, 'main_app/missed.html', context)

def new(request):

    return render(request, 'main_app/new.html')

def add(request):

    appt = Appt.ApptManager.add(request.POST)
    logged_in = User.objects.get(id=request.session['user_id'])

    if appt[0] == False:
        new_appt = Appt.objects.create(
            user=logged_in,
            my_task=request.POST['task'],
            my_date=request.POST['date'],
            my_time=request.POST['time'],
            my_location=request.POST['location'],
            my_type=request.POST['type'],
            my_priority=request.POST['priority'],
            my_status='Pending'
        )
        new_appt.save()

        return redirect(reverse ('appts:appts'))
    else:
        errors = appt[1]
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:new'))

def edit(request, appt_id):

    context = {
        'appt': Appt.objects.get(id=appt_id)
    }
    return render(request, 'main_app/edit.html', context)

def process(request, appt_id):

    errors = []

    if request.POST['type'] == "Choose One":
        errors.append("Please choose an appointment type.")

    if request.POST['priority'] == "Choose One":
        errors.append("Please choose an appointment priority.")

    if request.POST['status'] == "Choose One":
        errors.append("Please choose an appointment status.")

    if errors:
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:edit', kwargs={'appt_id':appt_id}))

    else:
        appt = Appt.ApptManager.add(request.POST)

        if appt[0] == False:
            appt = Appt.objects.get(id=appt_id)
            appt.my_task = request.POST['task']
            appt.my_date = request.POST['date']
            appt.my_time = request.POST['time']
            appt.my_location = request.POST['location']
            appt.my_type = request.POST['type']
            appt.my_priority = request.POST['priority']
            appt.my_status = request.POST['status']
            appt.save()

            return redirect(reverse ('appts:appts'))

def complete(request, appt_id):

    appt = Appt.objects.get(id=appt_id)
    appt.my_status = 'Complete'
    appt.save()

    return redirect(reverse ('appts:appts'))

#-------------------------------------------------------------------------------
# USER ACCOUNT SETTINGS

def account(request):

    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'main_app/account.html', context)

def change_username(request, user_id):

    errors = []

    if len(request.POST['username']) < 6:
        errors.append('Username must have at least 6 characters.')

    if errors:
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:account'))

    else:
        user = User.objects.get(id=request.session['user_id'])
        user.username = request.POST['username']
        user.save()
        return redirect(reverse ('appts:appts'))

def change_email(request, user_id):

    errors = []

    if not EMAIL_REGEX.match(request.POST['email']) or len(request.POST['email']) == 0:
        errors.append('Please enter a valid email address.')

    if errors:
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:account'))

    else:
        user = User.objects.get(id=request.session['user_id'])
        user.email = request.POST['email']
        user.save()
        return redirect(reverse ('appts:appts'))

def change_password(request, user_id):

    errors = []

    if len(request.POST['password']) < 8:
        errors.append('Password must have at least 8 characters.')
    if request.POST['password'] != request.POST['confirm_password']:
        errors.append('The passwords you entered did not match.')

    if errors:
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:account'))

    else:
        user = User.objects.get(id=request.session['user_id'])
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.password = hashed
        user.save()
        return redirect(reverse ('appts:appts'))

def delete_account(request, user_id):

    user = User.objects.get(id=user_id)

    user.delete()
    return redirect(reverse ('login:register_home'))

#-------------------------------------------------------------------------------

def delete(request, appt_id):

    appt = Appt.objects.get(id=appt_id)
    appt.delete()
    return redirect(reverse ('appts:appts'))

def logout(request):

    request.session.clear()
    return redirect(reverse('login:login_home'))
