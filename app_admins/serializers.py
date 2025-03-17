from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from app_groups.models import GroupModel

UserModel = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name',
                  'gender', 'phone_number', 'role', 'image', 'groups']


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=50, write_only=True)
    groups = serializers.SlugRelatedField(
        queryset=GroupModel.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name',
                  'password', 'password2', 'gender', 'phone_number', 'role', 'groups']
        extra_kwargs = {
            "role": {'required': True},
            "password": {'write_only': True},
            "password2": {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        role = attrs.get("role")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        if role not in ["admin", "student", "teacher"]:
            raise serializers.ValidationError("Role is invalid")
        return attrs

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        password = validated_data.pop("password")
        validated_data.pop("password2")
        try:
            user = UserModel.objects.create(**validated_data)
            user.set_password(password)
            if user.role == "admin":
                user.is_staff = True
                user.is_superuser = True
            if groups:
                user.groups.set(groups)
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Something went wrong :({e}")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['groups'] = [group.slug for group in instance.groups.all()]  # ✅ slug output
        return rep
