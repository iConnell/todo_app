from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskView


router = DefaultRouter()
router.register('create/', TaskView)

urlpatterns = [
    path('', TaskView.as_view({
        'post': 'create', 'get': 'list'
    })),
    path('<int:pk>/', TaskView.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }))

]