# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import validators
from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def registerValidation(self,postData):
        response = {
            'status': True,
            'errors': []
        }
        EMAIL_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if not postData['fname'].isalpha() or not postData['lname'].isalpha():
            response['errors'].append('Names cannot contain numbers')
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            response['errors'].append('Names must be at least two characters')
        if not re.match(EMAIL_regex,postData['nemail']):
            response['errors'].append('Please enter a valid email')
        if postData['npassword'] == None or len(postData['npassword']) < 8:
            response['errors'].append('Password must be at least 8 characters')
        if postData['npassword'] != postData['confirm']:
            response['errors'].append('Passwords do not match')
        emailObject = self.filter(email = postData['nemail'])
        if len(emailObject) > 0:
            response['errors'].append('User already exists, please log in')
        if len(response['errors']) == 0:
            hashed = bcrypt.hashpw((postData['npassword'].encode()),bcrypt.gensalt(12))
            user = self.create(fname = postData['fname'].capitalize() , lname = postData['lname'], email = postData['nemail'], password = hashed)
            response['user'] = {
                'name':user.fname,
                'id':user.id,
            }
            return response
        else:
            response['status'] = False
            return response
        
    def loginValidation(self,postData):
        response = {
            'status': True,
            'errors': []
        }
        try:
            user = self.get(email = postData['email'])
        except:
            user = None
        if not user:
            print 'invalid email'
            response['errors'].append('Invalid login')
        else:
            if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                print 'invalid password'
                response['errors'].append('invalid login')
        if len(response['errors']) == 0:
            response['user'] = {
                'name':user.fname,
                'id':user.id
            }
            return response
        else:
            response['status'] = False
            return response

class User(models.Model):
    fname = models.CharField(max_length=35)
    lname = models.CharField(max_length=35)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "User:\n{}\n{}\n{}\n{}\n{}".format(self.id,self.fname,self.lname,self.email,self.password)
    def __str__(self):
        return "User:\n{}\n{}\n{}\n{}\n{}".format(self.id,self.fname,self.lname,self.email,self.password)