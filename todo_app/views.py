from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class TaskCreateView(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            task = serializer.create(serializer.validated_data, created_by=user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


