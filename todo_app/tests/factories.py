import factory
from factory import post_generation
from django.contrib.auth.models import User

from todo_app.models import Task


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user%d' % n)

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = User

class TaskFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    title = "Test Task"
    description = "This is a test Task"

    class Meta:
        model = Task