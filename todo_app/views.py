from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import TaskCreateUpdateSerializer, TaskSerializer, CalculationSerializer
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


# Create your views here.


class TaskView(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(deleted=False, created_by=self.request.user)
        return queryset

    def get_object(self):
        user = self.request.user
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id, created_by=user)
        return task

    def create(self, request, *args, **kwargs):
        serializer = TaskCreateUpdateSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            task = serializer.create(serializer.validated_data, created_by=user)
            read_serializer = self.get_serializer(task)
            return Response(
                read_serializer.data, status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer =  TaskCreateUpdateSerializer(instance=task, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        task_instance = serializer.update(task, serializer.validated_data)
        response_data = self.get_serializer(task_instance).data
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        


class CalculationView(APIView):
    serializer_class = CalculationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_type = serializer.validated_data.get('operation_type')
        x = serializer.validated_data.get('x')
        y = serializer.validated_data.get('y')

        if operation_type == "addition":
            result = x + y
        elif operation_type == "subtraction":
            result = x - y
        elif operation_type == "multiplication":
            result = x * y

        response = {
            "slackUsername": "iConnell",
            "result": result,
            "operation_type": operation_type,

        }
        return Response(response)