from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from .views import TaskAPIView, TaskStats

urlpatterns = [
    path('get_article', TaskAPIView.as_view(), name='get_article'),
    path('create_article', TaskAPIView.as_view(), name='create_article'),
    path('update_article/<int:task_id>', TaskAPIView.as_view(), name='update_article'),
    path('get_article/<int:task_id>', TaskAPIView.as_view(), name='get_article'),
    path('delete_article/<int:task_id>', TaskAPIView.as_view(), name='delete_article'),
    path('article_stats', TaskStats.as_view(), name='article_stats'),
]