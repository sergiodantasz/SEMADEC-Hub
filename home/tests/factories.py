from factory import Sequence
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Tag'
        # django_get_or_create = ['name', 'slug']

    name = Sequence(lambda x: fake.pystr(max_chars=50))
    slug = Sequence(lambda x: fake.slug())
