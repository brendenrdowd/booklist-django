from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^library$', views.books, name='books'),
    url(r'^new', views.new,name="new"), 
    url(r'^add/(?P<id>\w)$', views.add), 
    url(r'^remove/(?P<id>\w)$', views.remove), 
    url(r'^$', views.dashboard,name="dashboard"), 
]