from django.db import models
from django.urls import reverse


class Categories(models.Model):
    title = models.CharField('Название', max_length=50, db_index=True)
    slug = models.SlugField('Слаг', max_length=50, unique=True)
    date = models.DateTimeField('Дата появления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-date']
