from random import choice, randint
from random import uniform as randfloat

from factory import (
    PostGeneration,
    RelatedFactory,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory
from factory.faker import faker
from faker.providers import BaseProvider


class ModelsDummyData(BaseProvider):
    def edition_name(self):
        options = [
            'I Semadec',
            'II Semadec',
            'III Semadec',
            'IV Semadec',
            'V Semadec',
            'VI Semadec',
            'VII Semadec',
            'VIII Semadec',
            'IX Semadec',
            'X Semadec',
        ]
        return choice(options)


fake = faker.Faker('pt_BR')
fake.add_provider(ModelsDummyData)


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.catch_phrase())


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'
        skip_postgeneration_save = True
        django_get_or_create = ('name',)

    name = fake.pystr(max_chars=75)


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Class'
        skip_postgeneration_save = True

    course = SubFactory(CourseFactory)
    team = SubFactory(TeamFactory)


class EditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Edition'
        skip_postgeneration_save = True
        # django_get_or_create = ('name',)

    year = Sequence(lambda x: fake.unique.random_number(digits=4, fix_len=True))
    name = Sequence(lambda x: fake.edition_name())
    edition_type = fake.pystr(max_chars=10)
    theme = fake.text(max_nb_chars=100)


class EditionTeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.EditionTeam'
        skip_postgeneration_save = True
        django_get_or_create = ('edition', 'team')

    edition = SubFactory(EditionFactory)
    team = SubFactory(TeamFactory)
    score = randfloat(1.0, 100.0)
    classification = randint(1, 10)


class EditionWithTeamFactory(EditionFactory):
    teams = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
    )


class EditionWith2TeamsFactory(EditionFactory):
    team1 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
        team__name='time1',
    )
    team2 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
        team__name='time2',
    )


class TeamWith2EditionsFactory(TeamFactory):
    edition1 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='team',
        edition__name='edicao1',
    )
    edition2 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='team',
        edition__name='edicao2',
    )
