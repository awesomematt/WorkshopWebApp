# Project name: Workshop Web Application
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^orders/', include('orders.urls')),
    url(r'^admin/', admin.site.urls),
]
