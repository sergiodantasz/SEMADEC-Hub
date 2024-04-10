from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from home.tests.factories import CollectionFactory
from utils.generate_placeholder import generate_placeholder

fake = faker.Faker('pt_BR')


class CollectionArchiveFactory(CollectionFactory):
    collection_type = 'image'
    cover = ImageField(from_func=generate_placeholder)


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Image'
        skip_postgeneration_save = True

    collection = SubFactory(CollectionArchiveFactory)
    content = ImageField(from_func=generate_placeholder)
