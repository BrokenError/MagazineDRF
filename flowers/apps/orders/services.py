from apps.orders.models import OrderItem
from apps.orders.serializers import OrderCreateSerializer


def order_create(data, cart):
    order = OrderCreateSerializer(data=data)
    valid = order.is_valid(raise_exception=True)
    if valid:
        created = order.create(validated_data=data)
        for item in cart:
            OrderItem.objects.create(
                order=created,
                product_id=item['product']['id'],
                price=item['price'],
                quantity=item['quantity'])
        cart.clear()
        valid = 'Заказ успешно создан'
    return {"cart": cart, 'results': valid}
