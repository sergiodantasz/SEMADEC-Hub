from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'

    name = fake.catch_phrase()


class EditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Edition'


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Class'


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Team'


class TeamEditionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamEdition'


class TeamCompetitionFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.TeamCompetition'
