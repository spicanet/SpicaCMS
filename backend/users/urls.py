# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    # path('password_reset/', reset_password_request_token, name='password_reset'),
    # path('password_reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
]
