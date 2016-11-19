from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta, date, time
from time import strftime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, data):
        errors = []
        bday = data['birthday']
        now = strftime("%Y-%m-%d")

        if len(data['name']) < 2:
            errors.append('Name is too short!')
        if bday == "":
            errors.append('Birthday cannot be blank!')
        if bday > now:
            errors.append('Birthday cannot be in the future!')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('That is an invalid email!')
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long!')
        if data['password'] != data['confirm_password']:
            errors.append('The passwords do not match!')

        user = self.filter(email=data['email'])
        # filter returns a list. if it's empty, the user doesnt exist yet. if the list has something in it, throw an error because the user already exists.
        if user:
            errors.append('That name is already taken!')
        if errors:
            return [False, errors]
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = self.create(name = data['name'], birthday = data['birthday'], email = data['email'], password = hashed)
        # do the rest for all the other inputs and stick inside the create method
        return [True, user]

    def login(self, data):
        errors = []
        user=self.filter(email=data['email'])
        # again we use filter to see if the user is in the list that is returned.
        if len(data['email']) == 0:
            errors.append('Email cannot be blank!')
        if len(data['password']) == 0:
            errors.append('Password cannot be blank!')
        if user:
            if bcrypt.hashpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
            # this compares the password the user types in with the hashed password already in the database to see if they match.
                return [True, user[0]]
            else:
                errors.append('That password is incorrect!')
        return [False, errors]

class User(models.Model):
    name = models.CharField(max_length = 30, blank = False)
    birthday = models.DateField(blank = False)
    email = models.EmailField(blank = False, unique = True)
    password = models.CharField(max_length = 255, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    # valiating:
    # make a variable called errors = [] errors = False
    # everytime we find an error, add to the list
    # at the end, if errors, return (True, errors), if no errors, return (False, user) and create the user_name
