# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request,'LR/index.html')

def register(request):
    result = User.objects.registerValidation(request.POST)
    if result['status']:
        request.session['user'] = result['user']
        return redirect('/books')
    else:
        for error in result['errors']:
            messages.error(request,error)
        return redirect('index')
        

def login(request):
    result = User.objects.loginValidation(request.POST)
    if result['status']:
        request.session['user'] = result['user']
        return redirect('/books')
    else:
        for error in result['errors']:
            messages.error(request,error)
        return redirect('index')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('index')