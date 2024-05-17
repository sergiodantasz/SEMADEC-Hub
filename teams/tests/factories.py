from factory import RelatedFactory, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


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
    slug = Sequence(lambda x: fake.unique.slug())
    course = SubFactory(CourseFactory)
