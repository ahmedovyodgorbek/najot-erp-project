from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

UserModel = get_user_model()


class AdminCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=50)

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name',
                  'password', 'password2', 'gender', 'phone_number', 'role']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        try:
            user = UserModel.objects.create(**validated_data)
            user.set_password(password)
            user.is_staff = True
            user.role = "admin"
            user.save()
            admin_group = Group.objects.get(name='admins')
            user.groups.add(admin_group)
            return user
        except:
            raise serializers.ValidationError("Something went wrong :(")
