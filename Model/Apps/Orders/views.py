from django.shortcuts import get_object_or_404, render
from .models import Service
from .models import ShoppingBox
from django.http import HttpResponse


def index(request):
    service_list = Service.objects.all()
    context = {'service_list': service_list}
    return render(request, 'orders/index.html', context)


def shoppingBox(request):
    # należy dopracować koszyk, użyć request.session..
    # https://docs.djangoproject.com/en/1.10/topics/http/sessions/
    shopping_box = get_object_or_404(ShoppingBox, pk=1)
    return render(request, 'orders/mybox.html', {'shopping_box': shopping_box})


def finalize(request):
    return HttpResponse("Finalizowanie zamówienia")


def order_info(request):
    return HttpResponse("Szczegóły zamówionych usług")
