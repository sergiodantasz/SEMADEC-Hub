from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from archive.models import Collection


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    administrator = SubFactory('users.Administrator')  # Add later
    title = 'This is a placeholder title.'
    cover = ImageField(filename='test_image')
    slug = 'this-is-a-placeholder-title'
    created_at = '05/06/2024'
    updated_at = '05/07/2024'
