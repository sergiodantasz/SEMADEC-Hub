from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, FileField
from factory.faker import faker

from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = 'documents.Document'

    administrator = SubFactory(AdministratorFactory)
    title = fake.text(max_nb_chars=200)
    content = FileField()
    slug = Sequence(lambda x: fake.unique.slug())
    created_at = fake.date()
    updated_at = fake.date()

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()
