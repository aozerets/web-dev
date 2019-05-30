from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=50)
    cost = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    comment = models.TextField(max_length=500, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('products')

    def __str__(self):
        return "{} ({})".format(self.title, self.brand)


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order №{} of '{}'".format(self.id, self.user)
