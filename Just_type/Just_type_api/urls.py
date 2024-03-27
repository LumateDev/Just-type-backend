from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [

    path('api/user/register', UserViewRegister.as_view(), name='register'),
    path('api/user/login', UserViewLogin.as_view(), name="login"),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('api/errors', UserErrorView.as_view(), name='errors'),
    path('api/errors/<int:pk>', UserErrorView.as_view(), name='get_errors'),
    path('api/errors/reset/<int:pk>', UserErrorView.as_view(), name='get_errors'),
    path('api/user/data', UserDataView.as_view(), name='user_data'),
    path('api/user/data/<int:pk>', UserDataView.as_view(), name='get_data'),

]
