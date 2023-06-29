import os
from datetime import datetime

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from apps.products.models import Products, Reviews, Comments


def report_data(qs: QuerySet, text, data):
    file = os.path.abspath('simple_demo.pdf')
    font = os.path.abspath('ffont.ttf')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"Report {date}"

    response = HttpResponse(content_type=file)
    response['Content-Disposition'] = f'attachment; filename={filename}'
    pages = canvas.Canvas(response, pagesize=(900.0, 1080.0))
    pdfmetrics.registerFont(TTFont('text', font, 'UTF-8'))
    pages.setFont("text", 12)
    pages.setTitle(f"Отчет за {date}")
    pages.drawString(20, 1050, f"{text} {qs.count()}шт")
    y = 1000
    for _ in data:
        pages.drawString(20, y, _)
        y -= 30
    pages.showPage()
    pages.save()
    return response


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'cat', 'image_show', 'price', 'available', 'date_created', 'date_uploaded']
    list_editable = ['price', 'available']
    list_filter = ['date_created', 'date_uploaded']
    list_display_links = ['id']
    actions = ['get_data']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

    def image_show(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='50' />".format(obj.photo.url))
        return 'None'

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Товаров за {cookie_filter} появилось в продаже:"
        else:
            text = f"Всего товаров:"
        data = []
        for _ in qs:
            data.append(f'{_.id}: "{_.title}", {_.price} ₽, создан - {_.date_created.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)

    image_show.__name__ = "Картинка"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'text', 'product', 'date_created', 'date_uploaded']
    list_filter = ['date_created', 'date_uploaded']
    list_display_links = ['id']
    actions = ['get_data']
    search_fields = ['user', 'text']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Появилось новых отзывов за {cookie_filter}:"
        else:
            text = f"Всего отзывов:"
        data = []
        for _ in qs:
            data.append(f'{_.id}: пользователь - {_.user}, название - "{_.name}", сообщение: "'
                        f'{_.text}", продукт - {_.product.title},'
                        f' обновлен - {_.date_uploaded.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'product', 'date']
    list_display_links = ['id']
    list_filter = ['date']
    actions = ['get_data']
    search_fields = ['user', 'text']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Новых комментариев появилось за {cookie_filter}:"
        else:
            text = f"Всего комментариев:"
        data = []
        for _ in qs:
            data.append(f'{_.id}: пользователь - {_.user}, сообщение - "{_.text}", продукт - {_.product},'
                        f' создан - {_.date.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)
