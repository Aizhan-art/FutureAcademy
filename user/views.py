from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout

from .serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"detail": "Успешный вход"}, status=status.HTTP_202_ACCEPTED)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Успешный выход"}, status=status.HTTP_200_OK)
