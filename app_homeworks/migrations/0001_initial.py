# Generated by Django 5.1.6 on 2025-03-11 18:26

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_lessons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkTaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('deadline', models.DateTimeField(default=datetime.datetime(2025, 3, 13, 6, 26, 38, 597308, tzinfo=datetime.timezone.utc))),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_tasks', to='app_lessons.lessonmodel')),
            ],
            options={
                'verbose_name': 'homework task',
                'verbose_name_plural': 'homework tasks',
            },
        ),
        migrations.CreateModel(
            name='HomeworkSubmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('homework', models.FileField(blank=True, null=True, upload_to='student/homeworks/')),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_submitted', models.BooleanField(default=False)),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to=settings.AUTH_USER_MODEL)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='app_homeworks.homeworktaskmodel')),
            ],
            options={
                'verbose_name': 'homework submission',
                'verbose_name_plural': 'homework submissions',
            },
        ),
    ]
