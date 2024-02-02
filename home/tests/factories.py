from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Tag'

    name = fake.pystr(max_chars=50)
    slug = fake.pystr(max_chars=75)
