from django.contrib.auth import get_user_model
from django.db import models

from app_common.models import BaseModel
from app_groups.models import GroupModel

UserModel = get_user_model()


class LessonModel(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    video = models.FileField(upload_to='lessons/', null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name='lessons')
    ended_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title}  in group {self.group.title}"

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'


class AttendanceModel(BaseModel):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )
    lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    def __str__(self):
        return f"{self.lesson.title} attendances"

    class Meta:
        unique_together = ('lesson', 'student')
        verbose_name = 'attendance'
        verbose_name_plural = 'attendances'
