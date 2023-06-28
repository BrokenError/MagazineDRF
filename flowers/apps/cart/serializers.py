from rest_framework import serializers


class CartAddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, label='Кол-во', initial=1)
    update = serializers.BooleanField(required=False, initial=False, default=False)
