from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .jwt_authentication import get_tokens_for_user
from .serializers import UserSerializer


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        response_data = serializer.data
        response_data['refresh'], response_data['access'] = get_tokens_for_user(
            user).values()
        return Response({"user": response_data}, status=status.HTTP_200_OK)


class UserLoginView(APIView):

    def post(self, request):
        user = request.data.get('user', {})
        serializer = UserSerializer(data=user, context={'is_login': True})
        user = authenticate(username=user.get('username'),
                            password=user.get('password'))
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            response_data = UserSerializer(user).data
            response_data['refresh'], response_data['access'] = get_tokens_for_user(
                user).values()
            return Response({"user": response_data}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):

    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response({"user": response_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
