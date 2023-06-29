from django.contrib import admin
from django.db.models import QuerySet

from apps.catalog.models import Categories
from apps.products.admin import report_data


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'date']
    list_display_links = ('id', 'title')
    list_filter = ['date']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['get_data']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Новых категорий за {cookie_filter}:"
        else:
            text = f"Всего категорий:"
        data = []
        for _ in qs:
            data.append(f'{_.id}: название - "{_.title}", перевод - "{_.slug}",'
                        f' создана - {_.date.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)
