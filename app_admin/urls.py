from django.urls import path

from . import views
app_name = 'admin'

urlpatterns = [
    path('', views.AdminListCreateAPIView.as_view(), name='list-create')
]
