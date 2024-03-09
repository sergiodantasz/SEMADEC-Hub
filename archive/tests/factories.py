from factory import PostGeneration, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from archive.models import Collection
from home.tests.factories import TagFactory
from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'
        skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)  # Add later
    files = PostGeneration(lambda obj, create, extracted: obj.files)
    title = Sequence(lambda x: fake.unique.pystr(max_chars=200))
    type = FuzzyChoice(Collection.COLLECTION_TYPE_CHOICES)
    slug = Sequence(lambda x: fake.unique.slug())
    tags = PostGeneration(lambda obj, create, extracted: obj.tags)
    post_generation(fake.unique.clear())


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'
        skip_postgeneration_save = True

    display_name = fake.pystr(max_chars=225)
    content = fake.unique.file_path()

    post_generation(fake.unique.clear())
