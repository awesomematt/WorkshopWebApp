# Project name: Workshop Web Application
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

from django.shortcuts import render
from .models import Service
from .models import ShoppingBox
from .models import Order


# Function which defines view for root of orders app
# Index of Orders app. Shows the list of available services.
def index(request):
    service_list = Service.objects.all()
    box_edit = request.POST.get('edit')
    if box_edit is not None:
        request.session['box_edit'] = 'true'
    context = {'service_list': service_list}
    return render(request, 'orders/index.html', context)


# Function which defines view for shopping box in orders app
# MyBox of Orders app. Shows the content of shopping box.
def shoppingBox(request):
    selected_services = " ".join(request.POST.getlist('service[]'))
    if not selected_services and 'shopping_box' not in request.session:
        return render(request, 'orders/mybox.html', {
            'message': "Twój koszyk jest pusty.",
        })
    elif 'shopping_box' in request.session:
        box_edit = request.session.get('box_edit')
        if box_edit is not None and 'true' in box_edit:
            if 'order' in request.session:
                request.session['box_edit'] = 'false'
                return render(request, 'orders/mybox.html', {
                    'message': "Dokonano już zamówienia! Edycja koszyka nie jest już możliwa!",
                })
            elif not selected_services:
                request.session['box_edit'] = 'false'
                shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
                ids = shopping_box.client_service_ordered
                box_content = ShoppingBox.objects.show_content_of_shopping_box(ids)
                context = {'box_content': box_content,
                           'shopping_box': shopping_box,
                           'message': "Nie wybrano żadnej usługi! Edycja koszyka anulowana! "}
                return render(request, 'orders/mybox.html', context)
            else:
                summary = ShoppingBox.objects.calculate_final_price(selected_services)
                ShoppingBox.objects.update_box(request.session['shopping_box'], selected_services, summary)
                shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
                shopping_box.refresh_from_db()
                context = ShoppingBox.objects.create_context(selected_services, shopping_box)
                request.session['box_edit'] = 'false'
                return render(request, 'orders/mybox.html', context)
        else:
            shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
            ids = shopping_box.client_service_ordered
            context = ShoppingBox.objects.create_context(ids, shopping_box)
            return render(request, 'orders/mybox.html', context)
    else:
        summary = ShoppingBox.objects.calculate_final_price(selected_services)
        shopping_box = ShoppingBox.objects.create_box(selected_services, summary)
        request.session['shopping_box'] = shopping_box.id
        shopping_box.save()
        context = ShoppingBox.objects.create_context(selected_services, shopping_box)
        return render(request, 'orders/mybox.html', context)


# Function which defines view for finalization form of orders app
# Finalize of Orders app. Shows the form for order finalization.
def finalize(request):
    box_edit = request.POST.get('edit')
    data_edit = request.POST.get('data_edit')
    if box_edit is not None:
        request.session['box_edit'] = 'false'
    if 'order' in request.session:
        if data_edit is not None:
            request.session['order_edit'] = 'true'
            return render(request, 'orders/finalize.html')
        else:
            return render(request, 'orders/finalize.html', {
                'message': "Dokonano już zamówienia!",
            })
    elif 'shopping_box' in request.session:
        return render(request, 'orders/finalize.html')
    else:
        return render(request, 'orders/finalize.html', {
            'message': "Twój koszyk jest pusty! Proszę najpierw dodać usługi do koszyka w celu finalizacji!",
        })


# Function which defines view for summary of orders app
# Summary of Orders app. Shows the summary about ordered services, client data and final price.
def order_info(request):
    order_edit = request.session.get('order_edit')
    if not order_edit:
        order_edit = 'false'
    if 'shopping_box' in request.session:
        shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
    else:
        return render(request, 'orders/summary.html', {
            'message': "Twój koszyk jest pusty! Proszę najpierw dodać usługi do koszyka!",
        })
    if 'order' in request.session and 'false' in order_edit:
        shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
        order = Order.objects.get(pk=request.session['order'])
        context = Order.objects.create_context(order, shopping_box)
        return render(request, 'orders/summary.html', context)
    else:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        number = request.POST.get('phone_number')
        email = request.POST.get('e-mail')
        date = request.POST.get('date')
        list_of_fields = [name, surname, number, email, date]
        list_of_missing_fields = Order.objects.check_if_all_required_fields_are_filled(list_of_fields)
        if not list_of_missing_fields:
            if 'false' in order_edit:
                order = Order.objects.create_order(shopping_box, name, surname, number, email, date)
                order.save()
                request.session['order'] = order.id
                context = Order.objects.create_context(order, shopping_box)
                return render(request, 'orders/summary.html', context)
            else:
                Order.objects.update_order(request.session['order'], shopping_box, name, surname, number, email, date)
                order = Order.objects.get(pk=request.session['order'])
                order.refresh_from_db()
                request.session['order_edit'] = 'false'
                context = Order.objects.create_context(order, shopping_box)
                return render(request, 'orders/summary.html', context)
        else:
            if 'order' in request.session:
                shopping_box = ShoppingBox.objects.get(pk=request.session['shopping_box'])
                order = Order.objects.get(pk=request.session['order'])
                context = Order.objects.create_context(order, shopping_box)
                return render(request, 'orders/summary.html', context)
            else:
                return render(request, 'orders/summary.html', {
                    'message': "Nie wypełniono wymaganych pól w formularzu finalizacji zamówienia!",
                })
