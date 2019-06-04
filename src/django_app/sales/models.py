from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name="Product title")
    cost = models.CharField(max_length=50, verbose_name="Product cost")
    brand = models.CharField(max_length=50, verbose_name="Product brand")
    comment = models.TextField(max_length=500, verbose_name="Comments", null=True, blank=True)
    @staticmethod
    def get_absolute_url():
        return reverse('products')

    def __str__(self):
        return "{} ({})".format(self.title, self.brand)


class Order(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Order number")
    products = models.ManyToManyField(Product, verbose_name="Products basket")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_absolute_url():
        return reverse('orders')

    def __str__(self):
        return "Order №{} of '{}'".format(self.id, self.user)
