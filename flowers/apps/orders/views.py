from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.cart import Cart
from apps.orders.services import order_create


class CreateOrderAPIView(APIView):
    @staticmethod
    @login_required
    def get(request):
        return Response({'cart': Cart(request)})

    @staticmethod
    @login_required()
    def post(request):
        request.data['user'] = request.user
        return Response(order_create(request.data, Cart(request)))
