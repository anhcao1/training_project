from .views import (
    TaskViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')

urlpatterns = [
] + router.urls
