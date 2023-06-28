from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register

from apps.catalog.models import Categories
from apps.products.models import Products, Rating
from apps.users.models import UserLike


def get_like_and_rating(content):
    content.update(get_rating_catalog(content))
    content.update(show_like_product(content))
    return content


def search_magazine(query):
    if query:
        products = Products.objects.filter(Q(title__icontains=query) or Q(slug__icontains=query))
        content = {'products': products.values()}
        content.update(get_like_and_rating(content))
        return content


def magazine_catalog():
    prod = Products.objects.order_by('date_created')
    content = {'products': prod.values()}
    content.update(get_rating_catalog(content))
    content.update(show_like_product(content))
    return content


def show_categories(slug):
    cater = get_object_or_404(Categories, slug=slug)
    prod = Products.objects.filter(cat=cater.id).order_by('date_created')
    content = {'products': prod.values()}
    content.update(get_like_and_rating(content))
    return content


def get_rating_catalog(content):
    for product in content['products']:
        product.update({"grade": Rating.objects.filter(prod=product['id']).aggregate(Avg('star')).get('star__avg')})
    return content


def show_like_product(content):
    for product in content['products']:
        product.update({"like": UserLike.objects.filter(id=product['id']).exists()})
    return content


@register.filter
def rating(h, key):
    return h[key]
