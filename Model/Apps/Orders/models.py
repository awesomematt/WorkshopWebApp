# Project name: Workshop Web Application
# Authors: Mateusz Jachimczak & Dawid Pawłowski
# Silesian Univeristy of Technology, Gliwice, Poland
# GitHub: https://github.com/yellowmatt/WorkshopWebApp

from django.db import models


# Class which defines Service model in database
class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.service_name


# Class which defines ShoppingBoxManager - manager stores functions for ShoppingBox object
class ShoppingBoxManager(models.Manager):
    def create_box(self, services, summary):
        shopping_box = self.create(client_service_ordered=services, sum_price=summary)
        return shopping_box

    def update_box(self, shopping_box_id, services, summary):
        ShoppingBox.objects.filter(pk=shopping_box_id).update(client_service_ordered=services, sum_price=summary)

    def calculate_final_price(self, ids):
        list_of_ids = ids.split()
        summary = 0.0
        for id in list_of_ids:
            service = Service.objects.get(pk=id)
            summary += service.service_price
        return summary

    def show_content_of_shopping_box(self, ids):
        list_of_ids = ids.split()
        box_info = ""
        for id in list_of_ids:
            service = Service.objects.get(pk=id)
            service_name = service.service_name + ","
            box_info += service_name
        list = box_info.split(",")
        del list[-1]
        return list

    def create_context(self, ids, shopping_box):
        box_content = ShoppingBox.objects.show_content_of_shopping_box(ids)
        context = {'box_content': box_content, 'shopping_box': shopping_box}
        return context


# Class which defines ShoppingBox model in database
class ShoppingBox(models.Model):
    client_service_ordered = models.CharField(max_length=20)
    sum_price = models.FloatField(default=0.0)
    objects = ShoppingBoxManager()

    def __str__(self):
        return self.client_service_ordered


# Class which defines OrderManager - manager stores functions for Order object
class OrderManager(models.Manager):
    def create_order(self, box, name, surname, number, email, date):
        order = self.create(shopping_box=box, client_name=name,
                            client_surname=surname, client_number=number,
                            client_email=email, order_date=date)
        return order

    def update_order(self, order_id, box, name, surname, number, email, date):
        Order.objects.filter(pk=order_id).update(shopping_box=box, client_name=name,
                                                 client_surname=surname, client_number=number,
                                                 client_email=email, order_date=date)

    def show_order_details(self, shopping_box):
        list_of_ids = shopping_box.client_service_ordered
        list_of_ordered_services = ShoppingBox.objects.show_content_of_shopping_box(list_of_ids)
        return list_of_ordered_services

    def show_order_total_price(self, shopping_box):
        price = shopping_box.sum_price
        return price

    def create_context(self, order, shopping_box):
        user_details = [order.client_name, order.client_surname,
                        order.client_number, order.client_email, order.order_date]
        order_details = Order.objects.show_order_details(shopping_box)
        order_price = Order.objects.show_order_total_price(shopping_box)
        context = {'user_details': user_details, 'order_details': order_details, 'order_price': order_price}
        return context

    def check_if_all_required_fields_are_filled(self, list_of_fields):
        counter = 0
        field = ''
        list_of_ids = []
        list_of_missing_items = []
        for item in list_of_fields:
            field = item
            if not field:
                list_of_ids.append(counter)
            counter += 1
        for id in list_of_ids:
            if id == 0:
                field = 'name'
                list_of_missing_items.append(field)
            if id == 1:
                field = 'surname'
                list_of_missing_items.append(field)
            if id == 2:
                field = 'number'
                list_of_missing_items.append(field)
            if id == 3:
                field = 'e-mail'
                list_of_missing_items.append(field)
            if id == 4:
                field = 'date'
                list_of_missing_items.append(field)
        return list_of_missing_items


# Class which defines Order model in database
class Order(models.Model):
    shopping_box = models.ForeignKey(ShoppingBox, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200)
    client_surname = models.CharField(max_length=200)
    client_number = models.CharField(max_length=200)
    client_email = models.CharField(max_length=200)
    order_date = models.DateTimeField('order date', default=None)
    objects = OrderManager()

    def __str__(self):
        return self.order_date
