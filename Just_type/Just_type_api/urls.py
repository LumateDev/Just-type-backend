from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [

    path('api/user/register', UserViewRegister.as_view(), name='register'),
    path('api/user/login', UserViewLogin.as_view(), name="login"),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh')
]