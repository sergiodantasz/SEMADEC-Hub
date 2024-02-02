from factory import RelatedFactory, SubFactory
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from home.tests.factories import TagFactory
from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'

    administrator = SubFactory(AdministratorFactory)  # Add later
    title = fake.pystr(max_chars=200)
    cover = ImageField()
    slug = fake.slug()
    created_at = fake.date()
    updated_at = fake.date()
    tags = SubFactory(TagFactory)


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'
