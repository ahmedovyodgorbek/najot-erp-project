from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_common.pagination import StandardResultsSetPagination
from app_common.permissions import IsTeacherOrStudent, IsTeacher
from app_groups.models import GroupModel
from . import models
from . import serializers
from .models import HomeworkTaskModel


class HomeworkTaskCreateAPIView(CreateAPIView):
    queryset = HomeworkTaskModel.objects.all()
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = serializers.HomeworkTaskCreateSerializer

    def perform_create(self, serializer):
        group_slug = self.kwargs.get('slug')
        try:
            group = GroupModel.objects.get(slug=group_slug)
        except GroupModel.DoesNotExist:
            raise ValidationError("Group does not exist.")

        lesson = serializer.validated_data.get('lesson')
        if HomeworkTaskModel.objects.filter(group=group, lesson=lesson).exists():
            raise ValidationError("Task already exists for this lesson in this group.")

        serializer.save(group=group)


class HomeworkTasksListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTeacherOrStudent]
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.HomeworkTaskCreateSerializer

    def get_queryset(self):
        group_slug = self.kwargs['slug']
        return HomeworkTaskModel.objects.filter(group__slug=group_slug).order_by('-id')


class HomeworkSubmissionListCreateAPIView(ListCreateAPIView):
    queryset = models.HomeworkSubmissionModel.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.HomeworkSubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(is_submitted=True, student=self.request.user)
