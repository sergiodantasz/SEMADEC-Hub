from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

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
    created_at = fake.date()
    updated_at = fake.date()

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'

    collection = SubFactory(CollectionFactory)
    content = fake.unique.file_path()

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()
