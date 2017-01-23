# Workshop Web Application Project
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^admin/', admin.site.urls),
]
