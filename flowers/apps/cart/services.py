from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from apps.cart.serializers import CartAddProductSerializer
from apps.catalog.services import get_rating_catalog
from apps.orders.models import Order
from apps.products.models import Products


def add_product_in_cart(cart, serializer, product_id):
    product = get_object_or_404(Products, id=product_id)
    if serializer.is_valid(raise_exception=True):
        cart.add(product=product,
                 quantity=serializer.data['quantity'],
                 update_quantity=serializer.data['update'])


def delete_product_from_cart(cart, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)


def update_quantity(cart):
    for item in cart:
        item['update_quantity_form'] = CartAddProductSerializer(initial={'quantity': item['quantity'],
                                                                         'update': True}).data
    return cart


def liked_products(content, user):
    prod = Products.objects.filter(check_like__user=user)
    content['products'] = prod.values()
    content.update(get_rating_catalog(content))
    return content


def history_orders(user_id):
    orders = Order.objects.filter(user_id=user_id).order_by('-created')[:20]
    return orders


def paginator_page(quantity_objects, objects, request):
    paginator = PageNumberPagination()
    paginator.page_size = quantity_objects
    result_page = paginator.paginate_queryset(objects, request)
    return paginator.get_paginated_response(result_page)
