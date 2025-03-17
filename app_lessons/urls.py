from django.urls import path

from . import views

app_name = 'lessons'

urlpatterns = [
    path("create/", views.LessonCreateAPIView.as_view(), name='create'),
    path("<slug:slug>/my-lessons/", views.MyLessonsListAPIView.as_view(), name='my-lessons'),
    path("<slug:slug>/", views.LessonRetrieveUpdateDestroyAPIView.as_view(), name='detail')
]
