import requests
from bs4 import BeautifulSoup
from django.db.models import Avg

from apps.cart.serializers import CartAddProductSerializer
from apps.orders.models import Order
from apps.products.models import Products, Rating
from apps.products.serializers import ProductSerializer
from apps.users.models import ReplyComments
from apps.users.serializer import ReplyCommentsSerializer


def base_content(content, user_id):
    product = Products.objects.get(slug=content['prod_slug'])
    user_orders = Order.objects.filter(user_id=user_id).values()
    content['stars'] = Rating.objects.filter(prod=product.id).aggregate(Avg('star')).get('star__avg')
    content['check_like'] = product.check_like.filter(user_id=user_id, product=product).exists()
    check_buy = user_orders.filter(linkorder__product=product.id)
    check_not_review = not product.check_review.filter(user=user_id).exists()
    content['product_paid'] = False
    if check_buy:
        content['product_paid'] = True
    content.update({'product': ProductSerializer(product).data, 'cart_product_form': CartAddProductSerializer().data,
                    'check_not_review': check_not_review})
    return content


def take_location(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    content = {'valid_locations': request.COOKIES.get('answer'), 'ip': ip}
    return content


def get_location_user(content):
    data_locations = {
        'Rostov-on-Don': '%3A7187d1900e8f6fb609fd28593c8d2689135091c7e8c6aeb846b43b29deaa3210',
        'Moscow': '%3A6ba45ccc3778f11ab04a791350f71a03b7c87332aab7ed5b3d57470f564adbee',
        'Voronesh': '%3A1688495215b83856fbb37d8a1a91c4edc25e1d6a237d6933c11312a6ab6ea2f1',
        'Volgograd': '%3A28fcedf564921587da2e057ae0884202359b077cea124b0b68941958eeb941f3',
        'country': '%3A6a027cc11bee21604b8a97e648e09535306806441f0b71ec2a00e67d522cc289'}

    page = requests.get(f'https://check-host.net/ip-info?host={content["ip"]}')
    soup = BeautifulSoup(page.text, 'html.parser')
    location_user = soup.findAll('table', class_='hostinfo result')
    data_user = str(location_user[1].text).replace('\n', ' ').split('  ')
    country = data_user[10]
    city = data_user[15]
    if not content['valid_locations'] or f"{city}" not in data_locations.keys():
        map_code = data_locations['country']
    else:
        map_code = data_locations[f"{city}"]
    return {'title': 'Наши магазины', 'location': f'{country} {city}',
            'map_code': map_code}


def valid_serializer(serializer):
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.is_valid(raise_exception=True)


def rate_the_product(product_id, user, grade):
    prod = Products.objects.get(id=product_id)
    Rating.objects.update_or_create(prod=prod, defaults={'user': user, 'star': grade})


def change_reply_comment(data, reply_comment_id):
    change = ReplyComments.objects.get(pk=reply_comment_id)
    data['product'] = change.product_id
    data['comment'] = change.comment_id
    serializer = ReplyCommentsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.update(instance=ReplyComments.objects.get(id=reply_comment_id), validated_data=data)
