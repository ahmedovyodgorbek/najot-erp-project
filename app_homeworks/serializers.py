from rest_framework import serializers

from . import models


class HomeworkTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HomeworkTaskModel
        fields = '__all__'
