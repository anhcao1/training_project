from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskStatsSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50)
    count = serializers.IntegerField()


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'completed')
        extra_kwargs = {
            'owner': {'read_only': True},
            'assignee': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_blank': True},
            'status': {'required': False, 'default': 'pending'},
            'priority': {'required': False, 'default': 'medium'},
            'due_date': {'required': False, 'allow_null': True},
            'completed': {'required': False, 'default': False}
        }
