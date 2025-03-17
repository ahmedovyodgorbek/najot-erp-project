from django.contrib.auth import get_user_model
from rest_framework import serializers

from app_groups.serializers import GroupsSerializer

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    group_titles = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name',
                  'gender', 'phone_number', 'role', 'image', 'group_titles']

    def get_group_titles(self, obj):
        return [group.title for group in obj.groups.all()]
