from django.db import models

from app_common.models import BaseModel


class SubjectModel(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'


class GroupModel(BaseModel):
    title = models.CharField(max_length=128)
    subject = models.ForeignKey(SubjectModel, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='groups')

    def __str__(self):
        return f"{self.title}: {self.subject}"

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
