from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class EditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Edition'
        skip_postgeneration_save = True

    year = Sequence(lambda x: fake.unique.random_number(digits=4, fix_len=True))
    name = Sequence(lambda x: fake.unique.pystr(max_chars=10))
    edition_type = fake.pystr(max_chars=10)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Category'
        skip_postgeneration_save = True

    name = fake.unique.pystr(max_chars=15)


class SportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Sport'
        skip_postgeneration_save = True

    name = fake.unique.pystr(max_chars=30)
    category = SubFactory(CategoryFactory)
    date_time = None


class TestFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Test'
        skip_postgeneration_save = True

    title = fake.unique.text(max_nb_chars=50)
    description = ''
    date_time = None


class TestOrSportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.TestOrSport'
        skip_postgeneration_save = True

    test = SubFactory(TestFactory)
    sport = SubFactory(SportFactory)


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Competition'
        skip_postgeneration_save = True

    edition = SubFactory(EditionFactory)
    test_or_sport = SubFactory(TestOrSportFactory)
