from django.urls import path

from apps.orders.views import CreateOrderAPIView

urlpatterns = [path('create/', CreateOrderAPIView.as_view(), name='order_create'),
               ]
