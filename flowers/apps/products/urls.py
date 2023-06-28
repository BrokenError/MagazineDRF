from django.urls import path, include

from apps.products.views import MainAPIView, AboutUsAPIView, ShopsAPIView, ShowReviewsAPIView, ShowCommentsAPIView, \
    AddReviewsAPIView, AddCommentsAPIView, ChangeReviewAPIView, ChangeCommentAPIView, DeleteReviewAPIView, \
    DeleteCommentAPIView, GradeProductAPIView

urlpatterns = [
    path('', MainAPIView.as_view(), name='magazine_home'),
    path('auth/', include('rest_framework.urls'), name='login_logout'),
    path('aboutus/', AboutUsAPIView.as_view(), name='about_us_page'),
    path('catalog/', include('apps.catalog.urls'), name='catalog_app'),
    path('orders/', include('apps.orders.urls')),
    path('user/', include('apps.users.urls'), name='users_app'),
    path('our-shops/', ShopsAPIView.as_view(), name='our_shops_page'),
    path('reviews/<slug:prod_slug>/', ShowReviewsAPIView.as_view(), name='product'),
    path('comments/<slug:prod_slug>/', ShowCommentsAPIView.as_view(), name='product_comments'),
    path('add-review/<int:pk>', AddReviewsAPIView, name='review'),
    path('add-comment/<int:pk>', AddCommentsAPIView, name='comment'),
    path('change-review/<int:product_id>/<int:review_id>', ChangeReviewAPIView, name='change_review'),
    path('change-comment/<int:product_id>/<int:comment_id>', ChangeCommentAPIView, name='change_comment'),
    path('delete-review/<int:review_id>', DeleteReviewAPIView, name='delete_review'),
    path('delete-comment/<int:comment_id>', DeleteCommentAPIView, name='delete_comment'),
    path('give-grade/<int:product_id>', GradeProductAPIView, name='give_grade'),
    path('cart/', include('apps.cart.urls')),
]
