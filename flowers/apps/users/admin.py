from django.contrib import admin
from django.db.models import QuerySet

from apps.products.admin import report_data
from apps.users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'bio', 'birth_date', 'profile_img', 'country', 'city', 'phoneNumber',
                    'is_phone_verified', 'balance']
    list_editable = ['is_phone_verified']
    list_filter = ['birth_date', 'is_phone_verified']
    search_fields = ['username', 'country', 'city']
    actions = ['get_data']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != "none" and cookie_filter:
            text = f"Новых профилей появилось за {cookie_filter}:"
        else:
            text = f"Всего профилей:"
        data = []
        for _ in qs:
            data.append(f'{_.id}: пользователь - {_.username}, дата рождения - {_.birth_date}, страна - {_.country},'
                        f'город - {_.city}, создан - {_.username.date_joined.strftime("%Y-%m-%d %H:%M:%S")}')
        return report_data(qs, text, data)
