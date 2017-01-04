import datetime

from django.db import models
from django.utils import timezone


class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.service_name


class ShoppingBox(models.Model):
    client_service_ordered = models.CharField(max_length=20)
    sum_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.client_service_ordered


class Order(models.Model):
    shopping_box = models.ForeignKey(ShoppingBox, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200)
    client_surname = models.CharField(max_length=200)
    client_number = models.CharField(max_length=200)
    client_email = models.CharField(max_length=200)
    order_date = models.DateTimeField('order date', default=None)

    def __str__(self):
        return self.order_date
