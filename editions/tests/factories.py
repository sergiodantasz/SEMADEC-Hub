from factory import (
    PostGeneration,
    RelatedFactory,
    Sequence,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory
from factory.faker import faker

from competitions.tests.factories import CompetitionFactory, EditionFactory

fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.catch_phrase())

    post_generation(fake.unique.clear())


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Class'
        skip_postgeneration_save = True

    course = SubFactory(CourseFactory)

    post_generation(fake.unique.clear())


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'
        skip_postgeneration_save = True

    name = fake.pystr(max_chars=75)
    classes = PostGeneration(lambda obj, create, extracted: obj.classes)

    post_generation(fake.unique.clear())


class TeamEditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamEdition'
        skip_postgeneration_save = True

    team = SubFactory(TeamFactory)
    edition = SubFactory(EditionFactory)

    post_generation(fake.unique.clear())


class TeamCompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamCompetition'
        skip_postgeneration_save = True

    team = SubFactory(TeamFactory)
    competition = SubFactory(CompetitionFactory)
    winner = True

    post_generation(fake.unique.clear())


class TeamWithCompetitionsAndEditionsFactory(TeamFactory):
    competitions = RelatedFactory(
        TeamCompetitionFactory,
        factory_related_name='team',
    )
    editions = RelatedFactory(
        TeamEditionFactory,
        factory_related_name='team',
    )

    post_generation(fake.unique.clear())
