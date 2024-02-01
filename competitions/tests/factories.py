from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Category'


class SportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Sport'


class TestFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Test'


class TestOrSportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.TestOrSport'


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Competition'
