import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from app_common.models import BaseModel
from app_groups.models import GroupModel
from app_lessons.models import LessonModel

UserModel = get_user_model()


def default_deadline():
    return timezone.now() + datetime.timedelta(days=1, hours=12)


class HomeworkTaskModel(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    deadline = models.DateTimeField(default=default_deadline())
    lesson = models.OneToOneField(LessonModel, models.CASCADE, related_name='homework_task')
    group = models.ForeignKey(GroupModel, models.CASCADE, related_name='homework_tasks')

    def __str__(self):
        return f"{self.title} to lesson({self.lesson.title})"

    class Meta:
        verbose_name = 'homework task'
        verbose_name_plural = 'homework tasks'


class HomeworkSubmissionModel(BaseModel):
    homework = models.FileField(upload_to='student/homeworks/', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    task = models.OneToOneField(HomeworkTaskModel, models.CASCADE, related_name='submission')
    student = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                                limit_choices_to={"role": "student"},
                                related_name='homeworks')

    def __str__(self):
        return f"{self.student.username} uploaded {self.homework} for this task: {self.task.title}"

    def is_late(self):
        return self.created_at > self.task.deadline

    class Meta:
        verbose_name = 'homework submission'
        verbose_name_plural = 'homework submissions'
