from factory import PostGeneration, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from home.tests.factories import TagFactory
from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'
        # django_get_or_create = ['slug']
        # skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)  # Add later
    title = Sequence(lambda x: fake.unique.pystr(max_chars=200))
    slug = Sequence(lambda x: fake.unique.slug())
    tags = PostGeneration(lambda obj, create, extracted: obj.tags)
    post_generation(fake.unique.clear())


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'

    collection = SubFactory(CollectionFactory)
    content = fake.unique.file_path()

    post_generation(fake.unique.clear())
