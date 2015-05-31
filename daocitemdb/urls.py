'''
Created on May 5, 2015

@author: deltj
'''
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^searchform', views.searchform),
    url(r'^search', views.search),
    url(r'^showitem', views.showitem)
]

urlpatterns += staticfiles_urlpatterns()
