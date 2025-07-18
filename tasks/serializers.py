from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=Task.status_choices, default='pending', required=False)
    priority = serializers.ChoiceField(choices=Task.priority_choices, default='medium', required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False,
                                                    allow_null=True, default=None)
    created_at = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True, default=None)
    completed = serializers.BooleanField(default=False, required=False)
    
    def create(self, validated_data):
        return Task.objects.create(**validated_data)        

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance