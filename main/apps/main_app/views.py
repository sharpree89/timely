from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import datetime
from . import models
from .models import Appt, ApptManager
from ..login_app.models import User, UserManager
from django.db.models import Q
from django.contrib import messages

def login_home(request):
    print '%'*75
    print 'I am on the login page!'
    print '%'*75
    return render(request, 'login_app/login.html')

def register_home(request):
    print '%'*75
    print 'I am on the login page!'
    print '%'*75
    return render(request, 'login_app/register.html')

def appts(request):
    print '%'*75
    print 'I am on the appts page!'
    print '%'*75

    now = datetime.datetime.now()

    context = {
        # 'my_appt': Appt.objects.filter(user__id=request.session['user_id']),
        'today': now.strftime('%A, ' + '%B ' + '%d, ' + '%Y'),
        # 'appt': Appt.objects.all(),
        'right_now': datetime.datetime.now().time(),

        'my_future_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_date__gte=now)
            ).exclude(my_date__lte=now, my_date__gte=now
            ).exclude(my_status='Complete'
            ).order_by('my_date', 'my_time'),

        'my_today_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_date__lte=now, my_date__gte=now)
            ).exclude(my_status='Complete'
            ).order_by('my_time')
    }
    print '%'*75
    if len(context['my_today_appts']) == 0:
        print context['my_today_appts']
    if len(context['my_future_appts']) == 0:
        print context['my_future_appts']
    print '%'*75
    return render(request, 'main_app/appts.html', context)

def history(request):

    now = datetime.datetime.now()

    context = {
        'my_past_appts':
            Appt.objects.filter(
            Q(user__id=request.session['user_id']) &
            Q(my_status='Complete')
            ).order_by('my_date', 'my_time'
            ).reverse()
    }
    return render(request, 'main_app/history.html', context)

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
            my_location=request.POST['location'] or 'None',
            my_type=request.POST['type'] or 'None',
            my_priority=request.POST['priority'] or 'None',
            my_status='Pending',
            my_symbol=request.POST['symbol'] or '&#x263a;'
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

    appt = Appt.ApptManager.add(request.POST)
    logged_in = User.objects.get(id=request.session['user_id'])

    if appt[0] == False:
        appt = Appt.objects.get(id=appt_id)
        appt.my_task = request.POST['task']
        appt.my_date = request.POST['date']
        appt.my_time = request.POST['time']
        appt.my_location = request.POST['location'] or 'None'
        appt.my_type = request.POST['type']
        appt.my_priority = request.POST['priority']
        appt.my_status = request.POST['status']
        appt.my_symbol = request.POST['symbol']
        appt.save()
        return redirect(reverse ('appts:appts'))
    else:
        errors = appt[1]
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:edit', kwargs={'appt_id':appt_id}))

def complete(request, appt_id):

    appt = Appt.objects.get(id=appt_id)
    appt.my_status = 'Complete'
    appt.save()

    return redirect(reverse ('appts:appts'))

#-------------------------

def account(request):

    context = {
        'user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'main_app/account.html', context)

def process_account(request, user_id):

    user = User.objects.get(id=request.session['user_id'])

    user.username = request.POST['username']
    user.email = request.POST['email']

    user.save()
    return redirect(reverse ('appts:account'))

def delete_account(request, user_id):

    user = User.objects.get(id=user_id)
    user_appts = Appt.objects.filter(user__id=request.session['user_id'])
    
    user.delete()
    user_appts.delete()
    return redirect(reverse ('login:register_home'))

#--------------------------

def delete(request, appt_id):

    appt = Appt.objects.get(id=appt_id)
    appt.delete()
    return redirect(reverse ('appts:appts'))

def logout(request):

    request.session.clear()
    return redirect(reverse('login:login_home'))
