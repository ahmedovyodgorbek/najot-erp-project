from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path("list/", views.TeacherListAPIView.as_view(), name='list')
]
