from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app_common.serializers import UserSerializer
from app_common.pagination import StandardResultsSetPagination

UserModel = get_user_model()


class StudentListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = UserModel.objects.filter(role="student")
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | Q(username__icontains=search)
            )
        return queryset.order_by('-id')
