from rest_framework import serializers

from app_groups.models import GroupModel
from app_lessons.models import LessonModel
from . import models
from .models import HomeworkTaskModel


class HomeworkTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkTaskModel
        fields = ['title', 'description', 'deadline']



class HomeworkTaskCreateSerializer(serializers.ModelSerializer):
    lesson = serializers.SlugRelatedField(
        queryset=LessonModel.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = HomeworkTaskModel
        fields = ['id', 'title', 'description', 'deadline', 'lesson']
        read_only_fields = ['group']


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    is_late = serializers.SerializerMethodField()

    class Meta:
        model = models.HomeworkSubmissionModel
        fields = ['id', 'homework', 'comment', 'is_submitted', 'task', 'student', 'is_late']
        read_only_fields = ['student']

    def get_is_late(self, obj):
        return obj.is_late()
