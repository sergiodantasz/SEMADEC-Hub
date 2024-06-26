from random import choice, randint
from random import uniform as randfloat

from django.utils import timezone
from factory import (
    RelatedFactory,
    Sequence,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory
from factory.faker import faker
from faker.providers import BaseProvider

from apps.editions.tests.factories import EditionFactory
from apps.teams.tests.factories import TeamFactory


class ModelsDummyData(BaseProvider):
    def category(self):
        return choice(['Masculino', 'Feminino', 'Misto'])

    def sport(self):
        options = [
            'Futebol',
            'Futsal',
            'Vôlei de Quadra',
            'Vôlei de Areia',
            'Basquete',
            'Natação',
            'Sinuca',
            'Atletismo',
            'Handbol',
            'Badminton',
            'Ping Pong',
        ]
        return choice(options)

    def test(self):
        options = [
            'Fabricação de Pipa',
            'Mapa do Tesouro',
            'Cabo de Guerra',
            'Corrida de Saco',
            'Tiro ao Alvo com Estilingue',
            'Circuito',
            'Caminhada Orientada a Objetos',
        ]
        return choice(options)


fake = faker.Faker('pt_BR')
fake.add_provider(ModelsDummyData)


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
    slug = Sequence(lambda x: fake.unique.slug())

    @post_generation
    def categories(self, created, extracted):
        if not created or not extracted:
            return
        self.categories.add(*extracted)  # type: ignore

    post_generation(fake.unique.clear())


class SportCategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.SportCategory'
        skip_postgeneration_save = True
        # django_get_or_create = ('edition', 'team')

    sport = SubFactory(SportFactory)
    category = SubFactory(CategoryFactory)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Match'
        skip_postgeneration_save = True

    sport_category = SubFactory(SportCategoryFactory)
    edition = SubFactory(EditionFactory)
    date_time = fake.date_time(tzinfo=timezone.get_current_timezone())


class MatchTeamFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.MatchTeam'
        skip_postgeneration_save = True

    match = SubFactory(MatchFactory)
    team = SubFactory(TeamFactory)
    score = round(randfloat(1.0, 100.0), 2)


class MatchWithTeamFactory(MatchFactory):
    teams = RelatedFactory(
        MatchTeamFactory,
        factory_related_name='match',
    )


class TestFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.Test'
        skip_postgeneration_save = True

    title = Sequence(lambda x: fake.unique.pystr(max_chars=50))  # Change to .test()
    slug = Sequence(lambda x: fake.unique.slug())
    description = fake.text(max_nb_chars=200)
    date_time = fake.date_time(tzinfo=timezone.get_current_timezone())

    @post_generation
    def teams(self, created, extracted):
        if not created or not extracted:
            return
        self.teams.add(*extracted)  # type: ignore

    post_generation(fake.unique.clear())


class TestTeamFactory(DjangoModelFactory):
    class Meta:
        model = 'competitions.TestTeam'
        skip_postgeneration_save = True

    test = SubFactory(TestFactory)
    team = SubFactory(TeamFactory)
    score = randfloat(1.0, 100.0)
    # winner = choice([True, False])
    post_generation(fake.unique.clear())


class TestWithTeamFactory(TestFactory):
    teams = RelatedFactory(
        TestTeamFactory,
        factory_related_name='test',
    )
    post_generation(fake.unique.clear())
