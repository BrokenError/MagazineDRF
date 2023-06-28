from rest_framework import serializers

from apps.orders.models import Order


class OrderCreateSerializer(serializers.Serializer):
    description = serializers.CharField(label='Комментарий')
    deliv_address = serializers.CharField(label='Адрес доставки')
    paid = serializers.BooleanField(label='Оплачено')

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
