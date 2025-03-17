from django.urls import path

from . import views

app_name = 'homeworks'

urlpatterns = [
    path('<slug:slug>/create/', views.HomeworkTaskCreateAPIView.as_view(), name='create'),
    path('submission/', views.HomeworkSubmissionListCreateAPIView.as_view(), name='submission'),
    path('<slug:slug>/', views.HomeworkTasksListAPIView.as_view(), name='list'),
]
