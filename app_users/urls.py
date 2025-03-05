from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('profile/', views.ProfileRetrieveUpdateAPIView.as_view(), name='profile'),
    path('update/password/', views.UpdatePasswordAPIView.as_view(), name='update-password'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
