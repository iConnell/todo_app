import factory
from factory import post_generation
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user%d' % n)

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = User