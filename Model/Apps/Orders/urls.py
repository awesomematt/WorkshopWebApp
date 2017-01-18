# Project name: Workshop Web Application
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

from django.conf.urls import url

from . import views

app_name = 'orders'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mybox/$', views.shoppingBox, name='mybox'),
    url(r'^finalize/$', views.finalize, name='finalize'),
    url(r'^summary/$', views.order_info, name='summary'),
]
