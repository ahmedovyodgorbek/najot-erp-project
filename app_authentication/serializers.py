from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from app_groups.serializers import GroupsSerializer

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = UserModel.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User was not found")

        attrs['user'] = user

        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect")
        return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['image', 'first_name', 'last_name', 'username',
                  'gender', 'phone_number', 'role']
        extra_kwargs = {'role': {'read_only': True}}

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=30)
    password1 = serializers.CharField(max_length=30, write_only=True)
    password2 = serializers.CharField(max_length=30, write_only=True)

    def validate(self, attrs):
        user = self.context.get('user')
        old_password = attrs.get('old_password')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if not user.check_password(old_password):
            raise serializers.ValidationError("Your old password is incorrect")
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['password1'])
        user.save()
        return user
