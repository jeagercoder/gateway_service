from django.conf import settings

from service_lib.services import InternalService


class AuthService(InternalService):

    def get_host(self):
        return settings.AUTH_SERVICE_URL

    def get_headers(self):
        return {'Authorization': settings.AUTH_SERVICE_AUTH}

