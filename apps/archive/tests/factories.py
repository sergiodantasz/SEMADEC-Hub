from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from home.tests.factories import CollectionFactory

fake = faker.Faker('pt_BR')


class CollectionArchiveFactory(CollectionFactory):
    collection_type = 'image'
    cover = ImageField(width=10, height=10)


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Image'
        skip_postgeneration_save = True

    collection = SubFactory(CollectionArchiveFactory)
    content = ImageField(width=10, height=10)
