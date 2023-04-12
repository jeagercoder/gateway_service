from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from service_lib.auth_service.utils.auth import logout
from service_lib.views import ServiceViewSet

from .services import AuthService


class AccountViewSet(ServiceViewSet):
    service_class = AuthService
    route = '/internal/api/v1/account/login'

    def get_route(self):
        if self.action == 'profile':
            return f'/internal/api/v1/account/{self.request.user.uuid}/profile'
        elif self.action == 'logout':
            return f'/internal/api/v1/account/logout'
        elif self.action == 'register':
            return f'/internal/api/v1/account/register'
        elif self.action == 'register_otp':
            return f'/internal/api/v1/account/register_otp'
        return super(AccountViewSet, self).get_route()

    def get_service_class(self, **kwargs):
        return super(AccountViewSet, self).get_service_class()

    def get_permissions(self):
        if self.action in ['register', 'login', 'register_otp']:
            return [AllowAny()]
        return super().get_permissions()

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        logout(request.auth)
        response = Response()
        response.delete_cookie(key='session',
                               domain=settings.HOST_NAME,
                               samesite=settings.SAMESITE)

    @action(methods=['POST'], detail=False)
    def register_otp(self):
        service = self.get_service()
        return service.post_json()

    @action(methods=['POST'], detail=False)
    def register(self):
        service = self.get_service()
        return service.post_json()

    @action(methods=['GET'], detail=False)
    def profile(self):
        service = self.get_service()
        return service.get_json()

    @action(methods=['POST'], detail=False)
    def login(self):
        service = self.get_service()
        resp = service.post_json()
        if resp.status_code == 200:
            response = Response(data=resp.data, status=resp.status_code)
            response.set_cookie(
                key='session',
                value=resp.data.get('session'),
                secure=settings.SECURE,
                httponly=settings.HTTPONLY,
                samesite=settings.SAMESITE,
                domain=settings.HOST_NAME
            )
            return response
        return resp

