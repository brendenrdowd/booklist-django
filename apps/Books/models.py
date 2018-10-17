# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import validators
from django.db import models
from datetime import datetime
from ..LR.models import User
import re
import bcrypt

class BookManager(models.Manager):
    def bookValidation(self,postData):
        response = {
            'status': True,
            'errors': []
        }
        isbn_REGEX = re.compile(r'^(97(8|9))?\d{9}(\d|X)$')
        if len(postData['title']) < 3 or len(postData['title']) > 100:
            response['errors'].append('Please enter a valid title')
        if len(postData['author']) < 3 or len(postData['author']) > 100:
            response['errors'].append('Please enter a valid author')
        if len(postData['isbn']) > 13 or not re.match(isbn_REGEX,postData['isbn']):
            response['errors'].append('Please enter a valid ISBN, ISBNs should be 10-13 digits, or end in an X')
        else:
            bookObject = self.filter(isbn = postData['isbn'])
            if len(bookObject) > 0:
                response['errors'].append('Book already in library')
        if len(response['errors']) == 0:
            book = self.create(title=postData['title'],author=postData['author'],isbn=postData['isbn'],publication_date=postData['publication_date'])
            book.save()
            return response
        else:
            response['status'] = False
            return response

class ListManager(models.Manager):
    def grabAll(self,uid):
        # try:
        #     books = ReadingList.objects.filter(user_id=request.session['user']['id'])
        # except ReadingList.DoesNotExist:
        #     return render(request,'Books/dashboard.html',context)
        # if len(books) > 0:
        #     for book in books:
        #         context['list'].append(Book.objects.get(id=book.book_id))
        return

    def addToList(self,book,user):
        print '[addToList]:',self
        book = Book.objects.get(id=book)
        user = User.objects.get(id=user)
        self.create(book_id=book,user_id=user)
        return

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publication_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    def __repr__(self):
        return 'Book:\n{}\n{}\n{}\n{}\n{}'.format(self.id,self.title,self.author,self.isbn,self.publication_date)
    def __str__(self):
        return 'Book:\n{}\n{}\n{}\n{}\n{}'.format(self.id,self.title,self.author,self.isbn,self.publication_date)


class ReadingList(models.Model):
    book_id = models.ForeignKey(Book,on_delete=models.PROTECT)
    user_id = models.ForeignKey(User,on_delete=models.PROTECT)
    objects = ListManager()
    def __repr__(self):
        return 'Book:\n{}\n{}\n{}'.format(self.id,self.user_id,self.book_id)
    def __str__(self):
        return 'Book:\n{}\n{}\n{}'.format(self.id,self.user_id,self.book_id)