from django.conf import settings

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny

from service_lib.helper import AuthHelper
from service_lib.auth_service.utils.auth import logout

from .serializers import (
    LoginSerializers,
    RegisterSerializer,
    RegisterVerifyOtpSerializer
)


class AccountViewSet(GenericViewSet):
    serializer_class = LoginSerializers

    def get_permissions(self):
        if self.action in ['register', 'login', 'register_otp']:
            return [AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializers
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'register_otp':
            return RegisterVerifyOtpSerializer
        return super().get_serializer_class()

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        logout(request.auth)
        response = Response()
        response.delete_cookie(key='session',
                               domain=settings.HOST_NAME,
                               samesite=settings.SAMESITE)
        return response

    @action(methods=['POST'], detail=False)
    def register_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data, status_code = serializer.save()
            return Response(data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data, status_code = serializer.save()
            return Response(data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def profile(self, request):
        route = f'/internal/api/v1/account/{request.user.uuid}/profile'
        helper = AuthHelper(route=route)
        helper.get_json()
        return Response(helper.response_json, status=helper.status_code)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data, status_code = serializer.save()
            if status_code == 200 and 'session' in data:
                response = Response(data, status=status_code)
                response.set_cookie(
                    key='session',
                    value=data.get('session'),
                    secure=settings.SECURE,
                    httponly=settings.HTTPONLY,
                    samesite=settings.SAMESITE,
                    domain=settings.HOST_NAME
                )
                return response
            else:
                return Response(data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


