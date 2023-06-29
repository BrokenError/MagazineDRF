from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Products, Reviews, Comments
from apps.products.serializers import ReviewSerializer, CommentSerializer
from apps.products.services import get_location_user, take_location, base_content, valid_serializer, rate_the_product


class MainAPIView(APIView):
    @staticmethod
    def get(request):
        slider = Products.objects.all().values()
        return Response({'slider': list(slider)})


class AboutUsAPIView(APIView):
    pass


class ShopsAPIView(APIView):
    @staticmethod
    def get(request):
        content = take_location(request)
        content.update(get_location_user(content))
        return Response({'content': content})


class ShowReviewsAPIView(APIView):
    def get(self, request, prod_slug):
        content = base_content(self, {'prod_slug': prod_slug})
        content.update({'reviews': Reviews.objects.filter(product=content['product']['id']).
                       order_by('-date_uploaded').values()})
        return Response({'content': content})


class ShowCommentsAPIView(APIView):
    def get(self, request, prod_slug):
        content = base_content(self, {'prod_slug': prod_slug})
        content.update({'comments': Comments.objects.filter(product=content['product']['id']).
                       order_by('-date').values()})
        return Response({'content': content})


@login_required
class AddReviewsAPIView(APIView):
    @staticmethod
    def post(request, pk):
        request.data['user'] = request.user.id
        request.data['product'] = pk
        review = valid_serializer(ReviewSerializer(data=request.data))
        return Response({'result': review})


@login_required
class AddCommentsAPIView(APIView):
    @staticmethod
    def post(request, pk):
        request.data['user'] = request.user.id
        request.data['product'] = pk
        comment = valid_serializer(CommentSerializer(data=request.data))
        return Response({'result': comment})


@login_required
class ChangeReviewAPIView(APIView):
    @staticmethod
    def get(request, product_id, review_id):
        return Response({'comment': Reviews.objects.filter(product_id=product_id).filter(id=review_id).values()})

    @staticmethod
    def post(request, product_id, review_id):
        request.data['user'] = request.user.id
        request.data['product'] = product_id
        request.data['review_id'] = review_id
        review = valid_serializer(ReviewSerializer(data=request.data,
                                                   instance=Reviews.objects.get(product_id=product_id)))
        return Response({'result': review})


@login_required
class ChangeCommentAPIView(APIView):
    @staticmethod
    def get(request, product_id, comment_id):
        return Response({'comment': Comments.objects.filter(product_id=product_id).filter(id=comment_id).values()})

    @staticmethod
    def post(request, product_id, comment_id):
        request.data['user'] = request.user.id
        request.data['product'] = product_id
        request.data['comment_id'] = comment_id
        comment = valid_serializer(ReviewSerializer(data=request.data,
                                                    instance=Comments.objects.get(product_id=product_id)))
        return Response({'result': comment})


@login_required
class DeleteReviewAPIView(APIView):
    @staticmethod
    def post(request, review_id):
        Reviews.objects.get(id=review_id).delete()
        return Response({'result': f'Отзыв {review_id} успешно удален'})


@login_required
class DeleteCommentAPIView(APIView):
    @staticmethod
    def post(request, comment_id):
        Comments.objects.get(id=comment_id).delete()
        return Response({"result": f'Комментарий {comment_id} успешно удален'})


@login_required
class GradeProductAPIView(APIView):
    @staticmethod
    def post(request, product_id):
        rate_the_product(product_id, request.user, request.data['grade'])
        return Response({'result': 'Оценка успешно поставлена'})
