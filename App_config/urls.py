"""
URL configuration for App_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from App_config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Najot Ta'lim erp API",
        default_version='v1',
        description="Project for exam",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ahmedov.python@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication]
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    # path('admin/', admin.site.urls),
    path('api/v1/admins/', include('app_admins.urls', namespace='admin')),
    path('api/v1/students/', include('app_students.urls', namespace='students')),
    path('api/v1/teachers/', include('app_teachers.urls', namespace='teachers')),
    path('api/v1/groups/', include('app_groups.urls', namespace='groups')),
    path('api/v1/lessons/', include('app_lessons.urls', namespace='lessons')),
    path('api/v1/authentication/', include('app_authentication.urls', namespace='authentication')),
    path('api/v1/homeworks/', include('app_homeworks.urls', namespace='homeworks'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
