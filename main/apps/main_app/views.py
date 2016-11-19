from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, time
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

    now = datetime.now()

    context = {
        'my_appt': Appt.objects.filter(user__id=request.session['user_id']),
        'today': datetime.now().date(),
        'appt': Appt.objects.all(),
        'my_future_appt': Appt.objects.filter(Q(my_date__gte=now) & Q(user__id=request.session['user_id'])).exclude(my_date__lte=now, my_date__gte=now).order_by('my_date'),
        'my_today_appt': Appt.objects.filter(Q(my_date__lte=now, my_date__gte=now) & Q(user__id=request.session['user_id'])).order_by('my_time')
    }

    return render(request, 'main_app/appts.html', context)

def add(request):
    print '%'*75
    print request.POST
    print '%'*75
    appt = Appt.ApptManager.add(request.POST)
    logged_in = User.objects.get(id=request.session['user_id'])

    if appt[0] == False:
        new_appt = Appt.objects.create(user=logged_in, my_task=request.POST['task'], my_location=request.POST['location'], my_date=request.POST['date'], my_time=request.POST['time'], my_status='Pending', my_symbol=request.POST['symbol'])
        new_appt.save()
        return redirect(reverse ('appts:appts'))
    else:
        errors = appt[1]
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:appts'))

def new(request):
    return render(request, 'main_app/new.html')

def delete(request, appt_id):
    print '%'*75
    print 'I am on the delete page'
    print '%'*75
    appt = Appt.objects.get(id=appt_id)
    appt.delete()
    return redirect(reverse ('appts:appts'))

def edit(request, appt_id):
    print '%'*75
    print 'I am on the edit page!'
    print '%'*75
    context = {
        'appt': Appt.objects.get(id=appt_id)
        }
    return render(request, 'main_app/edit.html', context)

def process(request, appt_id):
    print '%'*75
    print 'I am on the process edit page!'
    print '%'*75

    appt = Appt.ApptManager.add(request.POST)
    logged_in = User.objects.get(id=request.session['user_id'])

    if appt[0] == False:
        appt = Appt.objects.get(id=appt_id)
        appt.my_task = request.POST['task']
        appt.my_location = request.POST['location']
        appt.my_status = request.POST['status']
        appt.my_date = request.POST['date']
        appt.my_time = request.POST['time']
        appt.my_symbol = request.POST['symbol']
        appt.save()
        return redirect(reverse ('appts:appts'))
    else:
        errors = appt[1]
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('appts:edit', kwargs={'appt_id':appt_id}))

def logout(request):

    request.session.clear()
    return redirect(reverse('login:login_home'))
