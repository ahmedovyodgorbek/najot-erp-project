from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import LessonModel, AttendanceModel
from app_groups.models import GroupModel
from app_homeworks.models import HomeworkSubmissionModel, HomeworkTaskModel
from app_homeworks.serializers import HomeworkTaskSerializer

UserModel = get_user_model()


class LessonDetailSerializer(serializers.ModelSerializer):
    group_title = serializers.CharField(source='group.title')
    task = serializers.SerializerMethodField()
    my_submission = serializers.SerializerMethodField()

    class Meta:
        model = LessonModel
        fields = ['title', 'slug', 'group_title', 'video', 'created_at',
                  'task', 'my_submission']

    def get_task(self, obj):
        task = HomeworkTaskModel.objects.filter(lesson=obj).first()
        task_serializer = HomeworkTaskSerializer(task)
        return task_serializer.data

    def get_my_submission(self, obj):
        task = HomeworkTaskModel.objects.filter(lesson=obj).first()
        submission = HomeworkSubmissionModel.objects.filter(task=task).first()


class MyLessonsSerializer(serializers.ModelSerializer):
    homework_status = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    class Meta:
        model = LessonModel
        fields = ['title', 'homework_status', 'deadline', 'created_at']

    def get_homework_status(self, obj):
        student = self.context['request'].user
        task = getattr(obj, 'homework_task', None)
        if not task:
            return "No homework assigned"
        try:
            submission = HomeworkSubmissionModel.objects.get(task=task, student=student)
        except HomeworkSubmissionModel.DoesNotExist:
            return False
        return submission.is_submitted

    def get_deadline(self, obj):
        task = getattr(obj, 'homework_task', None)
        if not task:
            return None
        return task.deadline if task else None


class LessonCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    group = serializers.CharField(max_length=255)

    def validate(self, attrs):
        title = attrs.get('title')
        group = attrs.get('group')

        try:
            group = GroupModel.objects.get(title=group)
        except GroupModel.DoesNotExist:
            raise serializers.ValidationError("Group does not exist")
        attrs['group'] = group
        return attrs


class ManageAttendanceSerializer(serializers.Serializer):
    student_username = serializers.CharField()
    lesson_slug = serializers.CharField()

    def validate(self, attrs):
        student_username = attrs.get('student_username')
        lesson_slug = attrs.get('lesson_slug')

        try:
            student = UserModel.objects.get(username=student_username)
            lesson = LessonModel.objects.get(slug=lesson_slug)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User was not found")
        except LessonModel.DoesNotExist:
            raise serializers.ValidationError("Lesson was not found")
        attrs['student'] = student
        attrs['lesson'] = lesson
        return attrs

    def create(self, validated_data):
        student = validated_data.pop('student')
        lesson = validated_data.pop('lesson')

        attendance, created = AttendanceModel.objects.get_or_create(
            student=student, lesson=lesson,
            defaults={'status': 'present'}
        )
        if not created:
            attendance.status = 'present' if attendance.status == 'absent' else 'absent'
            attendance.save()
        return attendance


class AttendanceSerializer(serializers.ModelSerializer):
    lesson = serializers.CharField(source='lesson.title', read_only=True)
    student = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = AttendanceModel
        fields = ['lesson', 'student', 'status']
