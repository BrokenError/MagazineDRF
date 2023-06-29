from django.urls import path

from apps.users.views import ChangePasswordAPIView, RegisterUserAPIView, logout_user, delete_account, \
    UserSecurityAPIView, UserPersonalAPIView, user_like, ReplyCommentsAPIView, delete_reply_comment, \
    reply_message_change, verify_code

urlpatterns = [
    path('', ChangePasswordAPIView.as_view(), name='user'),
    path('comment/<int:pk_comment>/<int:pk_product>', ReplyCommentsAPIView.as_view(), name='add_comments'),
    path('delete-reply-comment/<int:id>', delete_reply_comment, name='delete-reply-comment'),
    path('product/<int:product_id>/comment/<int:comment_id>/<int:replcomment>', reply_message_change,
         name='change-reply-comment'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('verify/', verify_code, name='verify'),
    path('delete/', delete_account, name='delete-account'),
    path('security/', UserSecurityAPIView.as_view(), name='security'),
    path('personal/', UserPersonalAPIView.as_view(), name='personal'),
    path('like/<int:prod_id>', user_like, name='like'),
]
