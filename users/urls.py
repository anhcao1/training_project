from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', views.UserLoginView.as_view(), name='user_login'),
    path('register', views.UserRegisterView.as_view(), name='user_register'),
    path('profile', views.UserProfileView.as_view(), name='user_profile'),
]
