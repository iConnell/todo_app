import json
from turtle import title
from django.urls import reverse
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from todo_app.models import Task
from .factories import TaskFactory, UserFactory
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

@pytest.fixture
def create_task():
    def _make_task(user, **kwargs):
        return TaskFactory(created_by=user, **kwargs)
    return _make_task


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
            url, data=json.dumps(data), content_type='application/json'
        )
        
        assert res.status_code == 201
        assert res.data['id']
        assert res.data['title'] == data['title']
        assert res.data['description'] == data['description']
        assert res.data['completed'] == False
        
    def test_get_tasks_view(self, api_client, user, create_task):
        client = api_client

        create_task(user=user,title="Task 1")
        create_task(user=user,title="Task 2")

        url = reverse('task-create')

        res = client.get(url, content_type='application/json')
        results = res.data['results']

        res_data = json.dumps(results)
        res_data = json.loads(res_data)
        res_data = sorted(res_data, key=lambda task: task['title'])
        
        assert res.status_code == 200
        assert len(res_data) == 2

        assert res_data[0]["id"]
        assert res_data[0]["title"] == "Task 1"
        assert res_data[0]["created_by"] == user.id

        assert res_data[1]["id"]
        assert res_data[1]["title"] == "Task 2"
        assert res_data[1]["created_by"] == user.id
        

    def test_task_detail_view(self, user, create_task, api_client):
        client = api_client
        task = create_task(user=user)

        url = reverse('task-detail', kwargs={'pk': task.id})

        res = client.get(url, content_type='application/json')

        assert res.status_code == 200
        assert res.data["id"]
        assert res.data["title"] == "Test Task"
        assert res.data["description"] == "This is a test Task"
        assert res.data["created_by"] == user.id

    
    def test_update_task_view(self, user, create_task, api_client):
        client = api_client
        
        task = create_task(user=user)

        url = reverse('task-detail', kwargs={'pk': task.id})

        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }

        res = client.patch(url, json.dumps(data), content_type="application/json")

        updated_task = Task.objects.get(id=task.id)
        assert res.status_code == 200
        assert updated_task.title == data["title"]
        assert updated_task.description == data["description"]
        assert updated_task.completed == data["completed"]


    def test_delete_task_view(self, user, create_task, api_client):
        client = api_client

        create_task(user=user, title="Task 1")
        task_2 = create_task(user=user, title="Task 2")

        url = reverse('task-create')
        res = client.get(url, content_type='application/json')

        results = res.data['results']
        res_data = json.dumps(results)
        res_data = json.loads(res_data)
        assert res.status_code == 200
        assert len(res_data) == 2

        url = reverse('task-detail', kwargs={'pk': task_2.id})
        res = client.delete(url, content_type='application/json')
        assert res.status_code == 204

        url = reverse('task-create')
        res = client.get(url, content_type='application/json')

        results = res.data['results']
        res_data = json.dumps(results)
        res_data = json.loads(res_data)
        assert res.status_code == 200
        assert len(res_data) == 1





