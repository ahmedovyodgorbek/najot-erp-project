from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from app_common.pagination import StandardResultsSetPagination
from . import models
from . import serializers


class HomeworkTasksListCreateAPIView(ListCreateAPIView):
    queryset = models.HomeworkTaskModel.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.HomeworkTaskSerializer
