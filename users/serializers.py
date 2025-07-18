from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=False)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get('email', ''),
            password=validated_data['password'])
        staff_groups = Group.objects.get(name='Staff')
        user.groups.set([staff_groups])
        return user
    
    def validate_username(self, value):
        is_login = self.context.get('is_login', False)
        if not is_login and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value