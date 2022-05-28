from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title