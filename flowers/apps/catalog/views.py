from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.services import paginator_page
from apps.catalog.services import search_magazine, show_categories, magazine_catalog


class SearchResultAPIView(APIView):
    @staticmethod
    def get(request):
        content = search_magazine(None)
        return Response({'content': content})

    @staticmethod
    def post(request):
        search = request.data['prod_title_search']
        if search:
            content = search_magazine(search)
            return Response({"content": content})


class MagazineCatalogAPIView(APIView):
    @staticmethod
    def get(request):
        content = magazine_catalog()
        paginator = paginator_page(20, content['products'], request)
        return paginator


class ShowCategoriesAPIView(APIView):
    @staticmethod
    def get(request, slug):
        content = show_categories(slug)
        paginator = paginator_page(20, content['products'], request)
        return paginator
