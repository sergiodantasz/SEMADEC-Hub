from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'
        skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)  # Add later
    title = fake.pystr(max_chars=200)
    cover = ImageField()
    slug = fake.slug()
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
