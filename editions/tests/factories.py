from factory import RelatedFactory, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

from competitions.tests.factories import CompetitionFactory, EditionFactory

fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'
        # django_get_or_create = ['name']

    name = Sequence(lambda x: fake.unique.catch_phrase())

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Class'

    course = SubFactory(CourseFactory)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'

    name = fake.pystr(max_chars=75)

    @post_generation
    def classes(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.classes.add(*extracted)


class TeamEditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamEdition'

    team = SubFactory(TeamFactory)
    edition = SubFactory(EditionFactory)
    score = fake.random_number(digits=4, fix_len=True) / 100
    classification = fake.random_number(digits=1, fix_len=True)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class TeamCompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamCompetition'

    team = SubFactory(TeamFactory)
    competition = SubFactory(CompetitionFactory)
    winner = True

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()


class TeamWithCompetitionsAndEditionsFactory(TeamFactory):
    competitions = RelatedFactory(
        TeamCompetitionFactory,
        factory_related_name='team',
    )
    editions = RelatedFactory(
        TeamEditionFactory,
        factory_related_name='team',
    )
