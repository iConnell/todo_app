from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskCreateView


router = DefaultRouter()
router.register('create/', TaskCreateView)

urlpatterns = [
    path('create/', TaskCreateView.as_view({
        'post': 'create'
    }))
]