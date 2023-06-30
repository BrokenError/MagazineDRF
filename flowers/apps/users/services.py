from django.contrib.auth.models import User
from django.http import Http404

from apps.users.models import UserLike, ReplyComments
from apps.products.models import Products, Comments
from apps.users.serializer import ReplyCommentsSerializer, AddPhoneSerializer, RegisterUserSerializer, \
    SaveDataUserSerializer


def reply_comment(user, data):
    serializer = ReplyCommentsSerializer(data=data)
    valid = serializer.is_valid(raise_exception=True)
    if valid:
        ReplyComments.objects.create(user=user, text=serializer.data['text'],
                                     product=Products.objects.get(pk=data['product']),
                                     comment=Comments.objects.get(pk=data['comment']))
        return serializer.data
    return valid


def register_user(data):
    register = RegisterUserSerializer(data=data)
    valid_data = register.is_valid(raise_exception=True)
    if valid_data:
        register.create(validated_data=data)
        return register.data
    return valid_data


def change_user_info(user_profile, data):
    serializer = SaveDataUserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.update(instance=user_profile, validated_data=data)
        return {"success": "Данные успешно обновлены", "results": serializer.data}
    else:
        return {"errors": serializer.errors}


def delete_user(user_id):
    try:
        User.objects.get(pk=user_id).delete()
    except Exception:
        raise Http404


def like_product(like, user):
    obj, create = UserLike.objects.get_or_create(user=user, product_id=like)
    if not create:
        obj.delete()
