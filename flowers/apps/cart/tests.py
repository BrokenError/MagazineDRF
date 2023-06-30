import logging
import time

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from apps.products.tests import write_text
from apps.catalog.models import Categories
from apps.products.models import Products, Comments
from apps.products.serializers import ReviewSerializer, CommentSerializer
from apps.products.services import base_content

logging.basicConfig(level=51, format="Logs: %(message)s")


def time_of_function(function):
    def wrapped(*args, **kwargs):
        start_time = time.perf_counter()
        res = function(*args, **kwargs)
        logging.log(51, "Время выполнения: {0:.4f} сек".format(time.perf_counter() - start_time))
        return res
    return wrapped


class TestProducts(APITestCase):
    """ Тестирование корзины """

    @classmethod
    def tearDown(cls):
        logging.log(51, 'Success')

    @classmethod
    def setUp(cls):
        factory = APIRequestFactory()
        client = APIClient()
        cls.default_time = '2000-01-01 00:00:00+03'
        cls.comment = Comments.objects.first()
        cls.factory = factory
        cls.client = client

    def create_superuser(self):
        User.objects.all().delete()
        user = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        self.client.force_authenticate(user=user)
        return user

    def create_category(self):
        Categories(1, 'Букеты', 'byketi', self.default_time).save()
        self.category = Categories.objects.first()
        return self.category

    def create_product(self):
        self.create_category()
        Products(1, 'ТЕСТ1', 'test', '2400', '----', '', True, self.default_time, self.default_time,
                 self.category.id).save()
        self.product = Products.objects.first()
        return self.product

    @time_of_function
    def test_cart_view(self):
        write_text(f"Проверка-работа-корзины")
        response = self.client.get('/cart/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_cart_add(self):
        write_text('Проверка-добавление-в-корзину')
        product = self.create_product()
        response = self.client.post(f'/cart/add/{product.id}/', data={'update': 0, "quantity": 2}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_cart_delete(self):
        write_text('Проверка-удаление-из-корзины')
        product = self.create_product()
        response = self.client.post(f'/cart/remove/{product.id}/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_history_order(self):
        self.user = self.create_superuser()
        self.client.force_authenticate(user=self.user)
        write_text('Проверка-история-заказов')
        create_order = self.client.post('/orders/create/', {"description": "test", "paid": "True",
                                                            "deliv_address": "Success"}, format='json')
        response = self.client.get('/cart/history/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_like_products(self):
        write_text('Проверка-понравившиеся-товары')
        response = self.client.get('/cart/liked/', {}, format='json')
        print(response)
        logging.log(51, response.json())
