import logging

from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from apps.catalog.models import Categories
from apps.products.models import Products
from apps.products.tests import write_text, time_of_function

logging.basicConfig(level=51, format="Logs: %(message)s")


class TestCatalog(APITestCase):
    """ Тестирование каталога с товарами """

    @classmethod
    def setUp(cls):
        cls.default_time = '2000-01-01 00:00:00+03'
        User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        cls.user = User.objects.first()
        cls.client = APIClient()

    @classmethod
    def tearDown(cls):
        logging.log(51, 'Success')

    def create_check_categories(self):
        data_categories = {1: ['Букеты', 'bukety'], 2: ['Цветы', 'cveti'],
                           3: ['События', 'sobitiya'], 4: ['Другое', 'drygoe']}
        for _ in data_categories:
            Categories(id=_, title=data_categories[_][0], slug=data_categories[_][1], date=self.default_time).save()

    def create_category(self):
        self.category = Categories(1, 'Букеты', 'byketi', self.default_time)
        self.category.save()

    def create_and_authorization(self):
        self.client.force_authenticate(user=self.user)

    def create_product(self):
        self.create_category()
        self.product = Products(1, 'ТЕСТ1', 'test', '2400', '----', '', True,
                                self.default_time, self.default_time, self.category.id)
        self.product.save()

    @time_of_function
    def test_search_page(self):
        write_text('Проверка-поиск-товаров-в-каталоге')
        self.create_product()
        response = self.client.get('/catalog/search/', {}, format='json')
        print(response)
        response = self.client.post('/catalog/search/', {'prod_title_search': 'тес'}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_catalog_main(self):
        write_text('Проверка-все-категории')
        self.create_product()
        response = self.client.get('/catalog/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_show_category(self):
        write_text('Проверка-выбранная категория')
        self.create_product()
        self.create_check_categories()
        response = self.client.get('/catalog/bukety/', {}, format='json')
        print(response)
        logging.log(51, Categories.objects.all().values('title', 'slug'))
        logging.log(51, response.json())


def write_categories(cat_title):
    return print('---- Категория {}'.format(cat_title))
