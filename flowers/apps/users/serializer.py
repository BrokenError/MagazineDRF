from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.users.models import Profile, ReplyComments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   password=validated_data['password'])
        return user


class SaveDataUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User, Profile
        fields = ("first_name", "last_name", "bio", "country", "city", "birth_date")


class AddPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("phoneNumber",)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Введите смс, отправленное на ваш телефон')


class ReplyCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComments
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
