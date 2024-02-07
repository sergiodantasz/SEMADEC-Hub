from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class EditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Edition'

    year = fake.unique.random_number(digits=4, fix_len=True)
    name = fake.unique.pystr(max_chars=10)
    edition_type = fake.pystr(max_chars=10)
    theme = fake.pystr(max_chars=100)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


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

    title = fake.unique.text(max_nb_chars=50)
    description = ''
    date_time = None

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class TestOrSportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.TestOrSport'

    test = SubFactory(TestFactory)
    sport = SubFactory(SportFactory)


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Competition'

    edition = SubFactory(EditionFactory)
    test_or_sport = SubFactory(TestOrSportFactory)
