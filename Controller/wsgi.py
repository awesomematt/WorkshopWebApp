# Project name: Workshop Web Application
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

"""
WSGI config for WorkshopSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WorkshopSite.settings")

application = get_wsgi_application()
