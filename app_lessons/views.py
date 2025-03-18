from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import serializers
from app_common.pagination import StandardResultsSetPagination
from app_common.permissions import IsTeacherRelatedByGroup, IsTeacherOrAdminOrStudentReadOnly
from .models import LessonModel, AttendanceModel

UserModel = get_user_model()


class LessonCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacherRelatedByGroup]
    serializer_class = serializers.LessonCreateSerializer
    queryset = LessonModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        group = serializer.validated_data['group']
        lesson = LessonModel.objects.create(title=title, group=group)
        lesson_serializer = serializers.LessonCreateSerializer(instance=lesson)
        return Response(lesson_serializer.data, status=status.HTTP_201_CREATED)


class MyLessonsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.MyLessonsSerializer

    def get_queryset(self):
        return LessonModel.objects.filter(group__slug=self.kwargs['slug']).order_by('-id')


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdminOrStudentReadOnly]
    queryset = LessonModel.objects.all()
    serializer_class = serializers.LessonDetailSerializer
    lookup_field = 'slug'


class ManageAttendanceAPIView(ListCreateAPIView):
    serializer_class = serializers.ManageAttendanceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    queryset = AttendanceModel.objects.all()

    def create(self, request, *args, **kwargs):
        lesson_slug = self.kwargs['slug']
        try:
            lesson = LessonModel.objects.get(slug=lesson_slug)
        except LessonModel.DoesNotExist:
            raise ValidationError("Lesson does not exist.")

        if (lesson.group not in request.user.groups.all() and
                request.user.role not in ['teacher', 'admin']):
            raise ValidationError("You do not have permission.")

        data = request.data.copy()
        data['lesson_slug'] = lesson_slug
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response("Attendance created/updated successfully.", status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        lesson_slug = self.kwargs['slug']
        try:
            lesson = LessonModel.objects.get(slug=lesson_slug)
        except LessonModel.DoesNotExist:
            raise ValidationError("Lesson does not exist.")

        if (lesson.group not in request.user.groups.all() and
                request.user.role not in ['teacher', 'admin']):
            raise ValidationError("You do not have permission.")

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.AttendanceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        lesson_slug = self.kwargs['slug']
        try:
            lesson = LessonModel.objects.get(slug=lesson_slug)
        except LessonModel.DoesNotExist:
            raise ValidationError("Lesson does not exist.")
        attendance = AttendanceModel.objects.filter(lesson=lesson)
        return attendance.order_by('-id')

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
