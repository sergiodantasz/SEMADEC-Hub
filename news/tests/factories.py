from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class NewsFactory(DjangoModelFactory):
    class Meta:
        model = 'news.News'
