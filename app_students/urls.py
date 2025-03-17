from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path("list/", views.StudentListAPIView.as_view(), name='list')
]
