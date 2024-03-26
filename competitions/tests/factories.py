from random import choice

from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker
from faker.providers import BaseProvider


class ModelsDummyData(BaseProvider):
    def category(self):
        return choice(['Masculino', 'Feminino', 'Misto'])

    def sport(self):
        options = [
            'Futebol',
            'Vôlei',
            'Basquete',
            'Natação',
            'Sinuca',
            'Atletismo',
            'Handbol',
            'Badminton',
            'Tênis de Mesa',
        ]
        return choice(options)


fake = faker.Faker('pt_BR')
fake.add_provider(ModelsDummyData)


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
        django_get_or_create = ('name',)
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.category())
    post_generation(fake.unique.clear())


class SportFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Sport'
        django_get_or_create = ('name',)
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.sport())
    date_time = None
    post_generation(fake.unique.clear())

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.categories.add(*extracted)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Match'
        skip_postgeneration_save = True

    sport = SubFactory(SportFactory)
    category = SubFactory(CategoryFactory)
    edition = SubFactory(EditionFactory)
    scoreboard = fake.pystr(max_chars=10)
    date_time = None


class TestFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Test'
        skip_postgeneration_save = True

    title = fake.unique.text(max_nb_chars=50)
    description = ''
    date_time = None
