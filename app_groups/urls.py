from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('list-create/', views.GroupListCreateAPIView.as_view(), name='list-create'),
    path('my-groups/', views.MyGroupsListAPIView.as_view(), name='my-groups'),
    path('detail/<slug:slug>/', views.GroupRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
    path('add/user/', views.AddUserToGroupAPIView.as_view(), name='add-user'),
    path('add/subject/', views.AddSubjectToGroupAPIView.as_view(), name='add-subject'),
    path('subject/<slug:slug>/detail/', views.SubjectRetrieveUpdateDestroyAPIView.as_view(), name='subject detail'),
    path('list-create/subject/', views.SubjectListCreateAPIView.as_view(), name='create-subject'),
]
