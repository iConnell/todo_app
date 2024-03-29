from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskView, CalculationView


router = DefaultRouter()
router.register('create/', TaskView, basename='tasks')

urlpatterns = [
    path('', TaskView.as_view({
        'post': 'create', 'get': 'list'
    }), name='task-create'),
    path('<int:pk>/', TaskView.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }), name='task-detail'),
    path('eval/', CalculationView.as_view(), name='calculation')

]