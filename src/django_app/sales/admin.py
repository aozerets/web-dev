from django.contrib import admin
from .models import Product, Order

admin.site.register(Order)
admin.site.register(Product)
