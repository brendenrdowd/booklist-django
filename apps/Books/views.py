# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from .models import *

from django.shortcuts import render,redirect

def authenticate(request):
    context = {}
    if 'user' in request.session:
        context = {
            'logged_in':True,
            'name': request.session['user']['name'],
            'id': request.session['user']['id'],
            'list':[]
        }
        return context
    else:
        context['logged_in'] = False
        return context

def books(request):
    # will fetch all books here and return context
    context = authenticate(request)
    library = Book.objects.all()
    context['books'] = library
    return render(request,'Books/books.html',context)

def dashboard(request):
    context = authenticate(request)
    if context['logged_in']:
        # grab all books
        books = ReadingList.objects.grabAll(context['id'])
        return render(request,'Books/dashboard.html',context)
    else:
        return redirect('/')

def new(request):
    context = authenticate(request)
    if request.method=="POST" and context['logged_in']:
        result = Book.objects.bookValidation(request.POST)
        if result['status']:
            return redirect('books')
        else:
            for error in result['errors']:
                messages.error(request,error)
            return redirect('new')
        return render(request,'Books/create.html')
    if not context['logged_in']:
        return redirect('books')
    return render(request,'Books/create.html')

def add(request,id):
    context = authenticate(request)
    if context['logged_in']:
        ReadingList.objects.addToList(id,context['id'])
    return redirect('dashboard')


def remove(request):
    return redirect('dashboard')
