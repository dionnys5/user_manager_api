from django.db.models import fields, manager
from rest_framework import serializers
from web.models import CustomUser, Phone
from django.db import IntegrityError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    default_error_messages = {
        'no_active_account': ('Invalid e-mail or password')
    }

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['firstName'] = self.user.firstName
        data['lastName'] = self.user.lastName
        update_last_login(None, self.user)
        return data

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, write_only=True, max_length=32)

class PhoneSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=True)
    area_code = serializers.IntegerField(required=True)
    country_code = serializers.CharField(required=True, allow_blank=False, max_length=3)


class GetMyUserSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'firstName', 'lastName', 'email', 'last_login', 'phones']


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    firstName = serializers.CharField(required=True, allow_blank=False, max_length=255)
    lastName = serializers.CharField(required=True, allow_blank=False, max_length=255)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, write_only=True, max_length=32)
    phones = serializers.ListField(child=PhoneSerializer())

    def create(self, validated_data):
        try:
            phones = validated_data.pop('phones', None)
            psw = validated_data.pop('password', None)
            user = CustomUser(**validated_data)
            user.set_password(psw)
            user.save()
            phones = [Phone(user=user, **phone) for phone in phones]
            Phone.objects.bulk_create(phones)
        except IntegrityError:
            return {'success': False, 'message': 'E-mail already exists'}
        return {'success':True, 'user': user}
