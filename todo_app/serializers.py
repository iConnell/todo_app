from rest_framework.serializers import ModelSerializer
from .models import Task

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = ['deleted']


class TaskCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at'
        ]

    def create(self, validated_data, **kwargs):
        created_by = kwargs['created_by']
        task = super().create(dict(created_by=created_by, **validated_data))
        return task
    