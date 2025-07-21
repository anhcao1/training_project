
from rest_framework import viewsets
from .serializers import TaskModelSerializer
# from rest_framework import generics
from rest_framework import mixins
# from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.utils.timezone import now
from django.db.models import Q
from rest_framework.decorators import action
from datetime import timedelta
from .models import Task
from .permissions import IsAdminOrManager, IsManagerOrAdminOrOwner
from .serializers import TaskStatsSerializer


# class TaskStats(APIView):
#     permission_classes = [IsAdminOrManager]

#     def get(self, request, *args, **kwargs):
#         last_7_days = now().date() - timedelta(days=7)

#         # Filter by last 7 days
#         tasks = Task.objects.filter(created_at__date__gte=last_7_days) \
#                             .values('status') \
#                             .annotate(count=Count('id')) \
#                             .order_by('status')
#         # Convert to a list of dictionaries
#         serializers = TaskStatsSerializer(tasks, many=True)

#         return Response(serializers.data, status=200)


# class TaskListCreateView(generics.ListCreateAPIView):
#     serializer_class = TaskModelSerializer
#     queryset = Task.objects.all()

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         status = self.request.query_params.get('status')
#         q = Q()
#         user = self.request.user
#         if status:
#             q &= Q(status=status)
#         priority = self.request.query_params.get('priority')
#         if priority:
#             q &= Q(priority=priority)
#         title = self.request.query_params.get('title')
#         if title:
#             q &= Q(title__icontains=title)

#         if user.groups.filter(name='Staff').exists():
#             q &= (Q(assignee=user) | Q(owner=user))
#         return queryset.filter(q).order_by('-created_at')

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [IsManagerOrAdminOrOwner()]
#         return [IsAuthenticated()]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskModelSerializer
#     lookup_field = 'id'

#     def get_permissions(self):
#         method = self.request.method
#         if method == 'PUT':
#             return [IsManagerOrAdminOrOwner()]
#         elif method == 'DELETE':
#             return [IsAdminOrManager()]


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    list    → GET    /tasks/           (IsAuthenticated)
    create  → POST   /tasks/           (IsManagerOrAdminOrOwner)
    update  → PUT    /tasks/{id}/      (IsManagerOrAdminOrOwner + object perms)
    partial_update → PATCH /tasks/{id}/(IsManagerOrAdminOrOwner + object perms)
    destroy → DELETE /tasks/{id}/      (IsAdminOrManager)
    """
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsManagerOrAdminOrOwner()]
        if self.action in ('update', 'partial_update'):
            return [IsManagerOrAdminOrOwner()]
        if self.action in ('destroy', 'stats'):
            return [IsAdminOrManager()]

    def get_queryset(self):
        # only applied on list
        if self.action != 'list':
            return super().get_queryset()

        qs = super().get_queryset()
        q = Q()
        user = self.request.user

        for param, lookup in (
            ('status',   'status'),
            ('priority', 'priority'),
            ('title',    'title__icontains'),
        ):
            val = self.request.query_params.get(param)
            if val:
                q &= Q(**{lookup: val})

        if user.groups.filter(name='Staff').exists():
            q &= Q(assignee=user) | Q(owner=user)

        return qs.filter(q).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def stats(self, request):
        last_7_days = now().date() - timedelta(days=7)

        # Filter by last 7 days
        tasks = Task.objects.filter(created_at__date__gte=last_7_days) \
                            .values('status') \
                            .annotate(count=Count('id')) \
                            .order_by('status')
        # Convert to a list of dictionaries
        serializer = TaskStatsSerializer(tasks, many=True)

        return Response(serializer.data, status=200)
