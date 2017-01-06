from django.shortcuts import get_object_or_404, render
from .models import Service
from .models import ShoppingBox
from .models import Order
from django.http import HttpResponse


def index(request):
    service_list = Service.objects.all()
    context = {'service_list': service_list}
    return render(request, 'orders/index.html', context)


def shoppingBox(request):
    # należy dopracować koszyk, użyć request.session..
    # https://docs.djangoproject.com/en/1.10/topics/http/sessions/
    selected_services = " ".join(request.POST.getlist('service[]'))
    if not selected_services:
        return render(request, 'orders/mybox.html', {
            'message': "Twój koszyk jest pusty.",
        })
    else:
        summary = ShoppingBox.objects.calculate_final_price(selected_services)
        shopping_box = ShoppingBox.objects.create_box(selected_services, summary)
        shopping_box.save()
        box_content = ShoppingBox.objects.show_content_of_shopping_box(selected_services)
        context = {'box_content': box_content, 'shopping_box': shopping_box}
        return render(request, 'orders/mybox.html', context)


def finalize(request):
    shopping_box_id = request.POST.get('shopping_box')
    context = {'shopping_box_id': shopping_box_id}
    return render(request, 'orders/finalize.html', context)


def order_info(request):
    shopping_box = ShoppingBox.objects.get(pk=request.POST.get('shopping_box_id'))
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    number = request.POST.get('phone_number')
    email = request.POST.get('e-mail')
    date = request.POST.get('date')
    order = Order.objects.create_order(shopping_box, name, surname, number, email, date)
    order.save()
    user_details = [name, surname, number, email, date]
    order_details = Order.objects.show_order_details(shopping_box)
    order_price = Order.objects.show_order_total_price(shopping_box)
    context = {'user_details': user_details, 'order_details': order_details, 'order_price': order_price}
    return render(request, 'orders/summary.html', context)
