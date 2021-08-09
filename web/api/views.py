from web.models import CustomUser, Phone
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from web.api.serializers import (
    CustomUserSerializer, 
    CustomTokenObtainPairSerializer,
    PhoneSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from django.core import serializers


class Me(APIView):
    def get(self, request, format=None):
        user = CustomUser.objects.get(email=request.user.email)
        phones = PhoneSerializer(
            data=list(Phone.objects.filter(user=user).values('area_code', 'number','country_code')),
            many=True
        )
        phones.is_valid()
        ctx = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'last_login': user.last_login,
            'phones': phones.validated_data
        }
        return JsonResponse(ctx)


class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            saved_data = serializer.save()
            if not saved_data['success']:
                return JsonResponse(
                    {'message': saved_data['message'], 'codeError': 409}, status=status.HTTP_409_CONFLICT)
            user = saved_data['user']
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'email': user.email,
                'firstName': user.firstName,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            error_ctx = {
                'codeError': status.HTTP_400_BAD_REQUEST,
                'errorDetails': serializer.errors
            }
            errors = []
            for values in serializer.errors.values():
                errors += [value[:] for value in values]
            if 'This field is required.' in errors:
                error_ctx['message'] = 'Missing fields'
                return JsonResponse(error_ctx, status=status.HTTP_400_BAD_REQUEST)
            error_ctx['message'] = 'Invalid fields'
            return JsonResponse(error_ctx, status=status.HTTP_400_BAD_REQUEST)
            


class Signin(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'codeError': 400, 'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST
                    )
        except TokenError as e:
            raise InvalidToken(e.args[0])

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
