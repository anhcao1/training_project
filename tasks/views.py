
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from .models import Task
from .tasks import send_email_task
from .permissions import IsAdminOrManager, IsManagerOrAdminOrOwner
from .serializers import TaskSerializer


class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOrManager()]

        elif self.request.method == 'POST':
            return [IsAuthenticated(), IsManagerOrAdminOrOwner()]

        elif self.request.method in ['PUT']:
            return [IsAuthenticated(), IsManagerOrAdminOrOwner()]

        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        priority = request.GET.get('priority')
        title = request.GET.get('title')
        tasks = Task.objects.all()
        filters = {}
        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if title:
            filters['title__icontains'] = title
        if request.user.groups.filter(name='Staff').exists():
            filters['assignee'] = request.user
        tasks = tasks.filter(**filters)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data, "task_count": tasks.count()}, status=200)

    def post(self, request, *args, **kwargs):
        task = request.data.get('task', {})
        serializer = TaskSerializer(data=task)
        if serializer.is_valid():
            task = serializer.save()
            return Response({"task": TaskSerializer(task).data}, status=201)
        else:
            return Response({"errors": serializer.errors}, status=400)

    def put(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(
            data=request.data.get('task', {}), instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response({"task": serializer.data}, status=200)
        return Response({"errors": serializer.errors}, status=400)

    def delete(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=204)


class TaskStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request, *args, **kwargs):
        last_7_days = now().date() - timedelta(days=7)

        # Filter by last 7 days
        tasks = Task.objects.filter(created_at__date__gte=last_7_days) \
                            .values('status') \
                            .annotate(count=Count('id')) \
                            .order_by('status')

        response_data = [
            {"status": task['status'], "count": task['count']}
            for task in tasks
        ]

        return Response(response_data, status=200)
