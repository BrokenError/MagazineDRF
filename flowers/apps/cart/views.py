from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.cart import Cart
from apps.cart.serializers import CartAddProductSerializer
from apps.cart.services import liked_products, history_orders, update_quantity, delete_product_from_cart, \
    add_product_in_cart, paginator_page


@api_view(['GET', 'POST'])
def cart_add(request, product_id):
    serializer = CartAddProductSerializer(data=request.data)
    add_product_in_cart(Cart(request), serializer, product_id)
    return Response({"cart": Cart(request).cart.values()})


@api_view(['GET', 'POST'])
def cart_remove(request, product_id):
    delete_product_from_cart(Cart(request), product_id)
    return Response({"result": f" удален товар с номером{product_id}", 'cart': Cart(request).cart.values()})


@api_view(['GET', 'POST'])
def cart_detail(request):
    cart = update_quantity(Cart(request))
    return Response({'cart': cart.cart})


class HistoryOrdersAPIView(APIView):
    @staticmethod
    def get(request):
        return paginator_page(10, history_orders(request.user.id).values(), request)


class LikedPagesAPIView(APIView):
    @staticmethod
    def get(request):
        content = liked_products({}, request.user.id)
        paginate = paginator_page(10, content['products'], request)
        return paginate
