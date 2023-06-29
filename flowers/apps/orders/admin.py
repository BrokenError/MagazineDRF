from django.contrib import admin
from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem
from apps.products.admin import report_data


class CategoriesAdmin(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'deliv_address', 'created', 'description', 'paid']
    list_display_links = ('id', 'created')
    list_filter = ['created', 'paid']
    search_fields = ['user', 'deliv_address']
    inlines = [CategoriesAdmin]
    actions = ['get_data']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Новых заказов появилось за {cookie_filter}:"
        else:
            text = f"Всего заказов:"
        data = []
        for _ in qs:
            if _.paid:
                paid = "оплачен"
            else:
                paid = "не оплачен"
            data.append(f'{_.id}: пользователь - {_.user}, адресс доставки - "{_.deliv_address}",'
                        f' описание - "{_.description}", заказ - {paid},'
                        f' создан - {_.created.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)
