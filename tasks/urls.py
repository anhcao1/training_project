from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from .views import TaskStats, TaskCreateView,TaskDeleteView, TaskUpdateView, TaskListView

urlpatterns = [
    # path('create_article', TaskAPIView.as_view(), name='create_article'),
    path('create_article', TaskCreateView.as_view(), name='create_article'),
    path('get_article', TaskListView.as_view(), name='list_article'),
    path('update_article/<int:id>', TaskUpdateView.as_view(), name='update_article'),
    path('delete_article/<int:id>', TaskDeleteView.as_view(), name='delete_article'),
    path('article_stats', TaskStats.as_view(), name='article_stats'),
]