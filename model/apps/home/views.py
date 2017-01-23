from django.shortcuts import render
from orders.models import Service


def index(request):
    return render(request, 'home/index.html')


def services(request):
    service_list = Service.objects.all()
    context = {'service_list': service_list}
    return render(request, 'home/services.html', context)


def localization(request):
    return render(request, 'home/localization.html')
