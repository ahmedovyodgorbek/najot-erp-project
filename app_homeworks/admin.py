from django.contrib import admin

from .models import HomeworkTaskModel, HomeworkSubmissionModel

admin.site.register(HomeworkTaskModel)
admin.site.register(HomeworkSubmissionModel)
