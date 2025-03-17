from django.apps import AppConfig


class AppLessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_lessons'

    def ready(self):
        from . import signals
