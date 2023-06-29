from django.urls import path

from apps.catalog.views import SearchResultAPIView, ShowCategoriesAPIView, MagazineCatalogAPIView

urlpatterns = [
    path('', MagazineCatalogAPIView.as_view(), name='magazine_catalog'),
    path('search/', SearchResultAPIView.as_view(), name='search_products_page'),
    path('<slug:slug>/', ShowCategoriesAPIView.as_view(), name='selected_category_page'),
]
