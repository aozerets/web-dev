from django.urls import path
from . import views

urlpatterns = [
    path('', views.Sales.as_view()),
    path('orders/', views.Orders.as_view(), name='orders'),
    path('orders/<int:pk>', views.DetailOrder.as_view()),
    path('products/', views.Products.as_view(), name='products'),
    path('products/<int:pk>', views.DetailProduct.as_view(), name='product-detail'),
    path('<string>', views.Sales.as_view()),
]
