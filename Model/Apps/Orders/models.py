import datetime

from django.db import models
from django.utils import timezone


class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.service_name


class ShoppingBoxManager(models.Manager):
    def create_box(self, services, summary):
        shopping_box = self.create(client_service_ordered=services, sum_price=summary)
        return shopping_box

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


class ShoppingBox(models.Model):
    client_service_ordered = models.CharField(max_length=20)
    sum_price = models.FloatField(default=0.0)
    objects = ShoppingBoxManager()

    def __str__(self):
        return self.client_service_ordered


class OrderManager(models.Manager):
    def create_order(self, box, name, surname, number, email, date):
        order = self.create(shopping_box=box, client_name=name, client_surname=surname, client_number=number,
                            client_email=email, order_date=date)
        return order

    def show_order_details(self, shopping_box):
        list_of_ids = shopping_box.client_service_ordered
        list_of_ordered_services = ShoppingBox.objects.show_content_of_shopping_box(list_of_ids)
        return list_of_ordered_services

    def show_order_total_price(self, shopping_box):
        price = shopping_box.sum_price
        return price


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
