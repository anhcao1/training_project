
from .serializers import TaskModelSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.timezone import now
from django.db.models import Q
from datetime import timedelta
from .models import Task
from .tasks import send_email_task
from .permissions import IsAdminOrManager, IsManagerOrAdminOrOwner
from .serializers import TaskStatsSerializer


class TaskStats(APIView):
    permission_classes = [IsAdminOrManager]

    def get(self, request, *args, **kwargs):
        last_7_days = now().date() - timedelta(days=7)

        # Filter by last 7 days
        tasks = Task.objects.filter(created_at__date__gte=last_7_days) \
                            .values('status') \
                            .annotate(count=Count('id')) \
                            .order_by('status')
        # Convert to a list of dictionaries
        serializers = TaskStatsSerializer(tasks, many=True)

        return Response(serializers.data, status=200)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsManagerOrAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        q = Q()
        user = self.request.user
        if status:
            q &= Q(status=status)
        priority = self.request.query_params.get('priority')
        if priority:
            q &= Q(priority=priority)
        title = self.request.query_params.get('title')
        if title:
            q &= Q(title__icontains=title)

        if user.groups.filter(name='Staff').exists():
            q &= (Q(assignee=user) | Q(owner=user))
        return queryset.filter(q).order_by('-created_at')


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsManagerOrAdminOrOwner]
    lookup_field = 'id'


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsAdminOrManager]
    lookup_field = 'id'
