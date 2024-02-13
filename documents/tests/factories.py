from factory import PostGeneration, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, FileField
from factory.faker import faker

from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = 'documents.Document'
        skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)
    title = fake.text(max_nb_chars=200)
    content = FileField()
    slug = Sequence(lambda x: fake.unique.slug())
    tags = PostGeneration(lambda obj, create, extracted: obj.tags)

    post_generation(fake.unique.clear())
