from rest_framework import serializers

from app_teachers.models import TeacherModel


class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = ['image', 'first_name', 'last_name', 'username',
                  'gender', 'phone_number']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
