from random import choice, choices, randint
from random import uniform as randfloat

from factory import (
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

    def edition_type(self):
        options = {
            'classes': 'Confronto entre turmas',
            'courses': 'Confronto entre cursos',
        }
        return choice(list(options.keys()))

    def team_name(self):
        options = [
            'Técnico Integrado em Informática',
            'Técnico Integrado em Manutenção e Suporte em Informática',
            'Técnico Integrado em Eletrônica',
            'Técnico Integrado em Alimentos',
            'Graduação em Tecnologia em Sistemas para Internet',
            'Graduação em Química',
        ]
        return choice(options)

    def edition_year(self):
        return randint(2000, 3000)


fake = faker.Faker('pt_BR')
fake.add_provider(ModelsDummyData)


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.text(max_nb_chars=75))


class EditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Edition'
        skip_postgeneration_save = True
        django_get_or_create = ('name',)

    year = Sequence(lambda x: fake.unique.edition_year())
    name = Sequence(lambda x: fake.edition_name())
    edition_type = fake.edition_type()
    theme = fake.text(max_nb_chars=100)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'
        skip_postgeneration_save = True
        django_get_or_create = ('name',)

    name = Sequence(lambda x: fake.pystr(max_chars=75))


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Class'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.text(max_nb_chars=30))
    course = SubFactory(CourseFactory)
    team = SubFactory(TeamFactory)


class EditionTeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.EditionTeam'
        skip_postgeneration_save = True
        django_get_or_create = ('edition', 'team')

    edition = SubFactory(EditionFactory)
    team = SubFactory(TeamFactory)
    score = randfloat(1.0, 100.0)


class EditionWithTeamFactory(EditionFactory):
    teams = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
    )


class EditionWith2TeamsFactory(EditionFactory):
    team1 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
        team__name=fake.unique.team_name(),
    )
    team2 = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
        team__name=fake.unique.team_name(),
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
