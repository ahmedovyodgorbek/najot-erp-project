from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from app_groups.models import GroupModel, SubjectModel
from app_lessons.serializers import MyLessonsSerializer

UserModel = get_user_model()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = ['title', 'slug']


class GroupsSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.title', read_only=True)

    class Meta:
        model = GroupModel
        fields = ['title', 'slug', 'subject']


class GroupMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'role']


class GroupDetailSerializer(serializers.ModelSerializer):
    members = GroupMembersSerializer(many=True, read_only=True)
    subject_title = serializers.CharField(source='subject.title', read_only=True)
    lessons = MyLessonsSerializer(many=True, read_only=True)

    class Meta:
        model = GroupModel
        fields = ['title', 'slug', 'time', 'members', 'subject_title', 'lessons']


class AddUserToGroupSerializer(serializers.Serializer):
    group_title = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    def validate(self, attrs):
        group_title = attrs.get("group_title")
        username = attrs.get("username")

        try:
            group = GroupModel.objects.get(title=group_title)
        except GroupModel.DoesNotExist:
            raise NotFound(detail="Group not found")
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise NotFound(detail="User not found")
        attrs['group'] = group
        attrs['user'] = user
        return attrs


class AddSubjectToGroupSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    group = serializers.CharField(max_length=255)

    def validate(self, attrs):
        subject = attrs.get("subject")
        group = attrs.get("group")

        try:
            group = GroupModel.objects.get(title=group)
        except GroupModel.DoesNotExist:
            raise NotFound(detail="Group not found")
        try:
            subject = SubjectModel.objects.get(title=subject)
        except SubjectModel.DoesNotExist:
            raise NotFound(detail="Subject not found")
        attrs['group'] = group
        attrs['subject'] = subject
        return attrs
