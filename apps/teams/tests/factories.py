from random import choice, randint

from factory import RelatedFactory, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker
from faker.providers import BaseProvider


class ModelsDummyData(BaseProvider):
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

    def entry_year(self):
        return randint(2000, 3000)


fake = faker.Faker('pt_BR')
fake.add_provider(ModelsDummyData)


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'teams.Course'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.text(max_nb_chars=75))
    slug = Sequence(lambda x: fake.unique.slug())


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'teams.Team'
        skip_postgeneration_save = True
        django_get_or_create = ('name',)

    name = Sequence(lambda x: fake.team_name())  # Change later
    slug = Sequence(lambda x: fake.unique.slug())

    @post_generation
    def classes(self, created, extracted):
        if not created or not extracted:
            return
        self.classes.add(*extracted)


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = 'teams.Class'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.text(max_nb_chars=30))
    entry_year = Sequence(lambda x: fake.unique.entry_year())
    slug = Sequence(lambda x: fake.unique.slug())
    course = SubFactory(CourseFactory)
