# Generated by Django 5.1.6 on 2025-03-02 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_lessons', '0001_initial'),
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='app_lessons.groupmodel'),
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]
