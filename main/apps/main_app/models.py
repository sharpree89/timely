from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User, UserManager
from datetime import datetime, timedelta, date, time
from time import strftime

class ApptManager(models.Manager):
    def add(self, data):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H=%M-%S")

        if data['date'] == "" or data['date'] < today:
            errors.append('Please enter a valid date!')
        if data['time'] == "":
            errors.append('Please enter a valid time!')
        if data['task'] == "":
            errors.append('Please enter a task!')
        if data['location'] == "":
            errors.append('Please enter a location!')
        if errors:
            return (True, errors)
        else:
            errors.append('Invalid info, try again!')
            return (False, data)

    def process(self, data):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H=%M-%S")

        if data['date'] == "" or data['date'] < today:
            errors.append('Please enter a valid date!')
        if data['time'] == "":
            errors.append('Please enter a valid time!')
        if data['task'] == "":
            errors.append('Please enter a task!')
        if data['location'] == "":
            errors.append('Please enter a location!')
        if errors:
            return (True, errors)
        else:
            errors.append('Invalid info, try again!')
            return (False, data)

class Appt(models.Model):
    user = models.ForeignKey('login_app.User', related_name='userforeignkey')
    my_task = models.CharField(max_length=45, blank=False)
    my_location = models.CharField(max_length=45, blank=False)
    my_date = models.DateField(blank=False)
    my_time = models.TimeField(blank=False)
    my_status = models.CharField(max_length=12)
    my_symbol = models.CharField(max_length = 10, default='&#x263a;')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ApptManager = ApptManager()
    objects = models.Manager()
