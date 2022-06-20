import json
from django.urls import reverse
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .factories import UserFactory
from django.contrib.auth.models import User

# Create your tests here.

@pytest.fixture
def user():
    user: User = UserFactory()
    return user


@pytest.fixture
def api_client(user):
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.mark.django_db
class TestTaskViews:
    def test_create_task_view(self, api_client):
        client = api_client
        url = reverse('task-create')

        data = {
            "title": "Test Task",
            "description": "This is a test task",
        }

        res = client.post(
            url, json.dumps(data), content_type='application/json'
        )
        print("testing")
        
        assert res.status_code == 201