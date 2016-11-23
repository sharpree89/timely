from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User, UserManager
from time import strftime

class ApptManager(models.Manager):
    def add(self, data):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H-%M")

        if data['task'] == "":
            errors.append('Please enter a task.')
        if data['date'] == "" or data['date'] < today:
            errors.append('Please enter a valid date.')
        if data['time'] == "" or data['date'] == today and data['time'] < now:
            errors.append('Please enter a valid time.')
        if data['location'] == "":
            errors.append('Please enter a location.')

        if errors:
            return (True, errors)
        else:
            return (False, data)

class Appt(models.Model):
    #if a user is deleted, all appts tied to that user will be also be deleted
    user = models.ForeignKey('login_app.User', on_delete=models.CASCADE, related_name='userforeignkey')
    my_task = models.CharField(max_length=100, blank=False)
    my_location = models.CharField(max_length=100, blank=False)
    my_date = models.DateField(blank=False)
    my_time = models.TimeField(blank=False)
    my_type = models.CharField(max_length=20)
    my_priority = models.CharField(max_length=12)
    my_status = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ApptManager = ApptManager()
    objects = models.Manager()
