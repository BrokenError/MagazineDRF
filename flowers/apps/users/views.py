from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.services import change_reply_comment
from apps.users.models import ReplyComments
from apps.users.serializer import AddPhoneSerializer, ChangePasswordSerializer, UserSerializer, SaveDataUserSerializer
from apps.users.services import like_product, reply_comment, delete_user, register_user, change_user_info


class RegisterUserAPIView(APIView):
    @staticmethod
    def post(request):
        content = register_user(request.data)
        return Response({"result": content})


@api_view(["POST"])
def verify_code(request):
    serializer = AddPhoneSerializer(data=request.data, instance=request.user.user_profile)
    valid = serializer.is_valid(raise_exception=True)
    if valid:
        request.user.user_profile.is_phone_verified = True
        request.user.save()
        return Response({"success": "Успешно добавлен номер телефона"})
    return Response({"errors": valid})


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"success": "Пароль успеншно обновлен"})
        return Response(serializer.is_valid(), status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(APIView):
    @staticmethod
    @login_required
    def get(request):
        return Response({"user": UserSerializer(request.user).data})


class UserPersonalAPIView(APIView):
    @staticmethod
    @login_required
    def get(request):
        return Response({"user": UserSerializer(request.user).data,
                         'profile': SaveDataUserSerializer(request.data).data})

    @staticmethod
    @login_required
    def post(request):
        content = change_user_info(request.user.user_profile, request.data)
        return Response(content)


class UserSecurityAPIView(APIView):
    @staticmethod
    @login_required
    def get(request):
        return Response({"user": UserSerializer(request.user).data})


@api_view(['GET', 'POST'])
def logout_user(request):
    logout(request)
    return Response({"success": "Вы вышли из своего аккаунта"})


@api_view(['GET', 'POST'])
def delete_account(request):
    delete_user(request.user.id)
    return Response({"success": "Успешно удален аккаунт"})


@api_view(['GET'])
def user_like(request, prod_id):
    like_product(prod_id, request.user)
    return Response({"success": "успешно"})


class ReplyCommentsAPIView(APIView):
    @staticmethod
    def post(request, pk_comment, pk_product):
        request.data['user'] = request.user.id
        request.data['product'] = pk_product
        request.data['comment'] = pk_comment
        result = reply_comment(request.user, request.data)
        return Response(result)


@api_view(['GET', 'POST'])
def delete_reply_comment(request, pk_reply_comment):
    ReplyComments.objects.get(pk=pk_reply_comment).delete()
    return Response({"result": 'Ответный комментарий удален'})


@api_view(['POST'])
def reply_message_change(request, replcomment):
    request.data['user'] = request.user.id
    change_reply_comment(request.data, replcomment)
    return Response({"result": "Ответный комментарий изменен"})
