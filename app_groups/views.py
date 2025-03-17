from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from app_common.serializers import UserSerializer
from app_groups.models import GroupModel, SubjectModel
from . import serializers
from app_common.pagination import StandardResultsSetPagination
from app_common.permissions import IsGroupMember

UserModel = get_user_model()


class GroupListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = serializers.GroupsSerializer
    queryset = GroupModel.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination


class MyGroupsListAPIView(ListAPIView):
    serializer_class = serializers.GroupsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        groups = self.request.user.groups.all()
        return groups


class GroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsGroupMember]
    serializer_class = serializers.GroupDetailSerializer
    queryset = GroupModel.objects.all()
    lookup_field = 'slug'


class SubjectListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = serializers.SubjectSerializer
    queryset = SubjectModel.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination


class AddUserToGroupAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = serializers.AddUserToGroupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        group = serializer.validated_data['group']
        user.groups.add(group)
        return Response(data=f"{user.username} has been added to {group.title}", status=status.HTTP_202_ACCEPTED)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class AddSubjectToGroupAPIView(APIView):
    serializer_class = serializers.AddSubjectToGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.validated_data['group']
        subject = serializer.validated_data['subject']
        group.subject = subject
        group.save()
        return Response(data="Subject has been addded", status=status.HTTP_202_ACCEPTED)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
