import logging
import time

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

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
    """ Тестирование приложения с товарами"""

    def tearDown(cls):
        logging.log(51, 'Success')

    @classmethod
    def setUpTestData(cls):
        factory = APIRequestFactory()
        client = APIClient()
        User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        cls.default_time = '2000-01-01 00:00:00+03'
        cls.comment = Comments.objects.first()
        request = factory.get('/')
        user = User.objects.first()
        client.force_authenticate(user=user)
        cls.user = user
        cls.factory = factory
        cls.client = client

    def create_category(self):
        self.category = Categories(1, 'Букеты', 'byketi', self.default_time)
        self.category.save()

    def create_product(self):
        self.create_category()
        self.product = Products(1, 'ТЕСТ1', 'test', '2400', '----', '', True,
                                self.default_time, self.default_time, self.category.id)
        self.product.save()

    def add_comment(self):
        self.create_product()
        name_form_data = {'text': 'TEST', 'user': '1', 'product': '1'}
        serializer = CommentSerializer(data=name_form_data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            return serializer.save()
        else:
            return valid

    def add_review(self):
        self.create_product()
        name_form_data = {'name': 'TESTED', 'text': 'TEST', 'user': '1', 'product': '1'}
        serializer = ReviewSerializer(data=name_form_data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            return serializer.save()
        else:
            return valid

    @time_of_function
    def test_base_content(self):
        write_text(f"Проверка-базового-контента")
        self.create_product()
        content = base_content({'prod_slug': 'test'}, self.user.id)
        print(content)

    @time_of_function
    def test_main_view(self):
        write_text(f"Запуск-начальной-страницы")
        self.create_product()
        response = self.client.get('/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_links(self):
        write_text(f"Проверка-ссылок-страницы")
        links = ['/aboutus', '/catalog', '/user', '/cart']
        for i in links:
            response = self.client.get(i, {}, format='json')
            self.assertEquals(response.status_code, 301)

    @time_of_function
    def test_aboutus_view(self):
        write_text(f"Проверка-страницы-О нас")
        self.client.get('/aboutus/', {}, format='json')
        self.client.post('/aboutus/', {}, format='json')

    @time_of_function
    def test_reviews_view(self):
        write_text(f"Проверка-страницы-Отзывов")
        self.add_review()
        response = self.client.get('/reviews/test/')
        print(response)
        logging.log(51, response.json()['content'])

    @time_of_function
    def test_comments_view(self):
        write_text(f"Проверка-страницы-Комментариев")
        self.add_comment()
        response = self.client.get(f'/comments/test/')
        print(response)
        logging.log(51, response.json()['content'])

    @time_of_function
    def test_add_reviews(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-добавления-отзыва")
        self.create_product()
        response = self.client.post('/add-review/1', {"user": "1", "product": "1", 'name': 'test', 'text': 'success'},
                                    format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_add_comments(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-добавления-комментария")
        self.create_product()
        response = self.client.post('/add-comment/1', {"user": "1", "product": "1", 'text': 'success'}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_change_reviews(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-изменения-отзыва")
        review = self.add_review()
        response = self.client.post(f'/change-review/1/{review.id}', {"name": "success", "text": "test"}, format='json')
        print(response)
        logging.log(51, response.json()['result'])

    @time_of_function
    def test_change_comments(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-изменения-комментария")
        comment = self.add_comment()
        response = self.client.post(f'/change-comment/1/{comment.id}', {"text": "success"}, format='json')
        print(response)
        logging.log(51, response.json()['result'])

    @time_of_function
    def test_remove_review(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-удаление-отзыва")
        review = self.add_review()
        response = self.client.post(f'/delete-review/{review.id}', format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_remove_comment(self):
        self.client.force_authenticate(user=self.user)
        write_text(f"Проверка-удаление-комментария")
        comment = self.add_comment()
        response = self.client.post(f'/delete-comment/{comment.id}', format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_star(self):
        write_text(f"Проверка-оценка-товара")
        self.client.force_authenticate(user=self.user)
        self.create_product()
        response = self.client.post('/give-grade/1', {"grade": 5}, format='json')
        print(response)
        logging.log(51, response.json())


def write_text(text):
    return print('\n' + text.center(70, "-"))
