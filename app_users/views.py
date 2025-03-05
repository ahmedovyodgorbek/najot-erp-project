from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, UpdateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_common.permissions import IsOwnerOrReadOnly
from . import serializers

UserModel = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CreateUserSerializer


class LoginAPIView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = user.get_tokens()

        return Response(data=tokens, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = serializers.ProfileUpdateSerializer

    def get_object(self):
        return self.request.user


class UpdatePasswordAPIView(APIView):
    serializer_class = serializers.UpdatePasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"detail": "Your password was successfully updated"},
                        status=status.HTTP_202_ACCEPTED)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
