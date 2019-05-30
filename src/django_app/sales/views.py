from django.views.generic import ListView, UpdateView, DetailView, TemplateView
from .models import Order, Product
from datetime import datetime


class Sales(TemplateView):
    template_name = 'sales/base.html'
    day = datetime.now()

    def get_context_data(self, *args, **kwargs):
        context = super(Sales, self).get_context_data(*args, **kwargs)
        context['message'] = 'Hello World!'
        context['day'] = self.day
        context['string'] = context['string'] if 'string' in kwargs.keys() else 'Guest'
        return context


class Orders(ListView):
    template_name = 'sales/orders.html'
    queryset = Order.objects.all()
    context_object_name = 'orders'


class DetailOrder(DetailView):
    template_name = 'sales/order.html'
    queryset = Order.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(DetailOrder, self).get_context_data(*args, **kwargs)
        total = 0
        for product in list(context['order'].products.all()):
            total += int(product.cost[:-1])
        context['total'] = str(total) + "$"
        return context


class Products(ListView):
    template_name = 'sales/products.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class DetailProduct(DetailView, UpdateView):
    template_name = 'sales/product.html'
    queryset = Product.objects.all()
    fields = ['cost', 'comment']
    context_object_name = 'product'