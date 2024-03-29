from random import randint
from random import uniform as randfloat

from factory import (
    PostGeneration,
    RelatedFactory,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.catch_phrase())


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'
        skip_postgeneration_save = True

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

    year = Sequence(lambda x: fake.unique.random_number(digits=4, fix_len=True))
    name = Sequence(lambda x: fake.unique.pystr(max_chars=10))
    edition_type = fake.pystr(max_chars=10)
    theme = fake.text(max_nb_chars=100)


class EditionTeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.EditionTeam'
        skip_postgeneration_save = True

    edition = SubFactory(EditionFactory)
    team = SubFactory(TeamFactory)
    score = randfloat(1.0, 100.0)
    classification = randint(1, 10)


class EditionWithTeamFactory(EditionFactory):
    teams = RelatedFactory(
        EditionTeamFactory,
        factory_related_name='edition',
    )
