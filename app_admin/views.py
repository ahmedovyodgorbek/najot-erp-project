from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from app_common.permissions import IsSuperAdmin
from app_common.pagination import StandardResultsSetPagination

UserModel = get_user_model()


class AdminListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperAdmin, IsAuthenticated]
    serializer_class = serializers.AdminCreateSerializer
    queryset = UserModel.objects.all()
    pagination_class = StandardResultsSetPagination
