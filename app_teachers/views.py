# from django.shortcuts import render
# from rest_framework.generics import RetrieveUpdateAPIView
# from rest_framework.permissions import IsAuthenticated
#
# from app_common.permissions import IsOwnerOrReadOnly
# from app_teachers.models import TeacherModel
# from . import serializers
#
#
# class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = TeacherModel.objects.all()
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#     serializer_class = serializers.ProfileUpdateSerializer
#
#     def get_object(self):
#         return self.request.user
