from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.cart import Cart
from apps.orders.services import order_create


class CreateOrderAPIView(APIView):
    @staticmethod
    def get(request):
        return Response({'cart': Cart(request)})

    @staticmethod
    def post(request):
        request.data['user'] = request.user
        return Response(order_create(request.data, Cart(request)))