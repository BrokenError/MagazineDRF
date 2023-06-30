import logging

from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from apps.products.tests import write_text, time_of_function

logging.basicConfig(level=51, format="Logs: %(message)s")


class TestOrders(APITestCase):
    """ Тестирование системы заказов """

    def setUp(self):
        default_time = '2000-01-01 00:00:00+03'
        User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        self.user = User.objects.first()
        self.client = APIClient()

    @time_of_function
    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        write_text('Проверка-создание-заказа')
        response = self.client.post('/orders/create/', {"description": "test",
                                                        "paid": "True", "deliv_address": "Success"}, format='json')
        logging.log(51, response.json())
