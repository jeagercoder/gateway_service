from django.urls import path, include


urlpatterns = [
    path('auth/', include(('auth_service.urls', 'auth'), namespace='auth'))
]
