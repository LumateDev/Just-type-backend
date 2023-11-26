from django.urls import path
from .views import *

urlpatterns = [

    path('api/user/register', UserViewRegister.as_view(), name='register'),
    path('api/user/login', UserViewLogin.as_view(), name="login")
]