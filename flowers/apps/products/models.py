from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from apps.catalog.models import Categories


class Products(models.Model):
    title = models.CharField('Название', max_length=150, db_index=True)
    slug = models.SlugField('Слаг', max_length=150, unique=True)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', max_length=1000, blank=True)
    photo = models.ImageField(upload_to="product/%Y/%m/%d", blank=True)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField('Дата появления товара', auto_now_add=True)
    date_uploaded = models.DateTimeField('Дата обновления товара', auto_now=True)
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-date_created']
        index_together = (('id', 'slug'),)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    star = models.SmallIntegerField(verbose_name='star')
    prod = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='stars', verbose_name='prod')

    def __str__(self):
        return '{} {}'.format(self.prod, self.star)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинга'
        ordering = ['prod', '-star']


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    product = models.ForeignKey(Products, related_name='check_review', on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата появления отзыва', auto_now_add=True)
    date_uploaded = models.DateTimeField('Дата обновления отзыва', auto_now=True)

    def __str__(self):
        return f'{self.user} {self.name} {self.text} {self.product}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=5000)
    product = models.ForeignKey(Products, related_name='check_comment', on_delete=models.CASCADE)
    date = models.DateTimeField('Дата комментария', auto_now=True)

    def __str__(self):
        return '{} {} {} {}'.format(self.user, self.text, self.date, self.product)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
