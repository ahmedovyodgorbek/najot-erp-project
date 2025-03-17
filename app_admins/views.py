from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from . import serializers
from app_common.permissions import IsSuperAdmin
from app_common.pagination import StandardResultsSetPagination

UserModel = get_user_model()


class UserCreateAPIView(CreateAPIView):
    permission_classes = [IsSuperAdmin, IsAuthenticated]
    serializer_class = serializers.UserCreateSerializer


class UsersListAPIView(ListAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAdminUser]
    queryset = UserModel.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = UserModel.objects.all()
        role = self.request.query_params.get('role')
        if role in ['admin', 'teacher', 'student']:
            queryset = UserModel.objects.filter(role=role)

        return queryset.order_by('-id')
