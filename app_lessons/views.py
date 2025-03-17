from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import serializers
from app_common.pagination import StandardResultsSetPagination
from app_common.permissions import IsTeacherRelatedByGroup, IsTeacherOrAdminOrStudentReadOnly
from .models import LessonModel

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
        lesson_serializer = serializers.LessonSerializer(instance=lesson)
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
    serializer_class = serializers.LessonSerializer
    lookup_field = 'slug'
