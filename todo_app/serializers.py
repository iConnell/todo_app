from rest_framework.serializers import ModelSerializer, ChoiceField, IntegerField, Serializer
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
    

operation_type_choices = (
    ("addition", "addition"),
    ("subtraction", "subtraction"),
    ("multiplication", "multiplication")
)

class CalculationSerializer(Serializer):
    operation_type = ChoiceField(choices=operation_type_choices)
    x = IntegerField()
    y = IntegerField()