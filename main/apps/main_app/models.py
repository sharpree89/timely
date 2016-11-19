from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User, UserManager
import datetime
from time import strftime

class ApptManager(models.Manager):
    def add(self, data):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H-%M")
        print "%" * 50
        print "models.py def add", now
        print "%" * 50

        if data['task'] == "":
            errors.append('Please enter a task!')
        if data['date'] == "" or data['date'] < today:
            errors.append('Please enter a valid date!')
        if data['time'] == "" or data['date'] == today and data['time'] < now:
            errors.append('Please enter a valid time!')

        if errors:
            return (True, errors)
        else:
            return (False, data)

    # def process(self, data):
    #     errors = []
    #     today = strftime("%Y-%m-%d")
    #     now = strftime("%H-%M")
    #     print "%" * 50
    #     print "models.py def process", now
    #     print "%" * 50
    #
    #     if data['task'] == "":
    #         errors.append('Please enter a task!')
    #     if data['date'] == "" or data['date'] < today:
    #         errors.append('Please enter a valid date!')
    #     if data['time'] == "" or data['date'] == today and data['time'] < now:
    #         errors.append('Please enter a valid time!')
    #
    #     if errors:
    #         return (True, errors)
    #     else:
    #         return (False, data)

class Appt(models.Model):
    user = models.ForeignKey('login_app.User', related_name='userforeignkey')
    my_task = models.CharField(max_length=100, blank=False)
    my_location = models.CharField(max_length=100)
    my_date = models.DateField(blank=False)
    my_time = models.TimeField(blank=False)
    my_type = models.CharField(max_length=12)
    my_priority = models.CharField(max_length=12)
    my_status = models.CharField(max_length=12)
    my_symbol = models.CharField(max_length = 12) # smiley face
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ApptManager = ApptManager()
    objects = models.Manager()
