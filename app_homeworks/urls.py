from django.urls import path

from . import views

app_name = 'homeworks'

urlpatterns = [
    path('', views.HomeworkTasksListCreateAPIView.as_view(), name='tasks')
]
