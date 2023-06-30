import logging

from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from apps.catalog.models import Categories
from apps.products.models import Products
from apps.products.tests import write_text, time_of_function
from apps.products.serializers import CommentSerializer
from apps.users.models import ReplyComments

logging.basicConfig(level=51, format="Logs: %(message)s")


class TestUsers(APITestCase):
    """ Тестирование пользователя """

    @classmethod
    def tearDown(cls):
        logging.log(51, 'Success')

    @classmethod
    def setUp(cls):
        client = APIClient()
        cls.default_time = '2000-01-01 00:00:00+03'
        cls.client = client

    def create_and_authorization(self):
        self.user = self.create_superuser()
        self.client.force_authenticate(user=self.user)

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

    def add_comment(self):
        self.product = self.create_product()
        user = self.create_superuser()
        name_form_data = {'text': 'TEST', 'user': user.id, 'product': self.product.id}
        serializer = CommentSerializer(data=name_form_data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            return serializer.save()
        else:
            return valid

    def create_superuser(self):
        User.objects.all().delete()
        user = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        self.client.force_authenticate(user=user)
        return user

    @time_of_function
    def test_cart_view(self):
        write_text(f"Проверка-регистрация-пользователя")
        response = self.client.post('/user/register/', {"password": '1111', "username": 'root'}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_verify_phone(self):
        self.create_superuser()
        write_text('Проверка-привязка-телефона')
        response = self.client.post('/user/verify/', {"phoneNumber": '+79543212345'}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_change_password(self):
        self.create_and_authorization()
        write_text('Проверка-изменение-пароля')
        response = self.client.put('/user/', {"old_password": "1111", "new_password": "1234"}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_user_info(self):
        self.create_and_authorization()
        write_text('Проверка-информация-о-пользователе')
        response = self.client.get('/user/info/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_user_personal(self):
        self.create_and_authorization()
        write_text('Проверка-персональная-информация')
        response = self.client.get('/user/personal/', {}, format='json')
        print(response)
        response = self.client.post('/user/personal/', {'city': "Testes", "bio": 'ilovecoding'}, format='json')
        logging.log(51, response.json())

    @time_of_function
    def test_user_security(self):
        self.create_and_authorization()
        write_text('Проверка-секретная-информация')
        response = self.client.get('/user/security/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_user_logout(self):
        self.create_and_authorization()
        write_text('Проверка-выход-из-аккаунта')
        response = self.client.get('/user/logout/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_user_delete(self):
        self.create_and_authorization()
        write_text('Проверка-удаление-аккаунта')
        response = self.client.post('/user/delete/', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_user_like(self):
        self.create_and_authorization()
        write_text('Проверка-лайк-продукта')
        product = self.create_product()
        response = self.client.get(f'/user/like/{product.id}')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_reply_comment(self):
        self.create_and_authorization()
        write_text('Проверка-добавление-ответного-комментария')
        comment = self.add_comment()
        response = self.client.post(f'/user/comment/{comment.id}/{self.product.id}', {"text": 'TESTED'}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_delete_reply_comment(self):
        self.create_and_authorization()
        write_text('Проверка-удаление-ответного-комментария')
        comment = self.add_comment()
        add_reply_comment = self.client.post(f'/user/comment/{comment.id}/{self.product.id}', {"text": 'TESTED'},
                                             format='json')
        logging.log(51, add_reply_comment)
        response = self.client.post(f'/user/delete-reply-comment/{ReplyComments.objects.first().id}', {}, format='json')
        print(response)
        logging.log(51, response.json())

    @time_of_function
    def test_reply_message_change(self):
        self.create_and_authorization()
        write_text('Проверка-изменение-ответного-комментария')
        comment = self.add_comment()
        add_reply_comment = self.client.post(f'/user/comment/{comment.id}/{self.product.id}', {"text": 'TESTED'},
                                             format='json')
        logging.log(51, add_reply_comment)
        response = self.client.post(f'/user/change-reply-comment/{ReplyComments.objects.first().id}', {"text": "HELLO"},
                                    format='json')
        print(response)
        logging.log(51, response.json())




    # @time_of_function
    # def test_cart_add(self):
    #     write_text('Проверка-добавление-в-корзину')
    #     product = self.create_product()
    #     response = self.client.post(f'/cart/add/{product.id}/', data={'update': 0, "quantity": 2}, format='json')
    #     print(response)
    #     logging.log(51, response.json())
    #
    # @time_of_function
    # def test_cart_delete(self):
    #     write_text('Проверка-удаление-из-корзины')
    #     product = self.create_product()
    #     response = self.client.post(f'/cart/remove/{product.id}/', {}, format='json')
    #     print(response)
    #     logging.log(51, response.json())
    #
    # @time_of_function
    # def test_history_order(self):
    #     self.user = self.create_superuser()
    #     self.client.force_authenticate(user=self.user)
    #     write_text('Проверка-история-заказов')
    #     create_order = self.client.post('/orders/create/', {"description": "test", "paid": "True",
    #                                                         "deliv_address": "Success"}, format='json')
    #     response = self.client.get('/cart/history/', {}, format='json')
    #     print(response)
    #     logging.log(51, response.json())
    #
    # @time_of_function
    # def test_like_products(self):
    #     write_text('Проверка-понравившиеся-товары')
    #     response = self.client.get('/cart/liked/', {}, format='json')
    #     print(response)
    #     logging.log(51, response.json())
