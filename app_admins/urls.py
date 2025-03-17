from django.urls import path

from . import views

app_name = 'admins'

urlpatterns = [
    # endpoint that creates admin, student, teacher
    path('create/user/', views.UserCreateAPIView.as_view(), name='create-user'),

    path('users/', views.UsersListAPIView.as_view(), name='users'),
]
