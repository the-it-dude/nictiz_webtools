"""Generic Factories."""
import factory

from django.contrib.auth.models import Group, User


class UserFactory(factory.django.DjangoModelFactory):
    """User Factory."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'person{0}'.format(n))


class GroupFactory(factory.django.DjangoModelFactory):
    """Group Factory."""

    class Meta:
        model = Group
