from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Category'

    name = fake.unique.pystr(max_chars=15)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class SportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Sport'

    name = fake.unique.pystr(max_chars=30)
    category = SubFactory(CategoryFactory)
    date_time = None

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class TestFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Test'


class TestOrSportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.TestOrSport'


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Competition'
